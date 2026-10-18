import string
from functools import lru_cache

ALPHABET_SIZE = len(string.ascii_lowercase)


@lru_cache(maxsize=None)
def _translation_table(shift):
    """Translation table for a shift already normalised to 0..ALPHABET_SIZE-1."""
    lower, upper = string.ascii_lowercase, string.ascii_uppercase
    shifted_lower = lower[shift:] + lower[:shift]
    shifted_upper = upper[shift:] + upper[:shift]
    return str.maketrans(lower + upper, shifted_lower + shifted_upper)


class CaesarCipher:
    """Shifts the letters A-Z and a-z; every other character is left unchanged."""

    def caesar(self, text, shift):
        """Return `text` with each letter moved `shift` places forward in the alphabet.

        Case is preserved and the alphabet wraps around, so a shift of 0 or 26
        returns the text unchanged.
        """
        return text.translate(_translation_table(shift % ALPHABET_SIZE))
