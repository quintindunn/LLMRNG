# Data Collection
When picking the models to use, it's important to know what the model is capable of, many LLMs can run code which can generate (pseudo) random numbers, with an extremely even distribution, which has been utilized for years.<br>

For this reason, and the simplicity of Ollama integration I will be running the tests on the following models:
* LLama3.2

The models will be prompted through the user role, and given the exact same prompt of
```
Generate {**Expected** count of numbers per response} random numbers 0-100 in the format: n1, n2, n3..." DO NOT PUT ANY OTHER TEXT"
```
It's important to note that the LLMs will not necessarily generate exactly 100 numbers, for this reason if the model generates less than 100 numbers, it will try again, anything over 100 numbers the response will be truncated after the 100th number. This shouldn't affect the results of the response any meaningful amount, if at all because LLMs operate using tokens. Each number is likely a single token, and future tokens rely on the previous tokens, but previous tokens do not care for future tokens.<br>

During each test I generated 100 numbers per response, with 1,000 responses, totalling 100,000 numbers per model. The results were then stored to a file, maintaining the distinction between responses.

The code for data collection is in [generate_numbers.py](../generate_numbers.py).

[next - Analysis](ANALYSIS.md)