from openai import OpenAI
import json
import os

def generate_chapter_structure(api_key, structured_data_file, output_language, base_url, model):
    """
    根据PPT内容生成章节结构，并生成教材标题
    :param api_key: API密钥
    :param structured_data_file: 结构化数据文件路径
    :param output_language: 输出语言（默认中文）
    :param base_url: API基础URL（默认Openai）
    :param model: 模型名称（默认gpt-4o）
    :return: 包含章节结构列表和教材标题的字典，格式为 {"chapters": [...], "title": "教材标题"}
    """
    # 检查文件是否存在
    if not os.path.exists(structured_data_file):
        print(f"错误：文件 {structured_data_file} 不存在")
        return None

    try:
        # 读取文件内容
        with open(structured_data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误：文件 {structured_data_file} 不是有效的 JSON 格式")
        print(f"详细错误信息：{str(e)}")
        return None
    except Exception as e:
        print(f"错误：读取文件 {structured_data_file} 时发生未知错误")
        print(f"详细错误信息：{str(e)}")
        return None

    # 检查文件内容是否为空
    if not data:
        print(f"错误：文件 {structured_data_file} 内容为空")
        return None

    # 提取前3页内容
    try:
        first_three_pages = [page['raw_text'] for page in data[:3]]
        combined_text = "\n".join(first_three_pages)
    except KeyError as e:
        print(f"错误：文件 {structured_data_file} 中缺少 'raw_text' 字段")
        print(f"详细错误信息：{str(e)}")
        return None
    except Exception as e:
        print(f"错误：提取前3页内容时发生未知错误")
        print(f"详细错误信息：{str(e)}")
        return None

    # 调用API生成章节结构
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    try:
        # 第一次调用：生成章节结构
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"你是一个专业的教材编写助手，请根据PPT内容设计合理的教材章节结构。输出语言：{output_language}"},
                {"role": "user", "content": f"""请根据以下PPT内容设计教材章节结构，返回格式必须为JSON数组，每个章节包含'title'和'content'字段。
                要求：
                1. 章节设计应基于PPT内容的逻辑结构，而不是直接复制PPT目录。
                2. 每个章节应包含明确的学习目标和知识点。
                3. 章节数量应适中，通常为5-10章。
                4. 章节标题和内容描述必须使用{output_language}。

                PPT内容：
                {combined_text}

                示例：
                ```json
                [
                    {{
                        "title": "章节标题",
                    "content": "本章将介绍..."
                    }}
                ]
                ```"""}
            ],
            temperature=0.7,
            max_tokens=3000,
            stream=False
        )

        # 检查API返回内容是否为空
        if not response.choices[0].message.content:
            print("错误：API返回内容为空")
            return None

        # 去除Markdown代码块标记
        api_response = response.choices[0].message.content
        if api_response.startswith("```json") and api_response.endswith("```"):
            api_response = api_response[7:-3].strip()

        # 尝试解析JSON
        try:
            chapter_structure = json.loads(api_response)
        except json.JSONDecodeError as e:
            print("错误：API返回内容不是有效的JSON格式")
            print(f"API返回内容：{api_response}")
            return None

        # 确保每个章节包含 content 字段
        for chapter in chapter_structure:
            if 'content' not in chapter:
                chapter['content'] = ""

        # 第二次调用：生成教材标题（直接使用前三页内容）
        title_response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"你是一个专业的教材编写助手，我需要你帮我设计一个教材的名字。输出语言：{output_language}"},
                {"role": "user", "content": f"请根据以下PPT内容生成一个合适的教材标题（只回答我标题是什么，不需要任何其他的解释），标题必须使用{output_language}：\n{combined_text}"}
            ],
            temperature=0.3,
            max_tokens=40,
            stream=False
        )
        textbook_title = title_response.choices[0].message.content.strip()

        # 返回章节结构和教材标题
        return {
            "chapters": chapter_structure,
            "title": textbook_title
        }
    except Exception as e:
        print(f"错误：调用语言模型时发生错误")
        print(f"详细错误信息：{str(e)}")
        return None
    


