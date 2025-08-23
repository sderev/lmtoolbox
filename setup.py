from setuptools import setup, find_packages

VERSION = "0.5.16"


def read_requirements():
    """
    Read requirements from requirements.txt.
    """
    with open("requirements.txt", encoding="UTF-8") as file:
        return list(file)


def get_long_description():
    """
    Read the README.md file.
    """
    with open("README.md", encoding="UTF8") as file:
        return file.read()


setup(
    name="LMtoolbox",
    description="A collection of CLI tools leveraging language models",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Sébastien De Revière",
    url="https://github.com/sderev/lmtoolbox",
    project_urls={
        "Documentation": "https://github.com/sderev/lmtoolbox",
        "Issues": "http://github.com/sderev/lmtoolbox/issues",
        "Changelog": "https://github.com/sderev/lmtoolbox/releases",
    },
    license="Apache Licence, Version 2.0",
    version=VERSION,
    packages=find_packages(),
    package_data={
        "lmtoolbox": ["tools/templates/*.yaml"],
    },
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "cheermeup=lmtoolbox.cli:cheermeup",
            "codereview=lmtoolbox.cli:codereview",
            "commitgen=lmtoolbox.cli:commitgen",
            "critique=lmtoolbox.cli:critique",
            "define=lmtoolbox.cli:define",
            "explain=lmtoolbox.cli:explain",
            "lessonize=lmtoolbox.cli:lessonize",
            "life=lmtoolbox.cli:life",
            "lmtoolbox=lmtoolbox.cli:cli",
            "lmt=lmterminal.cli:lmt",
            "pathlearner=lmtoolbox.cli:pathlearner",
            "proofread=lmtoolbox.cli:proofread",
            "shellgenius=shellgenius.cli:shellgenius",
            "study=lmtoolbox.cli:study",
            "summarize=lmtoolbox.cli:summarize",
            "teachlib=lmtoolbox.cli:teachlib",
            "thesaurus=lmtoolbox.cli:thesaurus",
            "translate=lmtoolbox.cli:translate",
            "vocabmaster=vocabmaster.cli:vocabmaster",
        ]
    },
    python_requires=">=3.8",
)
