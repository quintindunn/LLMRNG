import json
import os

from collections import Counter

import matplotlib
import matplotlib.pyplot as plt

from scipy.stats import chi2

# Fixes issue with matplotlib backend in pycharm.
matplotlib.use("TkAgg")


def get_data(input_file: str | os.PathLike) -> list:
    """
    Reads the JSON from the input file
    :param input_file: Path to the input file
    :return: parsed json
    """

    with open(input_file, 'r') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("JSON file not properly formatted!")

    for i in data:
        if not isinstance(i, list):
            raise ValueError("JSON file not properly formatted!")

        for j in data:
            if not isinstance(j, int):
                raise ValueError("Values in JSON file not properly formatted!")

    return data


def joined_data(input_file: str | os.PathLike) -> list[int]:
    """
    Joins all the responses into one single list of integers
    :param input_file: The path to the input file.
    :return: concatenated list of the integers.
    """

    data = get_data(input_file=input_file)

    final = []
    for i in data:
        final.extend(i)

    return final


def graph(input_file: str | os.PathLike = "./histogram.png", output: str | os.PathLike = "./histogram.png",
          show: bool = False, save: bool = True, save_dpi: int = 900) -> None:
    """
    Graphs the numbers on a histogram and saves to f"./{output}"
    :param input_file: The path to the input file.
    :param output: The path to save the generated histogram to.
    :param show: Should it display the histogram
    :param save: Should it save the histogram to output
    :param save_dpi: The resolution to save the histogram at.
    :return: None
    """

    if not save and not show:
        raise ValueError("Must either save or show the histogram!")

    data = joined_data(input_file=input_file)

    plt.hist(data, bins=100, edgecolor='black', alpha=.7)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Value vs Frequency")

    if save:
        plt.savefig(output, dpi=save_dpi)
    if show:
        plt.show()
    print(f"Saved graph to \"{output}\".")


def most_common(input_file: str | os.PathLike = "./output.json") -> int:
    """
    Finds the most common integer in the list.
    :param input_file: The path to the input file.
    :return: The most common integer
    """
    data = joined_data(input_file=input_file)
    mc = Counter(data).most_common(1)[0][0]
    print(f"Most common number: {mc}.")
    return mc


def chi_squared(minimum: int = 0, maximum: int = 100, df: int = 100, p: float = 0.05,
                input_file: str | os.PathLike = "./output.json") -> None:
    """
    Calculated the chi-squared test statistic on the numbers
    :param minimum: The minimum number present
    :param maximum: The maximum number present
    :param df: How many degrees of freedom
    :param p: The confidence e.g. p=0.05 -> 95% confidence
    :param input_file: The path to the input file
    :return: None
    """
    data = joined_data(input_file=input_file)

    counts = [0 for _ in range(minimum, maximum + 1)]
    for i in data:
        counts[i] += 1

    expected = len(data) / 100

    x2 = 0
    for i in range(minimum, maximum + 1):
        observed = counts[i]
        numerator = (observed - expected) ** 2
        x2 += numerator / expected

    print(f"x^2 = {x2:.3f}")
    critical_value = chi2.ppf(1 - p, df)
    print(f"Critical Value: {critical_value:.3f}")

    if x2 > critical_value:
        print("Reject the H0")
    else:
        print("Fail to reject the H0")


def full_generation(input_file: str | os.PathLike, x2_min: int = 0, x2_max: int = 100,
                    x2_df: int = 100, x2_p: float = 0.05, histogram_output: str | os.PathLike = "./histogram.png"):
    """
    Runs all the result functions
    :param input_file: The path to the input file
    :param x2_min: The minimum value present in the data range (for chi-squared test)
    :param x2_max: The maximum value present in the data range (for chi-squared test)
    :param x2_df: The degrees of freedom for the chi-squared test
    :param x2_p: The confidence for the chi-squared test. e.g. p=0.05 -> 95% confidence
    :param histogram_output: The file path to output the histogram to.
    :return:
    """
    graph(input_file=histogram_output)
    most_common(input_file=input_file)
    chi_squared(input_file=input_file, minimum=x2_min, maximum=x2_max, df=x2_df, p=x2_p)


if __name__ == '__main__':
    full_generation("./output.json")
