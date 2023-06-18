# `proofread`

The `proofread` tool takes a text as input and provides a corrected version of it, if needed, along with an explanation of the corrections.

<!-- TOC -->
## Table of Contents

1. [Installation](#installation)
1. [Usage](#usage)
    1. [Improve the Quality of the Response](#improve-the-quality-of-the-response)
    1. [Spell Checking a Word](#spell-checking-a-word)
    1. [Changing the Language of the Response](#changing-the-language-of-the-response)
<!-- /TOC -->

## Installation

LLM-Toolbox needs to be installed. You can find [the detailed installation and configuration process on the main page of the repo](https://github.com/sderev/llm-toolbox).

You can install it with `pip` or `pipx` depending on your preferences:

* `pip`

    ```bash                                                                python3 -m pip install llm-toolbox
    ```
* `pipx`

    ```bash
    pipx install llm-toolbox
    ```

## Usage

You can pass arguments as the following:

```bash
proofread "Him and me are going to the store."
```

![proofread_english_1](https://github.com/sderev/llm-toolbox/assets/24412384/74e14a66-748f-4334-b1b4-cb511c80287c)

Or via `stdin` by using a pipe:

```bash
cat my_article.txt | proofread
```

### Improve the Quality of the Response

Sometimes, the response is not very good, especially for short sentences. If this is the case, you might want to add `-4` to call `gpt-4` to the rescue—but at a higher cost.

```bash
proofread "This have a mistake" -4
```

That last example might pose a problem to `gpt-3.5-turbo`, but `gpt-4` will answer appropriately.

### Spell Checking a Word

The `proofread` tool is designed to review and correct complete sentences to understand the context and provide the best suggestions. Thus, at times, `proofread` might complain that you didn't give it a complete sentence. If that happens, you can still accomplish your goal with a slight modification to your instruction. For example:

**Complaining**:

```
% proofread mispell
I'm sorry, but you have not provided any text or sentence to review and correct. Please provide me with the text or sentence so that I can assist you.
```
**Success**:

```
% proofread "Just the word: mispell"
Correction: misspell.

Reason: The word "misspell" is spelled with double "s", not "i". The correct spelling of the word means to spell a word incorrectly.
```

### Changing the Language of the Response

`proofread` will typically respond in the same language as the provided text. However, there may be occasions when it fails to do so, displaying the corrections in English instead. Alternatively, you might want to ensure that it always responds in a specific language.

In such case, you can modify the script and include a statement like this in the prompt: "Respond in French".

![proofread_french](https://github.com/sderev/llm-toolbox/assets/24412384/3bd02d3e-e8ce-4756-a3e1-b4a55475226c)
