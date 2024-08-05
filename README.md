# LChat

Large Language Model (LLM) chat command line inteferace based using [HuggingFace](https://huggingface.co/).


## Installation

```
pip install lchat
```

## Usage

You will likely need to login via [huggingface_hub](https://huggingface.co/docs/huggingface_hub/quick-start#authentication).

The usage is very simple, to enter the chat prompt run:

```
python -m lchat
```

The arguments that can be passed to lchat are as follows:

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

- To quit from the chat prompt, type `q` or `quit`.
- To erase all message history type `c` or `clear`.
- To show the help menu, type `h` or `help`.

Chats are not saved between sessions.

The `>>>` prompt is the prompt that awaits your input.
The `['.'] ... ` prompt is the LLM response.

## License

This project is licensed under the GNU GPL v3 license which can be found [here](LICENSE).

## Contributing

Issues and pull requests welcome!
