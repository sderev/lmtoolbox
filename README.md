# LLM-Toolbox

**Development Status**: 

LLM-Toolbox is currently under active development. Your feedback is crucial for this ongoing journey of refinement. Please share your thoughts, experiences, and suggestions. If you find this project beneficial, consider expression your support by giving it a star ⭐😊.

---

LLM-Toolbox is an ensemble of AI-powered command-line tools designed to modernize your workflow in the terminal. Built using OpenAI's ChatGPT, the tools in this toolbox can generate automatic commit messages, perform dictionary and thesaurus queries, translate text, proofread content, enrich language learning, and automate shell commands, among others.

Additionally, the toolbox provides an array of [prompt templates](#prompt-templates) that can serve as a valuable resource, whether you're new to using languages models or you're an experienced user.

I've created video demos to help you see the LLM-Toolbox in action and understand its wide-ranging capabilities. Therefore, I strongly recommend you check out the video demos of the tools to gain a hands-on understanding of their potential. After watching the demos, you can return here for a deeper dive into the specific applications and benefits. So, go ahead, watch the demos! 😊

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
    1. [Configuring your OpenAI API key](#configuring-your-openai-api-key)
1. [Tools](#tools)
    1. [LMT](#lmt)
    1. [ShellGenius](#shellgenius)
    1. [Commitgen](#commitgen)
    1. [Codereview](#codereview)
    1. [VocabMaster](#vocabmaster)
    1. [Thesaurus](#thesaurus)
    1. [Define](#define)
    1. [Proofread](#proofread)
    1. [Translate](#translate)
    1. [Cheermeup](#cheermeup)
    1. [Critique](#critique)
    1. [Explain](#explain)
    1. [Lessonize](#lessonize)
    1. [Life](#life)
    1. [Pathlearner](#pathlearner)
    1. [Study](#study)
    1. [Summarize](#summarize)
    1. [Teachlib](#teachlib)
1. [License](#license)
<!-- /TOC -->

## Prompt Templates 

For those less experienced with terminal interfaces or those preferring the convenience of a web interface, the [ChatGPT web interface templates](https://github.com/sderev/llm-toolbox/tree/main/prompt-templates) in the LLM-Toolbox can prove incredibly useful. These templates offer a broad spectrum of pre-structured prompts designed to enhance your engagement with ChatGPT, particularly in the context of longer chat interactions with GPT-4 in order to avoid expensive API costs.

These templates, found in the [`prompt-templates/`](https://github.com/sderev/llm-toolbox/tree/main/prompt-templates) directory, cater to various situations and are an excellent resource if you're uncertain about structuring prompts or seek to improve the effectiveness of your existing ones.

Feel free to explore these templates and adjust them to better suit your individual needs.

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

### Is GPT-3.5 Sufficient for Those Tools?

GPT-3.5 is an excellent model for these tools, offering a cost-effective solution that consistently delivers appropriate responses. I take great care in crafting my prompts and the tools to generate the best results that cater to my own daily needs.

I will continue refining them, if necessary, as time goes on. So stay tuned to this repo and consider giving it a star! ⭐

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

To use these tools, I recommend that you first install [pipx](https://pypa.github.io/pipx/installation/). It's a package manager for Python that makes the installation and upgrade of CLI apps easy (no more hassle with virtual environments 😌).

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

### Configuring your OpenAI API key

For LLM-Toolbox to work properly, it is necessary to acquire and configure an OpenAI API key. Follow these steps to accomplish this:

1. **Acquire the OpenAI API key**: You can do this by creating an account on the [OpenAI website](https://platform.openai.com/account/api-keys). Once registered, you will have access to your unique API key.

2. **Set usage limit**: Before you start using the API, you need to define a usage limit. You can configure this in your OpenAI account settings by navigating to *Billing -> Usage limits*.

3. **Configure the OpenAI API key**: Once you have your API key, you can set it up by running the `lmt key set` command.

    ```bash
    lmt key set
    ```

With these steps, you should now have successfully set up your OpenAI API key, ready for use with the LLM-Toolbox.

## Tools

Instructions on how to use each of the tools are included in the individual directories under [tools/](https://github.com/sderev/llm-toolbox/tree/main/tools). This is also where I give some tricks and tips on their usage 💡👀💭.

Note that LMT is the main tool in the LLM-Toolbox. All of its options apply to (almost) all of the other tools. For instance, you change the model to GPT-4 with `-m 4` or add emojis with `--emoji`. Refer to the [LMT's documentation](https://github.com/sderev/lmt) for more information. 

* **Reading from `stdin`**: Almost all of the tools can read from `stdin`. For instance: `cat my_text.md | summarize`.

* **Output Redirection**: You can use output redirections with the tools. For instance: `cat my_text.md | critique --raw > critique_of_my_text.md`

Here's a brief overview of the tools:

### LMT

[LMT](https://github.com/sderev/lmt) empowers you to interact directly with ChatGPT from the comfort of your terminal. One of the core features of `lmt` is its ability to facilitate the creation of custom templates, enabling you to design your personalized toolbox of CLI applications. You can easily install its standalone version from [the project's repository](https://github.com/sderev/lmt).

![cioran](https://github.com/sderev/llm-toolbox/assets/24412384/c1a7d7f2-1edb-425d-bd8c-2a813be9d088)

___

### ShellGenius

[ShellGenius](https://github.com/sderev/shellgenius) is an intuitive CLI tool designed to enhance your command-line experience by turning your task descriptions into efficient shell commands. Check out the project on [its dedicated repository](https://github.com/sderev/shellgenius).

![shellgenius](https://github.com/sderev/llm-toolbox/assets/24412384/688d9a1a-f351-42d0-9f4d-06a9a6d1909a)

___

### Commitgen

The [`commitgen`](https://github.com/sderev/llm-toolbox/tree/main/tools/commitgen) tool is designed to streamline your `git` workflow by automatically generating meaningful commit messages for your code changes.

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/37103ef6-7078-4b38-bdb6-bb4c9880ad3f)

___

### Codereview

The [`codereview`](https://github.com/sderev/llm-toolbox/tree/main/tools/codereview) tool accepts a file or a piece of text as input and provides an in-depth analysis of the code. It can identify potential issues, suggest improvements, and even detect security vulnerabilities. The Codereview tool is capable of handling a variety of programming languages, and its feedback can serve as an invaluable resource for developers seeking to enhance the quality of their code. 

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/6ee649e5-4e0f-4e59-8a36-a13080a2aa52)

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

___

### Cheermeup

The [`cheermeup`](https://github.com/sderev/llm-toolbox/tree/main/tools/cheermeup) tool is designed to uplift your spirits based on your current mood. Whether you're feeling down or just need a little pick-me-up, this tool uses a variety of methods to bring a smile to your face and brighten your day.

![ice_cream](https://github.com/sderev/llm-toolbox/assets/24412384/d9928f50-19fd-40a1-a862-697606a1c7c5)

___

### Critique

The [`critique`](https://github.com/sderev/llm-toolbox/tree/main/tools/critique) tool is your personal constructive text critic, designed to analyze a given piece of text and provide detailed, insightful feedback. It enables users to enhance their writing by addressing potential shortcomings and improving the overall quality.

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/e63186fe-ad22-400c-b98a-24ba9417a332)

___

### Explain

The [`explain`](https://github.com/sderev/llm-toolbox/tree/main/tools/explain) tool helps to clarify complex concepts. When given a concept, it presents a comprehensive and straightforward explanation, aiding in understanding and knowledge retention.

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/86c7d6b0-3ab3-4021-9355-638bd1eee956)

___

### Lessonize

The [`lessonize`](https://github.com/sderev/llm-toolbox/tree/main/tools/lessonize) tool transforms any piece of text into an informative lesson. Whether you're a teacher looking for instructional material or a student looking to further understand a subject, this tool makes learning more accessible.

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/c9945c67-a561-4666-9c74-a714a1d69b78)

___

### Life

The [`life`](https://github.com/sderev/llm-toolbox/tree/main/tools/life) tool offers a unique perspective on the passage of time, presenting thoughtful messages based on your life expectancy statistics. Whether you're seeking a novel way to reflect on your life journey or need a gentle reminder of the beauty and preciousness of life's uncertainty, this tool provides insightful outputs to provoke meaningful contemplation.

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/4f345485-d991-482f-b088-048dcf04b494)

___

### Pathlearner

The [`pathlearner`](https://github.com/sderev/llm-toolbox/tree/main/tools/pathlearner) tool provides a comprehensive study plan for a given topic. Whether you're studying for an exam or learning a new subject, this tool creates a structured, step-by-step plan that aids in understanding and mastering the material.

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/8e743ab9-ddff-4d77-bcac-b22afec40c79)

___

### Study

The [`study`](https://github.com/sderev/llm-toolbox/tree/main/tools/study) tool is a comprehensive guide that generates study material for a particular topic or content. It helps students to better prepare for exams, giving them access to tailored study material designed to enhance their learning experience.

![demo_0](https://github.com/sderev/llm-toolbox/assets/24412384/07192886-7203-4cf5-ae68-86783116fe3d)

___

### Summarize

The [`summarize`](https://github.com/sderev/llm-toolbox/tree/main/tools/summarize) tool provides succinct summaries of a web page, lengthy texts, or the content of given files. It's perfect for extracting key points and crucial information from vast amounts of data, saving users time and effort.

![wikipedia](https://github.com/sderev/llm-toolbox/assets/24412384/0c1988af-d11b-40c0-bf8a-de651315beb3)

___

### Teachlib

The [`teachlib`](https://github.com/sderev/llm-toolbox/tree/main/tools/teachlib) tool is designed to provide comprehensive lessons on various libraries. By simplifying complex aspects and focusing on the core functionalities, this tool helps users to understand and effectively utilize different libraries.

![numpy](https://github.com/sderev/llm-toolbox/assets/24412384/a85721e2-0be4-4b81-bfe3-8db5af560456)

___

## License

This project is licensed under the terms of the Apache License 2.0.

___

<https://github.com/sderev/llm-toolbox>
