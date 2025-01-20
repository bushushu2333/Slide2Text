from setuptools import setup, find_packages

# 从__init__.py中读取版本信息
from src import __version__, __description__, __author__, __email__

# 读取requirements.txt中的依赖
with open('src/requirements.txt', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='smart_textbook_generator',
    version=__version__,
    description=__description__,
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author=__author__,
    author_email=__email__,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'textbook-gen=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Education',
        'Topic :: Text Processing',
    ],
    keywords='textbook ppt ai education',
    project_urls={
        'Source': 'https://github.com/bushushu2333/Silde2Text',
        'Bug Reports': 'https://github.com/bushushu2333/Silde2Text/issues',
    },
)