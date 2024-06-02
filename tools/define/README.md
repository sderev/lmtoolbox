# `define`

The `define` tool takes a word as input and provides its definition along with an example sentence using the word.

It is part of the [LLM-Toolbox](https://github.com/sderev/lmtoolbox).

<!-- TOC -->
## Table of Contents

1. [Installation](#installation)
1. [Usage](#usage)
<!-- /TOC -->

## Installation

LLM-Toolbox needs to be installed. You can find [the detailed installation and configuration process on the main page of the repo](https://github.com/sderev/lmtoolbox).

You can install it with `pip` or `pipx` depending on your preferences:

* `pip`

    ```bash
    python3 -m pip install LMtoolbox
    ```

* `pipx`

    ```bash
    pipx install LMtoolbox
    ```

## Usage

**You can pass arguments as the following:**

```bash
define a proclivity
```

![define_1](https://github.com/sderev/lmtoolbox/assets/24412384/ec7b43b3-8a4f-4286-8968-6ecf95f925ef)

**You can specify a language:**

```bash
define impavide en français
```

![define_3](https://github.com/sderev/lmtoolbox/assets/24412384/606b68c2-43c6-41db-96d7-e1e7828b8421)

**Or you can read `stdin` by using a pipe:**

```bash
echo "unwavering" | define
```

![define_2](https://github.com/sderev/lmtoolbox/assets/24412384/315cbe8f-2065-4a71-9bb3-a683cb3336f3)

The latter example is a bit contrived, but it works.
