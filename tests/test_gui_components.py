import unittest
from unittest import mock

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QPushButton, QTextEdit, QApplication

from tests.qt_support import get_app
from src.ui.components import ShiftWidget
from src.utils import clipboard

app = get_app()


class ShiftWidgetTest(unittest.TestCase):
    def setUp(self):
        self.widget = ShiftWidget()
        self.emitted = []
        self.widget.value_changed.connect(self.emitted.append)

    def test_starts_at_zero(self):
        self.assertEqual(self.widget.value, 0)
        self.assertEqual(self.widget.value_label.text(), "00")

    def test_plus_click_increments_and_notifies(self):
        self.widget.plus_button.click()
        self.assertEqual(self.widget.value, 1)
        self.assertEqual(self.widget.value_label.text(), "01")
        self.assertEqual(self.emitted, [1])

    def test_minus_click_decrements(self):
        self.widget.set_value(5)
        self.widget.minus_button.click()
        self.assertEqual(self.widget.value, 4)

    def test_minus_stops_at_zero_without_notifying(self):
        self.widget.minus_button.click()
        self.assertEqual(self.widget.value, 0)
        self.assertEqual(self.emitted, [])

    def test_plus_wraps_from_maximum_to_zero(self):
        self.widget.set_value(ShiftWidget.MAX_SHIFT)
        self.widget.plus_button.click()
        self.assertEqual(self.widget.value, 0)
        self.assertEqual(self.widget.value_label.text(), "00")

    def test_label_is_zero_padded(self):
        self.widget.set_value(26)
        self.assertEqual(self.widget.value_label.text(), "26")
        self.widget.set_value(7)
        self.assertEqual(self.widget.value_label.text(), "07")

    def test_set_value_is_clamped_to_range(self):
        self.widget.set_value(99)
        self.assertEqual(self.widget.value, ShiftWidget.MAX_SHIFT)
        self.widget.set_value(-4)
        self.assertEqual(self.widget.value, ShiftWidget.MIN_SHIFT)

    def test_reset_returns_to_zero(self):
        self.widget.set_value(12)
        self.widget.reset()
        self.assertEqual(self.widget.value, 0)
        self.assertEqual(self.widget.value_label.text(), "00")

    def test_holding_a_button_repeats_the_step_until_released(self):
        QTest.mousePress(self.widget.plus_button, Qt.LeftButton)
        QTest.qWait(500)   # ticks every 150 ms -> at least 3 repeats
        QTest.mouseRelease(self.widget.plus_button, Qt.LeftButton)
        value_after_release = self.widget.value
        self.assertGreaterEqual(value_after_release, 3)

        QTest.qWait(400)   # the timer must be stopped now
        self.assertEqual(self.widget.value, value_after_release)

    def test_hold_does_nothing_while_disabled(self):
        QTest.mousePress(self.widget.minus_button, Qt.LeftButton)
        self.widget.set_value(10)
        self.widget.setDisabled(True)
        QTest.qWait(400)
        self.assertEqual(self.widget.value, 10)


class CopyButtonTest(unittest.TestCase):
    """clipboard.copy(): clipboard content and the temporary "Copied!" state of the button."""

    def setUp(self):
        self.output = QTextEdit()
        self.output.setPlainText("secret message")
        self.button = QPushButton("\U0001F4CB Copy")
        self.button.setObjectName("copy_btn")
        self.button.setProperty("copied", False)
        self.button.show()
        app.processEvents()

    def tearDown(self):
        self.button.close()

    def _background(self):
        image = self.button.grab().toImage()
        color = image.pixelColor(image.width() // 2, 4)   # plain fill, away from the text
        return color.red(), color.green(), color.blue()

    def test_copies_the_text_to_the_clipboard(self):
        clipboard.copy(self.output, self.button)
        self.assertEqual(QApplication.clipboard().text(), "secret message")

    def test_button_shows_copied_state_with_the_green_style(self):
        normal = self._background()
        clipboard.copy(self.output, self.button)
        red, green, blue = self._background()

        self.assertIn("Copied!", self.button.text())
        self.assertFalse(self.button.isEnabled())
        self.assertTrue(self.button.property("copied"))
        self.assertGreater(green, red + 20)     # [copied="true"] rule in style.qss is applied
        self.assertGreater(green, blue + 20)
        self.assertNotEqual((red, green, blue), normal)

    def test_button_is_restored_after_the_flash(self):
        normal = self._background()
        with mock.patch.object(clipboard, "COPIED_FLASH_MS", 30):
            clipboard.copy(self.output, self.button)
            QTest.qWait(200)

        self.assertEqual(self.button.text(), "\U0001F4CB Copy")
        self.assertTrue(self.button.isEnabled())
        self.assertFalse(self.button.property("copied"))
        self.assertEqual(self._background(), normal)

    def test_button_stays_disabled_if_content_was_cleared_during_the_flash(self):
        with mock.patch.object(clipboard, "COPIED_FLASH_MS", 30):
            clipboard.copy(self.output, self.button)
            self.output.clear()                      # e.g. the user pressed Reset
            QTest.qWait(200)

        self.assertFalse(self.button.isEnabled())
        self.assertEqual(self.button.text(), "\U0001F4CB Copy")


if __name__ == "__main__":
    unittest.main()
