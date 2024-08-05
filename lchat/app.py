"""Prompting for hugging face."""

# ruff: noqa: T201

from __future__ import annotations

# Module impots
from huggingface_hub import InferenceClient


def chat(
        model: str = "meta-llama/Meta-Llama-3.1-405B-Instruct",
        prompt: str | None = None,
) -> None:
    """Begin the chat interface."""
    client = InferenceClient(model=model)

    help_str = (
        "Press q to quit, c to clear chat history or h to display this message."
    )

    is_chatting = True
    messages = []
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
                continue

        messages.append({"role": "user", "content": _input})

        print("['.'] ... ")
        output = client.chat_completion(
            model = model,
            messages = messages,
            max_tokens = 1024,
        )

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
        "default" : (
                "The output of your response will be recived by a 89"
                " characeter wide terminal.\n"
                "Please format your response appropriately."
        ),
    }


def get_prompt(key: str) -> str:
        """Get the prompt from key."""
        for k, p in get_prompt_dict().items():
                if k.lower() == key.lower():
                        return p
        return ""
