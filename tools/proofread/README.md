# `proofread`

The `proofread` script takes a text as input and provides a corrected version of it, if needed, along with an explanation of the corrections.

<!-- TOC -->
## Table of Contents

1. [Prerequisites](#prerequisites)
1. [Installation](#installation)
    1. [Linux/macOS](#linuxmacos)
    1. [Windows](#windows)
1. [Usage](#usage)
<!-- /TOC -->

## Prerequisites

* `llm` needs to be installed. You can find it [here](https://github.com/simonw/llm). Follow the instructions in its README for installation details.

You can also check [the installation process I recommend](https://github.com/sderev/llm-toolbox#install-llm-with-pipx).

## Installation

To make the script globally available in your terminal, follow these steps:

### Linux/macOS

1. Move the script to `~/.local/bin` or a dedicated folder of your choice.
1. Open your shell configuration file (`.bashrc`, `.zshrc`, `.bash_profile`, or `.profile` depending on your system).
1. If you chose another folder than `~/.local/bin`, which should already be on your PATH, add the following line to your shell configuration file: `export PATH=$PATH:~/path/to/folder/of/your/choice` (match the directory you used in step 1).
1. Save the file and source your shell configuration file, or start a new shell session.

    ```bash
    source ~/path/to/folder
    ```

### Windows

For Windows users, if you use WSL, you're already covered with the previous instructions. If not, you'll need a Bash-like environment to run these scripts, such as Git Bash or Cygwin. 

You can choose a directory to store your scripts (for example, `C:\scripts`) and add this directory to your PATH:

1. Right-click on 'Computer' and choose 'Properties'.
1. Click on 'Advanced system settings'.
1. Click on 'Environment Variables'.
1. Under 'System Variables' find the PATH variable, select it, and click 'Edit'.
1. In the 'Variable value' field, add the path of the directory where you placed your scripts at the end, preceded by a semicolon (`;`). For example: `;C:\scripts`.
1. Click 'OK', 'OK', 'OK'. You may need to restart your session or even your computer for the changes to take effect (Windows magic 🪄).

## Usage

You can pass arguments as the following:

```bash
proofread "Him and me are going to the store."
```

![proofread_english_1](https://github.com/sderev/llm-toolbox/assets/24412384/d3ec4f50-1f1c-433e-b3d4-cbb7f51c91b3)


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

For more informations about the options like `-4`, you can run `llm --help` or read the documentation on [the GitHub repository of `llm`](https://github.com/simonw/llm).

### Change the Language of the Response

`proofread` will always try to respond in the same language as the provided text, but it may fail and still display the corrections in English. Or maybe you want to ensure that it always responds in a specific language. 

In that case, you can open the script and add in the prompt something like this: "Respond in French".

![proofread_french](https://github.com/sderev/llm-toolbox/assets/24412384/f21e7f5f-e520-4bce-997f-1acbea5a4b93)
