import unittest
from unittest import mock

from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from tests.qt_support import get_app
from src.ui.main_window import MainWindow
from src.utils import clipboard

app = get_app()


class EncryptControllerTest(unittest.TestCase):
    def setUp(self):
        self.window = MainWindow()
        self.page = self.window.encrypt_page

    def _shift_to(self, value):
        self.page.shift_widget.set_value(value)

    def test_initial_state(self):
        self.assertEqual(self.page.encrypt_output.toPlainText(), "")
        self.assertFalse(self.page.encrypt_reset_button.isEnabled())
        self.assertFalse(self.page.encrypt_copy_button.isEnabled())

    def test_encrypts_live_while_typing(self):
        self._shift_to(3)
        self.page.encrypt_input.setPlainText("Hello, World!")
        self.assertEqual(self.page.encrypt_output.toPlainText(), "Khoor, Zruog!")

    def test_changing_the_shift_re_encrypts(self):
        self.page.encrypt_input.setPlainText("abc")
        self.assertEqual(self.page.encrypt_output.toPlainText(), "abc")      # shift 00
        self.page.shift_widget.plus_button.click()
        self.assertEqual(self.page.encrypt_output.toPlainText(), "bcd")
        self.page.shift_widget.plus_button.click()
        self.assertEqual(self.page.encrypt_output.toPlainText(), "cde")

    def test_html_like_text_is_kept_as_plain_text(self):
        self.page.encrypt_input.setPlainText("<b>a</b>")
        self.assertEqual(self.page.encrypt_output.toPlainText(), "<b>a</b>")

    def test_buttons_follow_the_input(self):
        self.page.encrypt_input.setPlainText("hello")
        self.assertTrue(self.page.encrypt_reset_button.isEnabled())
        self.assertTrue(self.page.encrypt_copy_button.isEnabled())

        self.page.encrypt_input.clear()
        self.assertEqual(self.page.encrypt_output.toPlainText(), "")
        self.assertFalse(self.page.encrypt_reset_button.isEnabled())
        self.assertFalse(self.page.encrypt_copy_button.isEnabled())

    def test_random_option_disables_shift_widget_and_uses_a_random_shift(self):
        self.page.encrypt_input.setPlainText("abc")
        with mock.patch("src.controllers.encrypt_controller.randint", return_value=5) as randint:
            self.page.random_checkbox.setChecked(True)
            self.assertEqual(self.page.encrypt_output.toPlainText(), "fgh")
            randint.assert_called_with(1, 25)
        self.assertFalse(self.page.shift_widget.isEnabled())

    def test_unchecking_random_goes_back_to_the_manual_shift(self):
        self._shift_to(2)
        self.page.encrypt_input.setPlainText("abc")
        self.page.random_checkbox.setChecked(True)
        self.page.random_checkbox.setChecked(False)
        self.assertTrue(self.page.shift_widget.isEnabled())
        self.assertEqual(self.page.encrypt_output.toPlainText(), "cde")

    def test_random_shift_is_never_zero_or_a_full_cycle(self):
        self.page.encrypt_input.setPlainText("abc")
        self.page.random_checkbox.setChecked(True)
        for _ in range(200):
            self.window.encrypt_controller.update_output()
            self.assertNotEqual(self.page.encrypt_output.toPlainText(), "abc")

    def test_reset_clears_everything(self):
        self._shift_to(4)
        self.page.encrypt_input.setPlainText("hello")
        self.page.random_checkbox.setChecked(True)

        self.page.encrypt_reset_button.click()

        self.assertEqual(self.page.encrypt_input.toPlainText(), "")
        self.assertEqual(self.page.encrypt_output.toPlainText(), "")
        self.assertEqual(self.page.shift_widget.value, 0)
        self.assertEqual(self.page.shift_widget.value_label.text(), "00")
        self.assertFalse(self.page.random_checkbox.isChecked())
        self.assertTrue(self.page.shift_widget.isEnabled())
        self.assertFalse(self.page.encrypt_reset_button.isEnabled())
        self.assertFalse(self.page.encrypt_copy_button.isEnabled())


