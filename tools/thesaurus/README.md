# `thesaurus`

The `thesaurus tool takes a word or a phrase as input and provides a list of synonyms and antonyms.

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
thesaurus good
```

![thesaurus_1](https://github.com/sderev/lmtoolbox/assets/24412384/ce5996e6-4401-440c-a3eb-cd8dfed7608a)

**Or you can read `stdin` by using a pipe:**

```bash
echo "a thing" | thesaurus
```

![thesaurus_2](https://github.com/sderev/lmtoolbox/assets/24412384/5ed90014-0410-43dc-b691-e850f1cb0fb5)

The latter example is a bit contrived, but it would work.
