"""Main script for running the app."""

# ruff: noqa: T201

# Python imports
import argparse
import logging
import sys

# Local imports
import lchat
from lchat import app

logger = logging.getLogger(__name__)

def main() -> None:
    """Parse command line args and initialise chat."""
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

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Version information.",
    )

    parser.add_argument(
        "--log",
        default="warning",
        type=str,
        help="Log level, can be debug, info, warning, error or critical.",
    )

    args = parser.parse_args()

    if args.version:
        print(f"lchat: {lchat.__version__}")
        return True

    log_level = getattr(logging, args.log.upper())
    logging.basicConfig(level=log_level)

    if args.list:
        for k, p in app.get_prompt_dict().items():
            print(f"{k}:\n```\n{p}\n```\n\n")
        sys.exit(0)

    _prompt = app.get_prompt(args.prompt)

    ############
    # Response #
    ############

    llm = app.LLM(model=args.model, prompt=_prompt)
    llm.chat()
    return True


if __name__ == "__main__":
    main()
