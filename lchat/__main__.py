"""Main script for running the app."""

# ruff: noqa: T201

import argparse
import sys

from lchat import app

if __name__ == "__main__":

    #####################
    # Formats arguments #
    #####################

    parser = argparse.ArgumentParser(
        prog="lchat",
        description="Sends an input to a HuggingFace LLM.",
    )

    parser.add_argument(
        "-p",
        "--prompt",
        default="",
        type=str,
        help="Type of prompt to use. '' for none, 'email' for email.",
    )

    parser.add_argument(
        "-m",
        "--model",
        default="meta-llama/Meta-Llama-3.1-70B-Instruct",
        type=str,
        help="Hugging Face model to use.",
    )

    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List default prompts.",
    )

    args = parser.parse_args()

    if args.list:
        for k, p in app.get_prompt_dict().items():
            print(f"{k}:\n```\n{p}\n```\n\n")
        sys.exit(0)

    _prompt = app.get_prompt(args.prompt)

    ############
    # Response #
    ############

    app.chat(model=args.model, prompt=_prompt)