class DecryptControllerTest(unittest.TestCase):
    def setUp(self):
        self.window = MainWindow()
        self.page = self.window.decrypt_page

    def test_initial_state(self):
        self.assertEqual(self.page.decrypt_output.toPlainText(), "")
        self.assertFalse(self.page.decrypt_reset_button.isEnabled())
        self.assertFalse(self.page.decrypt_copy_button.isEnabled())

    def test_output_updates_live_while_typing(self):
        self.page.decrypt_input.setPlainText("abc")
        self.assertEqual(self.page.decrypt_output.toPlainText(), "abc")      # shift 00
        self.assertTrue(self.page.decrypt_reset_button.isEnabled())
        self.assertTrue(self.page.decrypt_copy_button.isEnabled())

    def test_changing_the_shift_updates_the_output(self):
        self.page.decrypt_input.setPlainText("abc")
        self.page.shift_widget.plus_button.click()
        self.assertEqual(self.page.decrypt_output.toPlainText(), "bcd")

    def test_shift_is_applied_forward_like_in_the_original_app(self):
        """Characterisation test: the original app's decrypt shifts letters FORWARD by
        the selected value (decrypting "Khoor" needs shift 23, not 3). Refactoring must
        not change this silently. If it is changed on purpose, update this test."""
        self.page.decrypt_input.setPlainText("Khoor")
        for _ in range(3):
            self.page.shift_widget.plus_button.click()
        self.assertEqual(self.page.decrypt_output.toPlainText(), "Nkrru")

    def test_html_like_text_is_kept_as_plain_text(self):
        # the original used setText() after a shift change, which interprets HTML
        self.page.decrypt_input.setPlainText("<b>a</b>")
        self.page.shift_widget.plus_button.click()
        self.page.shift_widget.minus_button.click()
        self.assertEqual(self.page.decrypt_output.toPlainText(), "<b>a</b>")

    def test_clearing_the_input_disables_the_buttons(self):
        self.page.decrypt_input.setPlainText("abc")
        self.page.decrypt_input.clear()
        self.assertFalse(self.page.decrypt_reset_button.isEnabled())
        self.assertFalse(self.page.decrypt_copy_button.isEnabled())

    def test_reset_clears_input_output_and_shift(self):
        self.page.decrypt_input.setPlainText("abc")
        for _ in range(5):
            self.page.shift_widget.plus_button.click()

        self.page.decrypt_reset_button.click()

        self.assertEqual(self.page.decrypt_input.toPlainText(), "")
        self.assertEqual(self.page.decrypt_output.toPlainText(), "")
        self.assertEqual(self.page.shift_widget.value, 0)
        self.assertEqual(self.page.shift_widget.value_label.text(), "00")
        self.assertFalse(self.page.decrypt_reset_button.isEnabled())
        self.assertFalse(self.page.decrypt_copy_button.isEnabled())


class NavigationTest(unittest.TestCase):
    def setUp(self):
        self.window = MainWindow()

    def test_starts_on_the_home_page(self):
        self.assertIs(self.window.pages.currentWidget(), self.window.home_page)

    def test_home_buttons_open_the_pages_and_back_returns(self):
        self.window.home_page.encrypt_button.click()
        self.assertIs(self.window.pages.currentWidget(), self.window.encrypt_page)
        self.window.encrypt_page.back_button.click()
        self.assertIs(self.window.pages.currentWidget(), self.window.home_page)

        self.window.home_page.decrypt_button.click()
        self.assertIs(self.window.pages.currentWidget(), self.window.decrypt_page)
        self.window.decrypt_page.back_button.click()
        self.assertIs(self.window.pages.currentWidget(), self.window.home_page)

    def test_pages_keep_their_content_when_navigating(self):
        self.window.encrypt_page.encrypt_input.setPlainText("hello")
        self.window.show_home()
        self.window.show_encrypt()
        self.assertEqual(self.window.encrypt_page.encrypt_input.toPlainText(), "hello")

    def test_copy_buttons_put_the_output_on_the_clipboard(self):
        # short flash so no timer is left pending after the test
        with mock.patch.object(clipboard, "COPIED_FLASH_MS", 1):
            self.window.encrypt_page.shift_widget.set_value(1)
            self.window.encrypt_page.encrypt_input.setPlainText("abc")
            self.window.encrypt_page.encrypt_copy_button.click()
            self.assertEqual(QApplication.clipboard().text(), "bcd")

            self.window.decrypt_page.decrypt_input.setPlainText("xyz")
            self.window.decrypt_page.decrypt_copy_button.click()
            self.assertEqual(QApplication.clipboard().text(), "xyz")
            QTest.qWait(50)


if __name__ == "__main__":
    unittest.main()