def generate_chapter_content(api_key, chapter_title, pages_content, base_url, model, customization_prompt="", stream=False):
    """
    生成单个章节的内容
    :param api_key: 大语言模型的 API密钥
    :param chapter_title: 章节标题
    :param pages_content: 该章节对应的PPT页面内容
    :param customization_prompt: 定制化需求
    :param stream: 是否使用流式输出（可选参数）
    :param base_url: API基础URL（默认Openai）
    :param model: 模型名称（默认gpt-4o）
    :return: 生成的章节内容
    """
    # 参数验证
    if not api_key or not isinstance(api_key, str):
        print("错误：API密钥无效，必须为非空字符串")
        return None

    if not chapter_title or not isinstance(chapter_title, str):
        print("错误：章节标题无效，必须为非空字符串")
        return None

    if not pages_content or not isinstance(pages_content, str):
        print("错误：PPT页面内容无效，必须为非空字符串")
        return None

    if not base_url or not isinstance(base_url, str):
        print("错误：API基础URL无效，必须为非空字符串")
        return None

    if not model or not isinstance(model, str):
        print("错误：模型名称无效，必须为非空字符串")
        return None

    if not isinstance(customization_prompt, str):
        print("错误：定制化需求必须是字符串")
        return None

    if not isinstance(stream, bool):
        print("错误：stream参数必须是布尔值")
        return None

    # 检查API密钥格式（基本格式验证）
    if not api_key.startswith("sk-"):
        print("警告：API密钥格式可能不正确，通常以'sk-'开头")

    # 检查base_url格式
    if not base_url.startswith(("http://", "https://")):
        print("警告：API基础URL格式可能不正确，应以http://或https://开头")

    # 检查模型名称格式
    if not model.lower() in ["gpt-4", "gpt-4o", "gpt-3.5-turbo"]:
        print("警告：模型名称可能不正确，建议使用gpt-4或gpt-3.5-turbo")

    # 检查章节标题长度
    if len(chapter_title) > 100:
        print("警告：章节标题过长，建议控制在100个字符以内")

    # 检查PPT内容长度
    if len(pages_content) < 50:
        print("警告：PPT内容过短，可能无法生成完整章节")
    elif len(pages_content) > 10000:
        print("警告：PPT内容过长，建议分章节处理")


    print(f"正在生成章节：{chapter_title}...")
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )



    try:
        # 详细的任务背景和输出格式要求
        system_prompt = """
        你是一个专业的教材编写助手，负责根据PPT内容编写高质量的教材章节。
        任务背景：
        1. 这是一份用于大学教学的教材，目标读者是本科生或研究生。
        2. 教材需要兼顾理论深度和实用性，帮助学生理解核心概念并掌握实际应用。
        3. 教材内容需要结构清晰、逻辑严谨，适合课堂教学和课后自学。

        输出格式要求：
        1. 必须严格遵循以下章节结构：
            # 第X章 《章节标题》
            ## 前言
            这一章主要介绍的内容是：
            （简要概述本章内容，2-3句话）
        
            ## 理论部分
            （详细的理论解释，包含核心概念、原理等）
        
            ## 示例部分
            （提供1-2个实际案例，说明理论的应用）
        
            ## 总结
            （总结本章要点，2-3句话）
        
            ## 练习题
            （提供3-5个与本章内容相关的练习题，如果有要求需要提供题目的话）
        2. 章节编号必须与输入保持一致
        3. 语言风格：专业学术风格；关键词可以加粗处理。
        """

        # 用户输入的任务细节
        user_prompt = f"""
        请根据以下PPT内容编写教材章节{customization_prompt}。
        具体要求：
        1. 章节标题：{chapter_title}
        2. 内容详实，结构清晰，符合教材标准。不要出现太多的分条罗列，最好是一段一段来描述，有需要几个点介绍的时候，也可以分条罗列，不要出现太多。
        3. 包含以下内容：
           - 理论解释：深入浅出地解释核心概念。
           - 示例：提供1-2个实际案例。
        4. 语言风格和其他要求：{customization_prompt}（如果未指定，则使用默认的专业学术风格）。

        PPT内容：
        {pages_content}
        """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=6000,
            stream=stream
        )
        # 新增错误检查
        if not response.choices:
            print(f"错误：章节 {chapter_title} 生成失败，API返回结果为空")
            return None
            
        if not response.choices[0].message.content:
            print(f"错误：章节 {chapter_title} 生成失败，API返回内容为空")
                    
        # 检查内容长度是否合理
        generated_content = response.choices[0].message.content
        if len(generated_content) < 100:  # 假设最少100个字符
            print(f"警告：章节 {chapter_title} 生成内容过短，可能存在问题")
            print(f"生成内容：{generated_content[:200]}...")  # 打印前200个字符用于调试

        print(f"章节 {chapter_title} 生成完成！")
        return generated_content
    except Exception as e:
        print(f"章节 {chapter_title} 生成失败：{str(e)}")
        return None


