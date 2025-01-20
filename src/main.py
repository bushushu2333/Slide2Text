import os
from ppt_processor import extract_ppt_content, save_structured_data
from customization import collect_customization_requirements
from textbook_generator import generate_textbook_from_ppt
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

def show_main_menu():
    print("""
    ============================
    智能教材生成系统 - 主菜单
    ============================
    1. 提取PPT内容
    2. 生成定制化教材
    3. 退出
    ============================
    """)

def process_ppt():
    """处理PPT文件，提取内容并保存为结构化数据"""
    ppt_file = input("请输入PPT文件路径：")
    output_dir = "output"
    output_file = os.path.join(output_dir, "structured_data.json")
    
    print("\n正在提取PPT内容...")
    structured_data = extract_ppt_content(ppt_file, output_dir)
    save_structured_data(structured_data, output_file)
    print(f"\n处理完成，结果已保存至：{output_file}")

def generate_textbook():
    """生成教材的主流程"""
    # 收集定制化需求
    customization_prompt, output_language = collect_customization_requirements()
    
    # 设置结构化数据文件路径
    structured_data_file = os.path.join("output", "structured_data.json")
    if not os.path.exists(structured_data_file):
        print(f"错误：未找到结构化数据文件 {structured_data_file}")
        print("请先执行PPT内容提取（主菜单选项1）")
        return
    

    # 模型选择
    print("\n请选择语言模型：")
    print("1. ChatGPT-4o (推荐)")
    print("2. DeepSeek")
    print("3. 其他自定义模型")
    model_choice = input("请选择（1-3）：")
    
    # 从环境变量读取配置
    if model_choice == "1":
        api_key = os.environ.get("GPT_API_KEY")
        base_url = os.environ.get("GPT_BASE_URL")
        model = "gpt-4o"
    elif model_choice == "2":
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        base_url = os.environ.get("DEEPSEEK_BASE_URL")
        model = "deepseek-chat"
    elif model_choice == "3":
        api_key = input("请输入API密钥：")
        base_url = input("请输入API基础URL：")
        model = input("请输入模型名称：")
    else:
        print("无效选择，将使用ChatGPT-4o默认配置")
        api_key = os.environ.get("GPT4_API_KEY")
        base_url = os.environ.get("GPT4_BASE_URL")
        model = "gpt-4o"
    
    # 设置输出文件名
    default_filename = "output_textbook.md"
    output_file = input(f"请输入输出教材文件名（默认：{default_filename}）：") or default_filename
    
    # 自动添加.md后缀
    if not output_file.lower().endswith('.md'):
        output_file += '.md'
    
    output_file = os.path.join("output", output_file)
    
    print(f"\n教材将保存至：{output_file}")
    
    # 确认需求
    while True:
        confirm = input("\n是否确认所有需求并开始生成教材？(是/否)：").strip().lower()
        if confirm in ['是', 'y', 'yes']:
            break
        elif confirm in ['否', 'n', 'no']:
            additional_requirements = input("还有什么要求？（按回车跳过）：")
            if additional_requirements:
                customization_prompt += f"。{additional_requirements}"
            print("\n更新后的定制化需求：")
            print(customization_prompt)
        else:
            print("请输入'是'或'否'")


    print("\n正在生成教材...")
    try:
        generate_textbook_from_ppt(
            api_key=api_key,
            structured_data_file=structured_data_file,
            output_file=output_file,
            output_language=output_language,
            customization_prompt=customization_prompt,
            base_url=base_url,
            model=model
        )
    except Exception as e:
        print(f"\n错误：生成教材时发生错误 - {str(e)}")
        # 让Python的默认错误处理机制工作
        raise

# 定义退出时的提示信息
EXIT_MESSAGE = """
感谢使用！

温馨提示：
1. 大模型生成的内容不一定完全准确，请在使用的过程中保持质疑精神
2. 如果对生成结果不满意，可以：
   - 重新生成内容
   - 在定制需求中明确指出不满意的地方
   - 详细描述您期待的内容类型
3. 我们持续改进系统，欢迎反馈使用体验
"""

def main():
    """主程序入口"""
    while True:
        show_main_menu()
        choice = input("请选择操作（1-3）：")
        
        if choice == "1":
            process_ppt()
        elif choice == "2":
            generate_textbook()
        elif choice == "3":
            print(EXIT_MESSAGE)
            break
        else:
            print("无效选择，请输入1-3之间的数字")
        
        input("\n按回车键返回主菜单...")

if __name__ == "__main__":
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    main()