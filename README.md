# LLM-Toolbox

LLM-Toolbox is a collection of command line tools that harness the power of large language models to perform various tasks. This repository houses scripts and tools that utilize OpenAI's ChatGPT for tasks such as dictionary and thesaurus queries, text translation, proofreading, enriching language learning, automating shell commands, and more.

Additionally, the toolbox provides a selection of prompt templates to help you get the most out of your interactions with the language models. Whether you're new to scripting with language models or an experienced developer, these templates can serve as an invaluable resource.

<!-- TOC -->
## Table of Contents

1. [Installation](#installation)
    1. [Install `llm` with `pipx`](#install-llm-with-pipx)
    1. [Cloning the LLM-Toolbox Repository](#cloning-the-llm-toolbox-repository)
1. [Tools](#tools)
    1. [ShellGenius](#shellgenius)
    1. [Vocabmaster](#vocabmaster)
    1. [Thesaurus](#thesaurus)
    1. [Define](#define)
    1. [Proofread](#proofread)
    1. [Translate](#translate)
1. [Prompt Templates](#prompt-templates)
1. [License](#license)
<!-- /TOC -->

## Installation

To use these scripts, you need to clone this repository and ensure you have installed all necessary dependencies.

For some of the scripts, you'll need to install `llm`. You can find [its repository here](https://github.com/simonw/llm). Follow the instructions in its README for the official installation details and documentation.

### Install `llm` with `pipx`

I recommend using [pipx](https://pypa.github.io/pipx/installation/) for the installation of `llm`.

You can either install the latest stable version:

```bash
pipx install llm
```

Or install from the GitHub repository to follow its main branch:

```bash
pipx install git+https://github.com/simonw/llm.git
```

### Cloning the LLM-Toolbox Repository

You can clone this repository with the following command:

```bash
git clone https://github.com/sderev/llm-toolbox.git
```

## Tools

Instructions on how to use each of the scripts and tools are included in the individual directories under [tools/](https://github.com/sderev/llm-toolbox/tree/main/tools). Here's a brief overview:

### ShellGenius

[ShellGenius](https://github.com/sderev/shellgenius) is an intuitive CLI tool designed to enhance your command-line experience by turning your task descriptions into efficient shell commands. Check out the project on [its dedicated repository](https://github.com/sderev/shellgenius).

![shellgenius](https://github.com/sderev/llm-toolbox/assets/24412384/688d9a1a-f351-42d0-9f4d-06a9a6d1909a)

___

### Vocabmaster

Master new languages with [VocabMaster](https://github.com/sderev/vocabmaster), a CLI tool designed to help you record vocabulary, access translations and examples, and seamlessly import them into Anki for an optimized language learning experience. Check out the project on [its dedicated repository](https://github.com/sderev/vocabmaster).

![vocabmaster_translate_japanese](https://github.com/sderev/llm-toolbox/assets/24412384/5f5612fe-f1fb-4d4c-bb25-68f07961e66b)

___

### Thesaurus

The [`thesaurus`](https://github.com/sderev/llm-toolbox/tree/main/tools/thesaurus) script takes a word or a phrase as input and provides a list of synonyms and antonyms.

![thesaurus](https://github.com/sderev/llm-toolbox/assets/24412384/dca6bf42-2545-4b56-bb20-4c8e6c872529)

___

### Define

The [`define`](https://github.com/sderev/llm-toolbox/tree/main/tools/define) script takes a word as input and provides its definition along with an example sentence using the word.

![define](https://github.com/sderev/llm-toolbox/assets/24412384/1e813b80-6896-483b-b31a-65ad7cb81173)

___

### Proofread

The [`proofread`](https://github.com/sderev/llm-toolbox/tree/main/tools/proofread) script takes a sentence as input and provides a corrected version of it, if needed, along with an explanation of the corrections.

![proofread_english](https://github.com/sderev/llm-toolbox/assets/24412384/e84ce7cd-68e9-4d6d-8c56-55b93c7e4fee)

___

### Translate

The [`translate`](https://github.com/sderev/llm-toolbox/tree/main/tools/translate) script takes a sentence and a target language as input and provides the translated sentence in the target language.

![translate](https://github.com/sderev/llm-toolbox/assets/24412384/505237c9-7735-4db6-aa4a-63c3ed2867a7)

## Prompt Templates

In addition to the various tools provided, the LLM-Toolbox includes a collection of prompt templates in the [`prompts/`](https://github.com/sderev/llm-toolbox/tree/main/prompts) directory. These templates cover a wide range of scenarios and are designed to optimize your interaction with language models. They are an excellent starting point if you're not sure how to structure your prompts or if you're seeking to improve the effectiveness of your current prompts.

Please feel free to explore these templates and adapt them to suit your specific needs.

## License

This project is licensed under the terms of the Apache License 2.0.

