import json
import os

from tqdm import tqdm
from ollama import ChatResponse, chat

EXPECTED_NUM_NUMBERS_PER_RESPONSE: int = 100
NUM_RESPONSES: int = 1000
MODEL: str = "llama3.2"
CALCULATE_RESULTS: bool = True


def generate_response(prompt: str = f"generate {EXPECTED_NUM_NUMBERS_PER_RESPONSE} random numbers 0-100 in the format: "
                                    f"\"n1, n2, n3...\" DO NOT PUT ANY OTHER TEXT") -> str:
    """
    Generates the "random" numbers through the LLM
    :param prompt: The prompt to feed the LLM
    :return: The response from the LLM
    """
    response: ChatResponse = chat(model=MODEL, messages=[
        {
            "role": "user",
            "content": prompt
        }
    ])
    return response.message.content


def filter_out_number(msg: str) -> list[int] | None:
    """
    Parse out the numbers from the response of the LLM, and return a list of the integers
    :param msg: The message from the LLM
    :return: List of integers parsed from the model's response.
    """
    try:
        msg = list(map(int, msg.split(", ")))
        return msg
    except ValueError:
        return None


def get_numbers() -> list[int]:
    """
    Generates an iteration of numbers from the LLM
    :return: List of "random" integers
    """
    num = None

    fails = 0
    while num is None:
        resp = generate_response()
        num = filter_out_number(resp)
        fails += 1

        if fails > 1 and fails % 10 == 0:
            print(f"{fails} consecutive fails!")

    return num


def generate_iterations(iter_count: int, output_file: str | os.PathLike = "./output.json"):
    """
    Generates the dataset
    :param iter_count: The amount of iterations of get_numbers(...)
    :param output_file: The output file for the dataset.
    :return:
    """
    rows = []

    progress_bar = tqdm(range(iter_count))
    for _ in progress_bar:
        rows.append(get_numbers())

    with open(output_file, 'w') as f:
        json.dump(rows, f)


if __name__ == '__main__':
    generate_iterations(NUM_RESPONSES, "output.json")
