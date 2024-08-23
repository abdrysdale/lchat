"""Prompting for hugging face."""

# ruff: noqa: T201

from __future__ import annotations

# Python imports
import time

import requests

# Module impots
from huggingface_hub import InferenceClient


def chat(
        model: str = "meta-llama/Meta-Llama-3.1-70B-Instruct",
        prompt: str | None = None,
        max_retries: int = 100,
) -> None:
    """Begin the chat interface."""
    client = InferenceClient(model=model)

    help_str = (
        "Press q to quit, c to clear chat history or h to display this message."
    )

    is_chatting = True
    num_failures = 0
    messages = [
        {
            "role": "user",
            "content": (
                "I am chatting to you via the terminal,"
                " please format your answers appropriately.\n"
                "You don't need to acknowledge this instruction,"
                " just do it."
            ),
        },
    ]
    while is_chatting:

        if prompt is not None and prompt:
            _input = prompt
            prompt = None
        else:
            _input = input(">>> ")
            if _input in ("q", "quit"):
                return
            if _input in ("h", "help"):
                print(help_str)
                continue
            if _input in ("c", "clear"):
                messages = []
                num_failures = 0
                continue

        if num_failures == 0:
            messages.append({"role": "user", "content": _input})

        try:
            n = num_failures % 4
            print(f"['_'] {"." * n }{" " * (3 - n)}\r", end="", flush=True)
            output = client.chat_completion(
                model = model,
                messages = messages,
                max_tokens = 1024,
            )
            num_failures = 0
            print("['o']", flush=True)
        except requests.exceptions.HTTPError:
            time.sleep(1)
            num_failures += 1
            prompt = _input
            if num_failures > max_retries:
                print(
                    "['o'] 'I'm sorry the model appears to be overloaded. Try again?'",
                    flush = True,
                )
                prompt = None
                del messages[-1]
            continue

        response = []
        if output.choices:
            response.append(output.choices[0].message.content)
            print(response[-1])
        else:
            print("Model did not respond!")
            return
        messages.append({"role": "assistant", "content": "\n".join(response)})


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
