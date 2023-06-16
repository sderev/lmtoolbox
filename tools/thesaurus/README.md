# `thesaurus`

The `thesaurus script takes a word or a phrase as input and provides a list of synonyms and antonyms.

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

**You can pass arguments as the following:**

```bash
thesaurus good
```

![thesaurus_1](https://github.com/sderev/llm-toolbox/assets/24412384/ce5996e6-4401-440c-a3eb-cd8dfed7608a)

**Or you can read `stdin` by using a pipe:**

```bash
echo "a thing" | thesaurus
```

![thesaurus_2](https://github.com/sderev/llm-toolbox/assets/24412384/5ed90014-0410-43dc-b691-e850f1cb0fb5)

The latter example is a bit contrived, but it would work.
