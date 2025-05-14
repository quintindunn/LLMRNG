import json

from tqdm import tqdm
from ollama import ChatResponse, chat

NUM_NUMBERS_PER_RESPONSE = 100
NUM_RESPONSES = 1000


def generate_response(prompt: str = f"generate {NUM_NUMBERS_PER_RESPONSE} random numbers 0-100 in the format: "
                                    f"\"n1, n2, n3...\" DO NOT PUT ANY OTHER TEXT") -> str:
    response: ChatResponse = chat(model="llama3.2", messages=[
        {
            "role": "user",
            "content": prompt
        }
    ])
    return response.message.content


def filter_out_number(msg: str) -> list[int] | None:
    try:
        msg = list(map(int, msg.split(", ")))
        return msg
    except ValueError:
        return None


def get_number() -> list[int]:
    num = None

    fails = 0
    while num is None:
        resp = generate_response()
        num = filter_out_number(resp)
        fails += 1

        if fails > 1 and fails % 10 == 0:
            print(f"{fails} consecutive fails!")

    return num


if __name__ == '__main__':
    rows = []

    progress_bar = tqdm(range(NUM_RESPONSES))
    for i in progress_bar:
        rows.append(get_number())

    with open('output.json', 'w') as f:
        json.dump(rows, f)
