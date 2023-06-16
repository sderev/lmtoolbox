# `define`

The `define` script takes a word as input and provides its definition along with an example sentence using the word.

<!-- TOC -->
## Table of Contents

1. [Prerequisites](#prerequisites)
1. [Installation](#installation)
    1. [Linux/macOS](#linuxmacos)
    1. [Windows](#windows)
1. [Usage](#usage)
<!-- /TOC -->

## Prerequisites

* `llm` needs to be installed. You can find it [here](https://github.com/simonw/llm). Follow the instructions in its README for the official installation details and documentaton.

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
define a proclivity
```

![define_1](https://github.com/sderev/llm-toolbox/assets/24412384/ec7b43b3-8a4f-4286-8968-6ecf95f925ef)

**You can specify a language:**

```bash
define impavide en français
```

![define_3](https://github.com/sderev/llm-toolbox/assets/24412384/606b68c2-43c6-41db-96d7-e1e7828b8421)

**Or you can read `stdin` by using a pipe:**

```bash
echo "unwavering" | define
```

![define_2](https://github.com/sderev/llm-toolbox/assets/24412384/315cbe8f-2065-4a71-9bb3-a683cb3336f3)

The latter example is a bit contrived, but it works.