def generate_textbook_from_ppt(api_key, structured_data_file, output_file, output_language, base_url, model, customization_prompt="", stream=False):
    """
    根据PPT内容生成详细的课程教材
    :param api_key: API密钥
    :param structured_data_file: 结构化数据文件路径
    :param output_file: 生成的教材文件路径
    :param customization_prompt: 定制化需求
    :param output_language: 输出语言（默认中文）
    :param stream: 是否使用流式输出（可选参数）
    :param base_url: AAPI基础URL（默认Openai）
    :param model: 模型名称（默认gpt-4o）
    """
    print("正在分析PPT内容...")
    # 第一步：生成章节结构和教材标题
    print("正在生成教材大纲...")
    structure_result = generate_chapter_structure(api_key, structured_data_file, output_language, base_url, model)
    if not structure_result:
        print("生成大纲失败，请检查PPT内容或API连接。")
        return

    chapter_structure = structure_result["chapters"]
    textbook_title = structure_result["title"]

    # 第二步：生成教材摘要
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    try:
        # 将章节结构转换为字符串
        chapters_summary = "\n".join([f"{i+1}. {chapter['title']}" for i, chapter in enumerate(chapter_structure)])

        # 调用API生成摘要
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的教材编写助手"},
                {"role": "user", "content": f"请根据以下章节结构生成教材摘要，输出语言：{output_language}。\n{chapters_summary}，\n3. 生成一大段，不要出现分条罗列，也不用输出标题，就直接生成摘要，其他的都不需要。"}
            ],
            temperature=0.7,
            max_tokens=800
        )
        textbook_abstract = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"生成教材摘要失败：{str(e)}")
        textbook_abstract = "未能生成摘要"

    # 显示教材标题和章节数
    print("教材大纲生成完成！")
    print(f"确定教材标题是：{textbook_title}")
    print(f"确定教材一共有{len(chapter_structure)}个章节")

    # 第三步：生成教材正文
    print("正在生成教材正文...")
    textbook_content = f"# {textbook_title}\n\n{textbook_abstract}\n\n"  # 包含摘要
    for i, chapter in enumerate(chapter_structure, 1):
        print(f"正在生成第 {i}/{len(chapter_structure)} 章：《{chapter['title']}》")
        chapter_content = generate_chapter_content(
            api_key, 
            f"第{i}章 {chapter['title']}", 
            chapter.get('content', ''), 
            base_url,  # 修正：base_url应该在第四个位置
            model,  # 修正：model应该在第五个位置
            f"{customization_prompt}。输出语言：{output_language}",  # 修正：customization_prompt应该在第六个位置
            stream  # 修正：stream应该在最后一个位置
        )
        if chapter_content:
            textbook_content += chapter_content + "\n\n"
            print(f"第 {i} 章生成完成！")
        else:
            print(f"第 {i} 章生成失败，跳过该章节。")
            textbook_content += f"# 第{i}章 {chapter['title']}\n\n[未能生成本章内容]\n\n"

    # 第四步：生成结论
    print("正在生成教材结论...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一个专业的教材编写助手"},
                {"role": "user", "content": f"请为以下教材生成结论{customization_prompt}，输出语言：{output_language}。要求：\n1. 总结全书核心内容\n2. 展望未来发展方向\n3. 生成两段，不要出现分条罗列\n\n教材内容：\n{textbook_content}"}
            ],
            temperature=0.7,
            max_tokens=800
        )
        conclusion = response.choices[0].message.content
        print("教材结论生成完成！")
    except Exception as e:
        print(f"生成结论失败：{str(e)}")
        conclusion = "## Conclusion\n\n[Failed to generate conclusion]"

    # 添加Conclusion到教材内容
    textbook_content += f"## Conclusion\n\n{conclusion}\n"

    # 保存生成的教材
    print("正在保存生成的教材...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(textbook_content)

    print(f"教材生成完成，已保存至：{output_file}")




