# LChat

Large Language Model (LLM) chat command line inteferace based using [HuggingFace](https://huggingface.co/).


## Installation

```
pip install lchat
```

## Usage

You will likely need to login via [huggingface_hub](https://huggingface.co/docs/huggingface_hub/quick-start#authentication).

The usage is very simple. Start chatting by typing `lchat`:

```
usage: lchat [-h] [-p PROMPT] [-m MODEL] [-l]

Sends an input to a HuggingFace LLM.

options:
  -h, --help            show this help message and exit
  -p PROMPT, --prompt PROMPT
                        Type of prompt to use. '' for none, 'email' for email.
  -m MODEL, --model MODEL
                        Hugging Face model to use.
  -l, --list            List default prompts.
```
