# `translate`

The translate tool takes a sentence and a target language as input and provides the translated sentence in the target language.

<!-- TOC -->
## Table of Contents

1. [Installation](#installation)
1. [Usage](#usage)
    1. [Default Pair of Languages](#default-pair-of-languages)
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

**You can pass arguments and specify a target language:**

```
translate marvelous in Japanese
```

![translate_japanese](https://github.com/sderev/lmtoolbox/assets/24412384/f2e36454-5563-4bc7-b332-e8ea3eec6921)

**But this is not required:**

```
translate to enrapture
```

![translate](https://github.com/sderev/lmtoolbox/assets/24412384/6cae15ee-756e-4f31-a0a2-fb7237aafbbb)

In that case, the default pair of languages will be used.

**Or you could read `stdin` by using a pipe:**

```bash
cat my_file.txt | translate
```

![translate_file_english](https://github.com/sderev/lmtoolbox/assets/24412384/c01568ef-5260-4a59-b987-2a7e7d53f565)

You won't be able to define a language with the latter example, though.

### Default Pair of Languages

The current prompt is set to French and English.

You can change this behavior by editing the prompt in the script with your desired pair of languages.
