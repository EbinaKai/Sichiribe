"""
画面の管理を行うクラス

1. 画面遷移を行う
2. 画面サイズの保存、復元を行う
3. ポップアップメッセージボックスの表示を行う
4. アプリケーションの終了を行う
"""

from PySide6.QtWidgets import QApplication, QStackedWidget, QMainWindow, QMessageBox
from PySide6.QtGui import QPalette
from PySide6.QtCore import QEventLoop, QTimer, QPoint, QSize
from gui.widgets.custom_qwidget import CustomQWidget
import logging
from dataclasses import dataclass
from typing import Tuple, Dict, Optional


@dataclass
class ScreenInfo:
    widget: CustomQWidget
    title: str


class ScreenManager:
    def __init__(self, stacked_widget: QStackedWidget, main_window: QMainWindow):
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.logger = logging.getLogger("__main__").getChild(__name__)
        self.screens: Dict[str, ScreenInfo] = {}
        self.window_pos: Optional[QPoint] = None
        self.window_size: Optional[QSize] = None

    def add_screen(self, name: str, widget: CustomQWidget, title: str) -> None:
        self.screens[name] = ScreenInfo(widget=widget, title=title)
        self.stacked_widget.addWidget(widget)

    def show_screen(self, name: str) -> None:
        if name in self.screens:
            widget = self.screens[name].widget
            widget.display()
            self.main_window.setWindowTitle(f"Sichiribe {self.screens[name].title}")
            self.stacked_widget.setCurrentWidget(widget)
            self.main_window.setFocus()
        else:
            raise ValueError(f"Screen '{name}' not found")

    def get_screen(self, name: str) -> CustomQWidget:
        if name in self.screens:
            return self.screens[name].widget
        else:
            raise ValueError(f"Screen '{name}' not found")

    def check_if_dark_mode(self) -> bool:
        palette = QApplication.palette()
        return palette.color(QPalette.ColorRole.Window).value() < 128

    def resize_defualt(self) -> None:
        self.main_window.resize(640, 480)

    def save_screen_size(self) -> Tuple[QPoint, QSize]:
        self.window_pos = self.main_window.frameGeometry().topLeft()
        self.window_size = self.main_window.size()
        return self.window_pos, self.window_size

    def restore_screen_size(self) -> None:
        QApplication.processEvents()
        if self.window_pos is not None and self.window_size is not None:
            self.logger.info("Screen geometry restoring...")

            # 現在の画面内のオブジェクトが処理を終えるまで10ms待つ
            loop = QEventLoop()
            QTimer.singleShot(10, loop.quit)
            loop.exec()

            self.main_window.move(self.window_pos)
            self.main_window.resize(self.window_size)
            self.window_pos = None
            self.window_size = None

        else:
            self.logger.error("No screen size saved")

    def popup(self, message: str) -> None:
        self.logger.debug("Popup message: %s" % message)

        msg_box = QMessageBox(self.main_window)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.show()

    def quit(self) -> None:
        self.logger.info("Quitting application")
        QApplication.quit()
