"""Class UserInterface."""
from Text import Text


class UserInterface:
    """Class for working with user."""

    def __init__(self) -> None:
        """Constructor."""
        print("Enter text:")
        data = input()
        while data == '':
            print('Error input! Try again:')
            data = input()
        last_symbol = data[len(data)-1]
        if last_symbol != '.' and last_symbol != '!' and last_symbol != '?':
            data += '.'
        self.text = Text(data)

    @staticmethod
    def print_dictionary(d: dict) -> None:
        """Print keys and value of dictionary."""
        keys = list(d.keys())
        for i in range(len(keys)):
            print(f"Word '{keys[i]}' is repeated {d[keys[i]]} times")

    @staticmethod
    def check_input() -> int:
        """Checking if a number is positive."""
        n = input()
        while (not n.strip().isdigit()) or int(n) == 0:
            print('Error input! Try again:')
            n = input()
        return int(n)

    def print_top_of_n_grams(self) -> None:
        """Print n-grams that are most used in text."""
        print("Enter N:")
        n = self.check_input()
        repetitions = self.text.repetitions_of_n_grams(n)
        print("Enter K:")
        k = self.check_input()
        while k > len(repetitions):
            print('Error input! Try again:')
            k = self.check_input()
        i = 0
        while i < k:
            print(repetitions[i])
            i += 1

    def show_information_about_text(self) -> None:
        """Print all need information about text."""
        self.print_dictionary(self.text.repetitions_of_words)
        print(f"Average value of words in sentences - "
              f"{self.text.average_value_of_words_in_sentence()}")
        print(f"Median value of words in sentences - "
              f"{self.text.median_value_of_words_in_sentence()}")
        self.print_top_of_n_grams()
