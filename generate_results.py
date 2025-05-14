import json

from collections import Counter

import matplotlib
import matplotlib.pyplot as plt

from scipy.stats import chi2

matplotlib.use("TkAgg")


def get_data() -> list:
    with open("output.json", 'r') as f:
        return json.load(f)


def joined_data() -> list[int]:
    data = get_data()

    final = []
    for i in data:
        final.extend(i)

    return final


def graph() -> None:
    data = joined_data()

    plt.hist(data, bins=100, edgecolor='black', alpha=.7)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Value vs Frequency")
    plt.savefig("./histogram.png", dpi=900)
    print("Saved graph to \"./histogram.png\".")


def most_common() -> int:
    data = joined_data()
    mc = Counter(data).most_common(1)[0][0]
    print(f"Most common number: {mc}.")
    return mc


def chi_squared(minimum: int = 0, maximum: int = 100, df: int = 100, p: float = 0.05) -> None:
    data = joined_data()

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


if __name__ == '__main__':
    graph()
    most_common()
    chi_squared()
