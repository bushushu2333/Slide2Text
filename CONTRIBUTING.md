# 参与贡献指南

感谢您对智能个性化教材生成系统的关注！本文档将指导您如何参与到项目的开发和改进中。作为一个专注于教育技术创新的开源项目，我们非常欢迎社区成员的贡献。

## 开发环境配置

在开始贡献代码之前，请确保您的开发环境满足以下要求：

### Python环境
确保您已安装Python 3.8或更高版本。您可以通过以下命令检查Python版本：
```bash
python --version
```

### 项目设置
1. 克隆项目代码：
```bash
git clone https://github.com/bushushu2333/Silde2Text.git
cd Silde2Text
```

2. 创建并激活虚拟环境：
```bash
# 创建虚拟环境
python -m venv venv

# Windows下激活
.\venv\Scripts\activate

# Linux/Mac下激活
source venv/bin/activate
```

3. 安装项目依赖：
```bash
pip install -r requirements.txt
```

### 环境变量配置
1. 复制环境变量模板文件：
```bash
cp .env.example .env
```

2. 在.env文件中填入必要的配置信息，包括：
- GPT_API_KEY
- GPT_BASE_URL
- DEEPSEEK_API_KEY
- DEEPSEEK_BASE_URL

## 开发流程

### 任务认领
1. 在开始开发之前，请先浏览项目的Issues页面
2. 找到您感兴趣的问题或功能
3. 如果是新功能，请先创建Issue讨论可行性
4. 在开始工作前，请在Issue下留言，表明您要处理这个任务

### 代码开发
1. 创建新的功能分支：
```bash
# 功能开发分支
git checkout -b feature/your-feature-name

# Bug修复分支
git checkout -b fix/bug-description
```

2. 开发时请注意：
- 遵循项目的代码风格指南
- 添加必要的注释和文档
- 编写对应的单元测试
- 保证代码的可读性和可维护性

3. 测试您的代码：
```bash
python -m pytest tests/
```

### 提交代码
1. 提交您的更改：
```bash
git add .
git commit -m "feat: add your feature description"
# 或
git commit -m "fix: fix the bug description"
```

2. 推送到远程仓库：
```bash
git push origin feature/your-feature-name
```

3. 创建Pull Request：
- 使用清晰的标题和描述
- 关联相关的Issue
- 等待维护者的审查和反馈

## 代码风格指南

我们遵循Python PEP 8风格指南，并有以下特定要求：

### 命名规范
1. 类名使用大驼峰命名法（PascalCase）
2. 函数和变量使用小写字母加下划线（snake_case）
3. 常量使用全大写字母加下划线
4. 私有方法和变量以单下划线开头

### 文档规范
所有的公共函数都需要docstring，使用Google风格：

```python
def process_ppt(file_path: str, output_dir: str) -> dict:
    """处理PPT文件并提取内容。

    详细说明这个函数的功能、处理逻辑和注意事项。

    Args:
        file_path: PPT文件的路径
        output_dir: 输出目录的路径

    Returns:
        包含处理结果的字典

    Raises:
        FileNotFoundError: 当PPT文件不存在时
        ValueError: 当参数格式不正确时
    """
    pass
```

### 代码结构
1. 相关的功能放在同一个模块中
2. 每个函数保持单一职责
3. 函数长度建议不超过50行
4. 模块导入顺序：标准库、第三方库、本地模块

## 问题反馈

### 问题报告
如果您发现了bug或有新的建议，请：

1. 在GitHub Issues中创建新的issue
2. 使用适当的标签（bug, enhancement, question等）
3. 提供详细的问题描述
4. 对于bug，请提供：
   - 复现步骤
   - 期望行为
   - 实际行为
   - 环境信息

### 联系方式
- GitHub Issues: [https://github.com/bushushu2333/Silde2Text/issues](https://github.com/bushushu2333/Silde2Text/issues)
- 电子邮件: zhouyizhou25@stu.ecnu.edu.cn （邮件主题请以[Silde2Text]开头）

## 其他贡献方式

除了代码贡献，您还可以通过以下方式参与项目：

### 文档改进
1. 修正文档中的错误
2. 添加使用示例和教程
3. 完善API文档
4. 翻译文档

### 社区推广
1. 在社交媒体上分享项目
2. 撰写项目相关的博客文章
3. 在技术会议上介绍项目

### 使用反馈
1. 分享您的使用案例
2. 提供改进建议
3. 反馈性能问题

感谢您为项目做出的贡献！
