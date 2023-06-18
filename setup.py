from setuptools import setup, find_packages
from pathlib import Path

VERSION = "0.0.1"


def read_requirements():
    with open("requirements.txt") as file:
        return list(file)


def get_long_description():
    with open("README.md", encoding="utf8") as file:
        return file.read()


setup(
    name="LLM-Toolbox",
    description="A versatile collection of CLI tools leveraging large language models",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Sébastien De Revière",
    url="https://github.com/sderev/llm-toolbox",
    project_urls={
        "Documentation": "https://github.com/sderev/llm-toolbox",
        "Issues": "http://github.com/sderev/llm-toolbox/issues",
        "Changelog": "https://github.com/sderev/llm-toolbox/releases",
    },
    license="Apache Licence, Version 2.0",
    version="0.0.1",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "llm-toolbox=llm_toolbox.cli:cli",
            "thesaurus=llm_toolbox.cli:thesaurus",
            "llm=llm.cli:cli",
            "translate=llm_toolbox.cli:translate",
            "define=llm_toolbox.cli:define",
            "proofread=llm_toolbox.cli:proofread",
            "lessonize=llm_toolbox.cli:lessonize",
            "commitgen=llm_toolbox.cli:commitgen",
            "codereview=llm_toolbox.cli:codereview",
            "summarize=llm_toolbox.cli:summarize",
            "critique=llm_toolbox.cli:critique",
            "pathlearner=llm_toolbox.cli:pathlearner",
            "explain=llm_toolbox.cli:explain",
            "cheermeup=llm_toolbox.cli:cheermeup",
            "shellgenius=shellgenius.cli:shellgenius",
            "study=llm_toolbox.cli:study",
            "teachlib=llm_toolbox.cli:teachlib",
            "vocabmaster=vocabmaster.cli:vocabmaster",
        ]
    },
    python_requires=">=3.8",
)
