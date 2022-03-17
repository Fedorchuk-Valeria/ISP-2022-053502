"""Class Text."""
import statistics
import re


class Text:
    """Working with text class."""

    def __init__(self, string: str) -> None:
        """Constructor."""
        self._data = string
        self._only_words = re.sub(r'[^a-zA-Z0-9\s]', '', self._data).lower()
        self._repetitions_of_words = self._count_repetitions_of_words()
        self._amount_of_words = sum(self._repetitions_of_words.values())
        self._amount_of_sentences = len(self._words_in_sentence())

    @property
    def data(self) -> str:
        """Get text data."""
        return self._data

    @property
    def repetitions_of_words(self) -> dict:
        """Get data about repetitions of words."""
        return self._repetitions_of_words

    def _count_repetitions_of_words(self) -> dict:
        """Count repetitions of words in text."""
        repetitions = {}
        words = self._only_words.split()
        for i in range(len(words)):
            if repetitions.get(words[i], -1) == -1:
                repetitions[words[i]] = 1
            else:
                repetitions[words[i]] += 1
        return repetitions

    def _words_in_sentence(self) -> list:
        """Count amount of words in sentence."""
        count_words = []
        new_text = self._data.replace('!', '.').replace('?', '.')
        sentences = new_text.split('.')
        for i in range(len(sentences)-1):
            sentences[i] = sentences[i].lstrip(' ').rstrip(' ')
            sentences[i] = re.sub(r'[^a-zA-Z0-9\s]', '', sentences[i])
            words = sentences[i].split()
            count_words.append(len(words))
        return count_words

    def average_value_of_words_in_sentence(self) -> float:
        """Find average value of words in sentences."""
        return self._amount_of_words / self._amount_of_sentences

    def median_value_of_words_in_sentence(self) -> int:
        """Find median value of words in sentences."""
        arr = self._words_in_sentence()
        return statistics.median(arr)

    def repetitions_of_n_grams(self, n: int) -> list:
        """Count repetitions of n-grams."""
        new_text = self._only_words.replace(' ', '')
        if n > len(new_text):
            n = len(new_text)
            print(f"N change to {n}")
        repetitions = {}
        for i in range(len(new_text)-n):
            if repetitions.get(new_text[i:i+n], -1) == -1:
                repetitions[new_text[i:i+n]] = 1
            else:
                repetitions[new_text[i:i+n]] += 1
        sort_l = sorted(repetitions.items(), key=lambda x: x[1], reverse=True)
        return sort_l
