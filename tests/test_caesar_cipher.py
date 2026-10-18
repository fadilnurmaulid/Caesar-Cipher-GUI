import string
import unittest

from src.core.caesar_cipher import CaesarCipher


class CaesarCipherTest(unittest.TestCase):
    def setUp(self):
        self.cipher = CaesarCipher()

    def test_shifts_letters_forward(self):
        self.assertEqual(self.cipher.caesar("abc", 3), "def")

    def test_classic_example(self):
        self.assertEqual(self.cipher.caesar("Hello, World!", 3), "Khoor, Zruog!")

    def test_preserves_case(self):
        self.assertEqual(self.cipher.caesar("aBcD", 1), "bCdE")

    def test_wraps_around_the_alphabet(self):
        self.assertEqual(self.cipher.caesar("xyz XYZ", 3), "abc ABC")

    def test_leaves_non_letters_untouched(self):
        text = "123 !@# \t\n ñ é 日本語 🎉"
        self.assertEqual(self.cipher.caesar(text, 7), text)

    def test_empty_text(self):
        self.assertEqual(self.cipher.caesar("", 5), "")

    def test_shift_zero_and_full_cycle_are_identity(self):
        text = string.ascii_letters
        self.assertEqual(self.cipher.caesar(text, 0), text)
        self.assertEqual(self.cipher.caesar(text, 26), text)

    def test_every_ui_shift_can_be_undone_with_the_complementary_shift(self):
        text = "The quick brown fox, 123, jumps over the lazy dog!"
        for shift in range(0, 27):
            with self.subTest(shift=shift):
                encrypted = self.cipher.caesar(text, shift)
                self.assertEqual(self.cipher.caesar(encrypted, 26 - shift), text)

    def test_shift_beyond_the_alphabet_wraps(self):
        self.assertEqual(self.cipher.caesar("abc", 27), self.cipher.caesar("abc", 1))

    def test_negative_shift_goes_backwards(self):
        self.assertEqual(self.cipher.caesar("def", -3), "abc")


if __name__ == "__main__":
    unittest.main()
