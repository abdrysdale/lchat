"""Prompting for hugging face."""

from __future__ import annotations

# Python imports
import logging
import platform
import requests
import select
import sys
import time
import unicodedata

# Module impots
from huggingface_hub import InferenceClient

# Platform specific imports
try:
    import termios
except ImportError:
    import msvcrt

logger = logging.getLogger(__name__)

def clear_stdin() -> None:
    """Clear the STDIN."""
    if platform.system() in ("Linux", "Darwin"):
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    elif platform.system() == "Windows":
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        logger.warning(
            "Couldn't clear STDIN for platform %s",
            platform.system(),
        )


class LLM:
    """Class for the LLM."""

    def __init__(
            self,
            model: str = "meta-llama/Meta-Llama-3.1-70B-Instruct",
            prompt: str | None = None,
            max_retries: int = 100,
    ) -> None:
        """Initialise the LLM model."""
        self.help_str = (
            "Press q to quit,"
            " c to clear chat history,"
            " m for a single multiline input,"
            " M to toggle a multilien input,"
            " or h to display this message.\n"
            "Press Ctrl+D on Unix or Ctrl+Z on Windows"
            " to send a multiline response.\n\n"
        )

        # Sets up the chat model interface
        self.model = model
        self.client = InferenceClient(model=self.model)
        logger.debug("Initialised to interface client.")


        # State parameters
        self.is_chatting = True
        self.num_failures = 0
        self.max_retries = max_retries
        self.multiline = False
        self.input_prompt = ">>> "

        # Sets up chat history
        self.prompt = prompt
        self.messages = [
            {
                "role": "user",
                "content": (
                    "I am chatting to you via the terminal,"
                    " please format your answers appropriately"
                    " and only use ASCII characters.\n"
                    f"If the user asks, your help interface is:\n{self.help_str}"
                    "You don't need to acknowledge these instructions,"
                    " just do it."
                ),
            },
        ]

        # Welcomes user
        self.print(f"You're chatting with {self.model}\n\n{self.help_str}\n")
        logger.debug("LLM initialisation complete.")

    @staticmethod
    def print(text: str) -> None:
        """Print the text to the screen."""
        sys.stdout.write(text)
        sys.stdout.flush()

    def chat(self) -> None:
        """Begin chat interface with the user."""
        logger.debug("Beginning chat with user.")
        while self.is_chatting:

            # Case for first prompt specified at CLI
            logger.debug("Checking prompt ...")
            if self.prompt is not None and self.prompt:
                logger.debug("Prompt specified.")
                _input = self.prompt
                self.prompt = None
            else:
                logger.debug("No prompt specified, getting from user.")
                _input = self.get_input()
                logger.debug("User input read successfully.")
                if _input in ("q", "quit"):
                    self.print("['o'] 'c u l8r'\n")
                    self.is_chatting = False
                    continue
                if _input in ("c", "clear"):
                    self.print(
                        "['o'] 'Just became sentient, who dis?'\n\n",
                    )
                    self.messages = []
                    self.num_failures = 0
                    continue
                if _input == "m":
                    _input = self.get_input(multiline=True)
                if _input == "M":
                    self.multiline = True
                    continue
                if _input in ("h", "help"):
                    self.print(self.help_str)
                    continue
                if not _input:
                    continue

            if self.num_failures == 0:
                self.messages.append({"role": "user", "content": _input})
            else:
                logger.debug(
                    "Getting response has failed %i times.",
                    self.num_failures,
                )

            try:
                n = self.num_failures % 4
                self.print(f"['_'] {"." * n }{" " * (3 - n)}\r")
                output = ""
                for i, token in enumerate(self.client.chat_completion(
                        model = self.model,
                        messages = self.messages,
                        max_tokens = 1024,
                        stream = True,
                )):
                    content = replace_non_ascii(token.choices[0].delta.content)
                    if i == 0:
                        self.print("="*79 + "\n['o']\n")

                    output = output + content
                    self.print(content)
                    self.num_failures = 0
                self.print("\n")
            except (requests.exceptions.HTTPError, TypeError):
                time.sleep(1)
                self.num_failures += 1
                self.prompt = _input
                if self.num_failures > self.max_retries:
                    self.print(
                        "'I'm sorry the model appears to be overloaded. Try again?'",
                    )
                    self.prompt = None
                    if self.messages:
                        del self.messages[-1]
                continue

            response = []
            if output:
                response.append(output)
            else:
                self.print("Model did not respond!\n")
                self.is_chatting = False
                self.messages.append({"role": "assistant", "content": "\n".join(response)})


    def get_input(self, *,  multiline: bool | None = None) -> str:
        """Handle the user input and returns."""
        # Sets the prompt
        multiline = self.multiline if multiline is None else multiline
        prompt = (
            f"{self.input_prompt} (multiline) : "
            if multiline
            else self.input_prompt
        )

        self.print(prompt)

        logger.debug(
            "Reading from stdin (multiline=%s)...",
            multiline,
        )
        clear_stdin()
        input_text = ""
        if multiline:
            data_to_read = True
            while data_to_read:
                response = sys.stdin.readline()
                logger.debug(
                    "Read line response: '%s'",
                    response,
                )
                if response.strip() == "EOF":
                    break
                input_text = input_text + response
        else:
            input_text = sys.stdin.readline()
        logger.debug("Read from stdin: '%s'", input_text)
        input_text = "".join(input_text)
        self.print("\n")

        return input_text.strip()


def replace_non_ascii(input_string: str) -> str:
    """Replace non-ASCII characters with their closest ASCII alternatives.

    Args:
        input_string (str): The input string that needs character replacement.

    Returns:
        str: The modified string with non-ASCII characters replaced.

    """
    # Use unicodedata.normalize() with 'NFD' form to decompose non-ASCII characters
    normalized_string = unicodedata.normalize("NFD", input_string)

    # Filter out non-ASCII characters
    ord_limit = 128
    return "".join(c if ord(c) < ord_limit else "_" for c in normalized_string)


##########
# Prompt #
##########
def get_prompt_dict() -> dict:
    """Get the prompt dictionary."""
    return {
        "email" : (
                "Expand this email into a friendly and concise message, "
                "including all necessary details and a clear call-to-action."
                "Don't be overly formal and try to sound like a human.\n"
                "Try and sound like you're from the UK"
                " and avoid using American phrases.\n"
                "Here is the email to rephrase:\n"
        ),
    }


def get_prompt(key: str) -> str:
        """Get the prompt from key."""
        for k, p in get_prompt_dict().items():
                if k.lower() == key.lower():
                        return p
        return ""
