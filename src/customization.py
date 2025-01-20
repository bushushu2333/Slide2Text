def collect_customization_requirements():
    """
    通过一轮对话收集用户的定制化需求，并将其转换为适合模型理解的 Prompt 格式
    :return: 包含定制化要求的字符串和输出语言
    """
    print("请提供以下定制化需求（按回车跳过使用默认值）：")

    # 收集语言风格
    language_style = input("1. 语言风格（例如：专业学术、通俗易懂、简洁明了）：") or "专业学术"

    # 收集章节长度
    chapter_length = input(
        "2. 章节长度（例如：较短[约1000字]、中等[约3000字]、较长[约5000字]）："
    ) or "中等"

    # 是否包含练习题
    include_exercises = input("3. 是否包含练习题？（是/否）：").strip().lower()
    include_exercises = "是" if include_exercises in ["是", "y", "yes"] else "否"

    # 目标读者群体
    target_audience = input("4. 目标读者群体（例如：本科生、研究生、初学者）：") or "本科生"

    # 输出语言
    output_language = input("5. 输出语言（例如：中文、英文、日语）：") or "中文"

    # 其他要求
    additional_requirements = input("6. 其他要求（例如：增加案例分析、添加图表说明等）：") or "无"

    # 将需求整合为 Prompt 格式
    prompt_addition = []
    prompt_addition.append(f"语言风格：{language_style}")
    prompt_addition.append(f"章节长度：{chapter_length}")
    prompt_addition.append(f"包含练习题：{include_exercises}")
    prompt_addition.append(f"目标读者：{target_audience}")
    prompt_addition.append(f"输出语言：{output_language}")
    prompt_addition.append(f"其他要求：{additional_requirements}")

    # 返回整合后的 Prompt 和语言信息
    return "。定制化要求：" + "，".join(prompt_addition), output_language




