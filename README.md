# LLM-Toolbox

**Development Notice**: Please note that the LLM-Toolbox is currently in active development. This means you can expect frequent updates, changes, and additions as I continue to refine and expand the toolset. I encourage you to stay updated with the latest features and fixes. Your feedback is also invaluable for this development process, so please don't hesitate to share your thoughts and experiences. If you find this project useful, please consider giving it a star to show your support ⭐😊.

---

LLM-Toolbox is a collection of command-line tools that harness the power of large language models to perform various tasks. This repository houses tools that utilize OpenAI's ChatGPT for tasks such as automatic commit messages, dictionary and thesaurus queries, text translation, proofreading, enriching language learning, automating shell commands, and more.

Additionally, the toolbox provides a selection of [prompt templates](#prompt-templates) to help you get the most out of your interactions with the language models. Whether you're new to using language models and CLI or an experienced developer, these tools and templates can serve as an invaluable resource.

Given the wide-ranging capabilities of the LLM-Toolbox, it can be helpful to see it in action first. Therefore, I strongly suggest you check out the video demos of the tools to gain a hands-on understanding of their potential. After viewing the demos, you can return here for a deeper dive into the specific applications and benefits. So, go ahead, watch the demos! 😊

<!-- TOC -->
## Table of Contents

1. [Prompt Templates](#prompt-templates)
1. [Isn't the OpenAI API expensive?](#isnt-the-openai-api-expensive)
1. [The Value of Investing in LLM-Toolbox](#the-value-of-investing-in-llm-toolbox)
    1. [Is GPT-3.5 Sufficient for Those Tools?](#is-gpt-35-sufficient-for-those-tools)
    1. [Current Costs](#current-costs)
1. [Installation](#installation)
    1. [pip](#pip)
    1. [`pipx`, the Easy Way](#pipx-the-easy-way)
    1. [Installing the LLM-Toolbox](#installing-the-llm-toolbox)
    1. [Cloning the LLM-Toolbox Repository](#cloning-the-llm-toolbox-repository)
1. [Getting Started](#getting-started)
    1. [Set your OpenAI API key](#set-your-openai-api-key)
1. [Tools](#tools)
    1. [ShellGenius](#shellgenius)
    1. [Commitgen](#commitgen)
    1. [VocabMaster](#vocabmaster)
    1. [Thesaurus](#thesaurus)
    1. [Define](#define)
    1. [Proofread](#proofread)
    1. [Translate](#translate)
1. [Prompt Templates](#prompt-templates)
1. [License](#license)
<!-- /TOC -->

## Prompt Templates

If you're not a terminal-centric person, or if you prefer the web interface anyway, note that I prepared [templates for ChatGPT web interface](https://github.com/sderev/llm-toolbox/prompt-templates).

It's better to use the web interface if you plan on having very long chat interactions with GPT-4 (requires a ChatGPT Plus subscription, though). Otherwise it will cost you too much.

## Isn't the OpenAI API expensive?

A lot of people are afraid that these tools will cost them too much. But the truth is, as long as you're not sending too many requests to GPT-4, you won't have exorbitant bills. On the contrary, this may surprise you, but I'm pretty confident that the majority of people won't exceed a cost of $3 to $5 per month, as long as they continue to use GPT-3.5, even if they use these tools more than a hundred times a day.

Also, there's a safeguard: **you can configure a soft and a hard usage limit on your OpenAI account**. This ensures that you won't ever be taken by surprise.

* Soft limit: You receive a notification email.
* Hard limit: Subsequent requests will be rejected.

## The Value of Investing in LLM-Toolbox

Well... in giving your money to OpenAI, actually.

Even if you have a monthly expense of more than a dollar, it's well worth looking at the huge benefits you'll receive from utilizing the tools in the LLM-Toolbox. These innovative solutions provide users with powerful capabilities that can **significantly streamline tasks, improve productivity, and foster creativity**.

Particularly, let's consider [ShellGenius](#shellgenius), a remarkable tool within the LLM-Toolbox. It enhances the command-line experience by translating task descriptions into efficient shell commands, a feat that not only saves time but also reduces the possibility of human error. This tool is extremely beneficial for both beginners, who may not be fluent in shell commands, and experienced users who can streamline their command-line tasks by simply describing what they wish to accomplish.

Therefore, when considering the cost, it's essential to look beyond the immediate dollar value and evaluate the considerable time, effort, and resources you stand to save. The utility and value derived from such tools often outweigh the minimal monthly cost. The price of these tools should not be a deterrent but rather seen as an investment in enhancing your efficiency and productivity.

Also, try to ask for an API key at your workplace.

### Is GPT-3.5 Sufficient for Those Tools?

GPT-3.5 is an excellent model for these tools, offering a cost-effective solution that consistently delivers appropriate responses. I take great care in crafting my prompts and the tools to generate the best results that cater to my own daily needs.

I will continue refining them, if necessary, as time goes on. So stay tuned to this repo and consider giving it a star ⭐!

You'll also be able to update the LLM-Toolbox directly from the CLI 😊.

### Current Costs

At the time of writing (2023-06-17T13:35:56+02:00), these are the costs:

| Model            | Prompt Cost   | Response Cost   |
|------------------|--------------:|----------------:|
| gpt-3.5-turbo    | $0.0015 / 1K  | $0.002 / 1K     |
| gpt-3.5-turbo-16k| $0.003 / 1K   | $0.004 / 1K     |
| gpt-4            | $0.03 / 1K    | $0.06 / 1K      |
| gpt-4-32k        | $0.06 / 1K    | $0.12 / 1K      |

## Installation

### pip

```bash
python3 -m pip install llm-toolbox
```

### `pipx`, the Easy Way

To use these tools, I recommend that you first install [pipx](https://pypa.github.io/pipx/installation/). It's a package manager for Python that makes the installation and upgrade of CLI apps easy (no more hassle with virtual environment 😌).

* Debian / Ubuntu

    ```bash
    sudo apt install pipx
    ```

* macOS    

    ```bash
    brew install pipx
    ```

### Installing the LLM-Toolbox

To install the latest stable version of the LLM-Toolbox, simply run this command:

```bash
pipx install llm-toolbox
```

If you want to follow the `main` branch:

```bash
pipx install git+https://github.com/sderev/llm-toolbox
```

To upgrade it:

```bash
pipx upgrade llm-toolbox
```

### Cloning the LLM-Toolbox Repository

You can clone this repository with the following command:

```bash
git clone https://github.com/sderev/llm-toolbox.git
```

## Getting Started

### Set your OpenAI API key

LLM-Toolbox requires an OpenAI API key to function. You can obtain a key by signing up for an account at [OpenAI's website](https://platform.openai.com/account/api-keys).

You need to set some usage limit before to be able to use the API. You can configure on your OpenAI account in *Billing -> Usage limits*.

Once you have your API key, set it as an environment variable:

* On macOS and Linux:

  ```bash
  export OPENAI_API_KEY="your-api-key-here"
  ```

  To avoid having to type it everyday, you can create a file with the key:

  ```bash
  echo "your-api-key" > ~/.openai-api-key.txt
  ```

  **Note:** Remember to replace `"your-api-key"` with your actual API key.

  And then, you can add this to your shell configuration file (`.bashrc`, `.zshrc`, etc.):

    ```bash
    export OPENAI_API_KEY="$(cat ~/.openai-api-key.txt)"
    ```

* On Windows:

  ```
  setx OPENAI_API_KEY your_key
  ```

## Tools

Instructions on how to use each of the tools are included in the individual directories under [tools/](https://github.com/sderev/llm-toolbox/tree/main/tools). This is also where I give some tricks and tips on their usage 💡👀💭.

Here's a brief overview:

### ShellGenius

[ShellGenius](https://github.com/sderev/shellgenius) is an intuitive CLI tool designed to enhance your command-line experience by turning your task descriptions into efficient shell commands. Check out the project on [its dedicated repository](https://github.com/sderev/shellgenius).

![shellgenius](https://github.com/sderev/llm-toolbox/assets/24412384/688d9a1a-f351-42d0-9f4d-06a9a6d1909a)

### Commitgen

The [`commitgen`](https://github.com/sderev/llm-toolbox/tree/main/tools/commitgen) tool is designed to streamline your `git` workflow by automatically generating meaningful commit messages for your code changes.

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/d41985d5-d8a2-4622-9ef7-643176cdc741)
___

### VocabMaster

Master new languages with [VocabMaster](https://github.com/sderev/vocabmaster), a CLI tool designed to help you record vocabulary, access translations and examples, and seamlessly import them into Anki for an optimized language learning experience. Check out the project on [its dedicated repository](https://github.com/sderev/vocabmaster).

![vocabmaster_translate_japanese](https://github.com/sderev/llm-toolbox/assets/24412384/5f5612fe-f1fb-4d4c-bb25-68f07961e66b)

___

### Thesaurus

The [`thesaurus`](https://github.com/sderev/llm-toolbox/tree/main/tools/thesaurus) tool takes a word or a phrase as input and provides a list of synonyms and antonyms.

![thesaurus](https://github.com/sderev/llm-toolbox/assets/24412384/dca6bf42-2545-4b56-bb20-4c8e6c872529)

___

### Define

The [`define`](https://github.com/sderev/llm-toolbox/tree/main/tools/define) tool takes a word as input and provides its definition along with an example sentence using the word.

![define](https://github.com/sderev/llm-toolbox/assets/24412384/1e813b80-6896-483b-b31a-65ad7cb81173)

___

### Proofread

The [`proofread`](https://github.com/sderev/llm-toolbox/tree/main/tools/proofread) tool takes a sentence as input and provides a corrected version of it, if needed, along with an explanation of the corrections.

![proofread_english](https://github.com/sderev/llm-toolbox/assets/24412384/e84ce7cd-68e9-4d6d-8c56-55b93c7e4fee)

___

### Translate

The [`translate`](https://github.com/sderev/llm-toolbox/tree/main/tools/translate) tool takes a sentence and a target language as input and provides the translated sentence in the target language.

![translate](https://github.com/sderev/llm-toolbox/assets/24412384/505237c9-7735-4db6-aa4a-63c3ed2867a7)

## Prompt Templates

In addition to the various tools provided, the LLM-Toolbox includes a collection of prompt templates in the [`prompts/`](https://github.com/sderev/llm-toolbox/tree/main/prompts) directory. These templates cover a wide range of scenarios and are designed to optimize your interaction with language models. They are an excellent starting point if you're not sure how to structure your prompts or if you're seeking to improve the effectiveness of your current prompts.

Please feel free to explore these templates and adapt them to suit your specific needs.

## License

This project is licensed under the terms of the Apache License 2.0.

