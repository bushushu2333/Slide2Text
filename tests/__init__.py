# 定义包的公共接口
from .test_customization import collect_customization_requirements
from .test_ppt_processor import extract_ppt_content, save_structured_data
from .test_textbook_generator import (
    generate_chapter_structure,
    generate_chapter_content,
    generate_textbook_from_ppt
)

# 定义包的版本信息
__version__ = "1.0.0"

# 定义包的描述信息
__description__ = "智能个性化教材生成系统"

# 定义包的作者信息
__author__ = "Zhou Yizhou"
__email__ = "zhouyizhou25@stu.ecnu.edu.cn"

# 可选：包初始化时执行的代码
def _initialize():
    print(f"Initializing {__name__} version {__version__}")

# 在包加载时执行初始化
_initialize()