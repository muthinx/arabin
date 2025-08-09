import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QMessageBox, QDialog, QDialogButtonBox
)
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

class NotificationDialog(QDialog):
    def __init__(self, message, dark_mode=False, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setFixedSize(250, 120)
        self.setStyleSheet(self._get_style(dark_mode))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        label = QLabel(message)
        label.setFont(QFont("Sans Serif", 10, QFont.Bold))
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(button_box)
    
    def _get_style(self, dark):
        if dark:
            return """
                QDialog {
                    background-color: #2d2d2d;
                    color: #f5f5f5;
                    border: 1px solid #555555;
                    border-radius: 10px;
                }
                QLabel {
                    color: #f5f5f5;
                }
                QPushButton {
                    background-color: #4a6fa5;
                    color: #f5f5f5;
                    padding: 6px 14px;
                    border: 1px solid #6688b3;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #587db8;
                }
            """
        else:
            return """
                QDialog {
                    background-color: #ffffff;
                    color: #333333;
                    border: 1px solid #cccccc;
                    border-radius: 10px;
                }
                QLabel {
                    color: #333333;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: #333333;
                    padding: 6px 14px;
                    border: 1px solid #aaaaaa;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """

class AboutDialog(QDialog):
    def __init__(self, dark_mode=False, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setFixedSize(300, 180)
        self.setStyleSheet(self._get_style(dark_mode))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title = QLabel("ℹ️ Tentang Arabin")
        title.setFont(QFont("Sans Serif", 11, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        desc = QLabel("Arabin v1.0\n\nAplikasi transliterasi Latin ke Arab.\nDikembangkan oleh Uiscript.\n© 2025 Uiscript.")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setFont(QFont("Sans Serif", 9))

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)

        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addStretch()
        layout.addWidget(button_box)

    def _get_style(self, dark):
        if dark:
            return """
                QDialog {
                    background-color: #2b2b2b;
                    color: #f0f0f0;
                    border: 1px solid #555;
                    border-radius: 8px;
                }
                QPushButton {
                    background-color: #3c3f41;
                    color: #f0f0f0;
                    padding: 5px 12px;
                    border: 1px solid #666;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #505354;
                }
            """
        else:
            return """
                QDialog {
                    background-color: #ffffff;
                    color: #2b2b2b;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: #2b2b2b;
                    padding: 5px 12px;
                    border: 1px solid #aaa;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d6d6d6;
                }
            """

class Transliterator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arabin")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(600, 500)
        self.setMinimumSize(500, 400)

        self.dark_mode = True  # default mode

        # ===== HEADER =====
        header = QHBoxLayout()
        header.setContentsMargins(5, 5, 5, 5)
        header.setSpacing(10)

        # Logo
        logo = QLabel()
        logo_pixmap = QPixmap("icon.png").scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(logo_pixmap)
        logo.setFixedHeight(20)

        # Judul
        title = QLabel("Arabin")
        title.setFont(QFont("Georgia", 18, QFont.Bold))
        title.setStyleSheet("padding-top: 2px;")

        title_layout = QHBoxLayout()
        title_layout.addWidget(logo)
        title_layout.addWidget(title)
        title_layout.addStretch()

        # Tombol dark/light mode
        self.mode_button = QPushButton("🌙")
        self.mode_button.setFixedSize(30, 30)
        self.mode_button.clicked.connect(self.toggle_mode)

        # Tombol about
        about_button = QPushButton("ℹ️")
        about_button.setFixedSize(30, 30)
        about_button.clicked.connect(self.show_about)

        header.addLayout(title_layout)
        header.addStretch()
        header.addWidget(self.mode_button)
        header.addWidget(about_button)

        # ===== TEXT AREA =====
        label_input = QLabel("Teks Latin:")
        label_input.setFont(QFont("Sans Serif", 10, QFont.Bold))

        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Masukkan teks Latin di sini...")
        self.text_input.setFont(QFont("Sans Serif", 11))
        self.text_input.setFocus()

        label_output = QLabel("Hasil Transliterasi:")
        label_output.setFont(QFont("Sans Serif", 10, QFont.Bold))

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        self.text_output.setPlaceholderText("سيظهر النص العربي هنا")
        self.text_output.setFont(QFont("Arabic Typesetting, Arial", 32))
        self.text_output.setAlignment(Qt.AlignRight)

        # ===== BUTTONS =====
        button_layout = QHBoxLayout()
        self.transliterate_button = QPushButton("🔁 Transliterasi Sekarang")
        self.transliterate_button.clicked.connect(self.transliterate)
        self.transliterate_button.setStyleSheet("font-size: 11pt;")

        self.copy_button = QPushButton("📋 Salin Hasil")
        self.copy_button.clicked.connect(self.copy_output)
        self.copy_button.setStyleSheet("font-size: 11pt;")

        self.reset_button = QPushButton("🧹 Reset")
        self.reset_button.clicked.connect(self.reset_text)
        self.reset_button.setStyleSheet("font-size: 11pt;")

        button_layout.addWidget(self.transliterate_button)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.reset_button)

        # ===== VERSION =====
        version_label = QLabel("Arabin v1.0 © 2025 Uiscript")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: gray; font-size: 10pt;")

        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.addLayout(header)
        main_layout.addWidget(label_input)
        main_layout.addWidget(self.text_input)
        main_layout.addWidget(label_output)
        main_layout.addWidget(self.text_output)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(version_label)

        self.setLayout(main_layout)

        # Enable Ctrl+Enter
        self.text_input.keyPressEvent = self.handle_keypress

        # Apply initial mode
        self.apply_dark_mode()

    def handle_keypress(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Return:
            self.transliterate()
        else:
            QTextEdit.keyPressEvent(self.text_input, event)

    def toggle_mode(self):
        if self.dark_mode:
            self.apply_light_mode()
            self.mode_button.setText("☀️")
        else:
            self.apply_dark_mode()
            self.mode_button.setText("🌙")
        self.dark_mode = not self.dark_mode

    def apply_dark_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #3c3f41;
                color: #f0f0f0;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #505354;
            }
            QLabel {
                color: #cccccc;
            }
        """)

    def apply_light_mode(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                color: #2b2b2b;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #2b2b2b;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #2b2b2b;
                border: 1px solid #bbb;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d6d6d6;
            }
            QLabel {
                color: #444444;
            }
        """)

    def show_about(self):
        dialog = AboutDialog(dark_mode=self.dark_mode, parent=self)
        dialog.exec_()

    def transliterate(self):
        input_text = self.text_input.toPlainText().strip()

        if not input_text:
            QMessageBox.warning(self, "Peringatan", "Teks input tidak boleh kosong.")
            return

        output_text = input_text
        # Input Husus
        output_text = re.sub(r'\'alaa', 'عَلٰى', output_text)
        output_text = re.sub(r'dzaalika', 'ذٰلِكَ', output_text)
        output_text = re.sub(r'--', 'ال', output_text)
        output_text = re.sub(r'-', 'ا', output_text)
        output_text = re.sub(r'TaN', 'ةً', output_text)
        output_text = re.sub(r'TiN', 'ةٍ', output_text)
        output_text = re.sub(r'TuN', 'ةٌ', output_text)
        output_text = re.sub(r'Ta', 'ةَ', output_text)
        output_text = re.sub(r'Ti', 'ةِ', output_text)
        output_text = re.sub(r'Tu', 'ةُ', output_text)
        output_text = re.sub(r',', '،', output_text)
        # input StaNdar
        output_text = re.sub(r'cchuu', 'خُّوْ', output_text)
        output_text = re.sub(r'cchii', 'خِّيْ', output_text)
        output_text = re.sub(r'cchoo', 'خَّا', output_text)
        output_text = re.sub(r'cchuN', 'خٌّ', output_text)
        output_text = re.sub(r'cchiN', 'خٍّ', output_text)
        output_text = re.sub(r'cchaN', 'خًّ', output_text)
        output_text = re.sub(r'ddhuu', 'ظُّوْ', output_text)
        output_text = re.sub(r'ddhii', 'ظِّيْ', output_text)
        output_text = re.sub(r'ddhoo', 'ظَّا', output_text)
        output_text = re.sub(r'ddhuN', 'ظٌّ', output_text)
        output_text = re.sub(r'ddhiN', 'ظٍّ', output_text)
        output_text = re.sub(r'ddhaN', 'ظًّ', output_text)
        output_text = re.sub(r'ddluu', 'ضُّوْ', output_text)
        output_text = re.sub(r'ddlii', 'ضِّيْ', output_text)
        output_text = re.sub(r'ddloo', 'ضَّا', output_text)
        output_text = re.sub(r'ddluN', 'ضٌّ', output_text)
        output_text = re.sub(r'ddliN', 'ضٍّ', output_text)
        output_text = re.sub(r'ddlaN', 'ضًّ', output_text)
        output_text = re.sub(r'ddzuu', 'ذُّوْ', output_text)
        output_text = re.sub(r'ddzii', 'ذِّيْ', output_text)
        output_text = re.sub(r'ddzaa', 'ذَّا', output_text)
        output_text = re.sub(r'ddzuN', 'ذٌّ', output_text)
        output_text = re.sub(r'ddziN', 'ذٍّ', output_text)
        output_text = re.sub(r'ddzaN', 'ذًّ', output_text)
        output_text = re.sub(r'gghuu', 'غُّوْ', output_text)
        output_text = re.sub(r'gghii', 'غِّيْ', output_text)
        output_text = re.sub(r'gghoo', 'غَّا', output_text)
        output_text = re.sub(r'gghuN', 'غٌّ', output_text)
        output_text = re.sub(r'gghiN', 'غٍّ', output_text)
        output_text = re.sub(r'gghoN', 'غًّ', output_text)
        output_text = re.sub(r'kkhuu', 'حُّوْ', output_text)
        output_text = re.sub(r'kkhii', 'حِّيْ', output_text)
        output_text = re.sub(r'kkhaa', 'حَّا', output_text)
        output_text = re.sub(r'kkhuN', 'حٌّ', output_text)
        output_text = re.sub(r'kkhiN', 'حٍّ', output_text)
        output_text = re.sub(r'kkhaN', 'حًّ', output_text)
        output_text = re.sub(r'sshuu', 'صُّوْ', output_text)
        output_text = re.sub(r'sshii', 'صِّيْ', output_text)
        output_text = re.sub(r'sshoo', 'صَّا', output_text)
        output_text = re.sub(r'sshuN', 'صٌّ', output_text)
        output_text = re.sub(r'sshiN', 'صٍّ', output_text)
        output_text = re.sub(r'sshaN', 'صًّ', output_text)
        output_text = re.sub(r'ssyuu', 'شُّوْ', output_text)
        output_text = re.sub(r'ssyii', 'شِّيْ', output_text)
        output_text = re.sub(r'ssyaa', 'شَّا', output_text)
        output_text = re.sub(r'ssyuN', 'شٌّ', output_text)
        output_text = re.sub(r'ssyiN', 'شٍّ', output_text)
        output_text = re.sub(r'ssyaN', 'شًّ', output_text)
        output_text = re.sub(r'tthuu', 'طُّوْ', output_text)
        output_text = re.sub(r'tthii', 'طِّيْ', output_text)
        output_text = re.sub(r'tthoo', 'طَّا', output_text)
        output_text = re.sub(r'tthuN', 'طٌّ', output_text)
        output_text = re.sub(r'tthiN', 'طٍّ', output_text)
        output_text = re.sub(r'tthoN', 'طًّ', output_text)
        output_text = re.sub(r'ttsuu', 'ثُّوْ', output_text)
        output_text = re.sub(r'ttsii', 'ثِّيْ', output_text)
        output_text = re.sub(r'ttsaa', 'ثَّا', output_text)
        output_text = re.sub(r'ttsuN', 'ثٌّ', output_text)
        output_text = re.sub(r'ttsiN', 'ثٍّ', output_text)
        output_text = re.sub(r'ttsaN', 'ثًّ', output_text)
        output_text = re.sub(r'bbuu', 'بُّوْ', output_text)
        output_text = re.sub(r'bbii', 'بِّيْ', output_text)
        output_text = re.sub(r'bbaa', 'بَّا', output_text)
        output_text = re.sub(r'bbuN', 'بٌّ', output_text)
        output_text = re.sub(r'bbiN', 'بٍّ', output_text)
        output_text = re.sub(r'bbaN', 'بًّ', output_text)
        output_text = re.sub(r'dduu', 'دُّوْ', output_text)
        output_text = re.sub(r'ddii', 'دِّيْ', output_text)
        output_text = re.sub(r'ddaa', 'دَّا', output_text)
        output_text = re.sub(r'dduN', 'دٌّ', output_text)
        output_text = re.sub(r'ddiN', 'دٍّ', output_text)
        output_text = re.sub(r'ddaN', 'دًّ', output_text)
        output_text = re.sub(r'ffuu', 'فُّوْ', output_text)
        output_text = re.sub(r'ffii', 'فِّيْ', output_text)
        output_text = re.sub(r'ffaa', 'فَّا', output_text)
        output_text = re.sub(r'ffuN', 'فٌّ', output_text)
        output_text = re.sub(r'ffiN', 'فٍّ', output_text)
        output_text = re.sub(r'ffaN', 'فًّ', output_text)
        output_text = re.sub(r'hhuu', 'هُّوْ', output_text)
        output_text = re.sub(r'hhii', 'هِّيْ', output_text)
        output_text = re.sub(r'hhaa', 'هَّا', output_text)
        output_text = re.sub(r'hhuN', 'هٌّ', output_text)
        output_text = re.sub(r'hhiN', 'هٍّ', output_text)
        output_text = re.sub(r'hhaN', 'هًّ', output_text)
        output_text = re.sub(r'jjuu', 'جُّوْ', output_text)
        output_text = re.sub(r'jjii', 'جِّيْ', output_text)
        output_text = re.sub(r'jjaa', 'جَّا', output_text)
        output_text = re.sub(r'jjuN', 'جٌّ', output_text)
        output_text = re.sub(r'jjiN', 'جٍّ', output_text)
        output_text = re.sub(r'jjaN', 'جًّ', output_text)
        output_text = re.sub(r'kkuu', 'كُّوْ', output_text)
        output_text = re.sub(r'kkii', 'كِّيْ', output_text)
        output_text = re.sub(r'kkaa', 'كَّا', output_text)
        output_text = re.sub(r'kkuN', 'كٌّ', output_text)
        output_text = re.sub(r'kkiN', 'كٍّ', output_text)
        output_text = re.sub(r'kkaN', 'كًّ', output_text)
        output_text = re.sub(r'lluu', 'لُّوْ', output_text)
        output_text = re.sub(r'llii', 'لِّيْ', output_text)
        output_text = re.sub(r'llaa', 'لَّا', output_text)
        output_text = re.sub(r'lluN', 'لٌّ', output_text)
        output_text = re.sub(r'lliN', 'لٍّ', output_text)
        output_text = re.sub(r'llaN', 'لًّ', output_text)
        output_text = re.sub(r'mmuu', 'مُّوْ', output_text)
        output_text = re.sub(r'mmii', 'مِّيْ', output_text)
        output_text = re.sub(r'mmaa', 'مَّا', output_text)
        output_text = re.sub(r'mmuN', 'مٌّ', output_text)
        output_text = re.sub(r'mmiN', 'مٍّ', output_text)
        output_text = re.sub(r'mmaN', 'مًّ', output_text)
        output_text = re.sub(r'nnuu', 'نُّوْ', output_text)
        output_text = re.sub(r'nnii', 'نِّيْ', output_text)
        output_text = re.sub(r'nnaa', 'نَّا', output_text)
        output_text = re.sub(r'nnuN', 'نٌّ', output_text)
        output_text = re.sub(r'nniN', 'نٍّ', output_text)
        output_text = re.sub(r'nnaN', 'نًّ', output_text)
        output_text = re.sub(r'qquu', 'قُّوْ', output_text)
        output_text = re.sub(r'qqii', 'قِّيْ', output_text)
        output_text = re.sub(r'qqo', 'قَّا', output_text)
        output_text = re.sub(r'qquN', 'قٌّ', output_text)
        output_text = re.sub(r'qqiN', 'قٍّ', output_text)
        output_text = re.sub(r'qqoN', 'قًّ', output_text)
        output_text = re.sub(r'rruu', 'رُّوْ', output_text)
        output_text = re.sub(r'rrii', 'رِّيْ', output_text)
        output_text = re.sub(r'rroo', 'رَّا', output_text)
        output_text = re.sub(r'rruN', 'رٌّ', output_text)
        output_text = re.sub(r'rriN', 'رٍّ', output_text)
        output_text = re.sub(r'rron', 'رًّ', output_text)
        output_text = re.sub(r'ssuu', 'سُّوْ', output_text)
        output_text = re.sub(r'ssii', 'سِّيْ', output_text)
        output_text = re.sub(r'ssaa', 'سَّا', output_text)
        output_text = re.sub(r'ssuN', 'سٌّ', output_text)
        output_text = re.sub(r'ssiN', 'سٍّ', output_text)
        output_text = re.sub(r'ssaN', 'سًّ', output_text)
        output_text = re.sub(r'ttuu', 'تُّوْ', output_text)
        output_text = re.sub(r'ttii', 'تِّيْ', output_text)
        output_text = re.sub(r'ttaa', 'تَّا', output_text)
        output_text = re.sub(r'ttuN', 'تٌّ', output_text)
        output_text = re.sub(r'ttiN', 'تٍّ', output_text)
        output_text = re.sub(r'ttaN', 'تًّ', output_text)
        output_text = re.sub(r'wwuu', 'وُّوْ', output_text)
        output_text = re.sub(r'wwii', 'وِّيْ', output_text)
        output_text = re.sub(r'wwaa', 'وَّا', output_text)
        output_text = re.sub(r'wwuN', 'وٌّ', output_text)
        output_text = re.sub(r'wwiN', 'وٍّ', output_text)
        output_text = re.sub(r'wwaN', 'وًّ', output_text)
        output_text = re.sub(r'yyuu', 'يُّوْ', output_text)
        output_text = re.sub(r'yyii', 'يِّيْ', output_text)
        output_text = re.sub(r'yyaa', 'يَّا', output_text)
        output_text = re.sub(r'yyuN', 'يٌّ', output_text)
        output_text = re.sub(r'yyiN', 'يٍّ', output_text)
        output_text = re.sub(r'yyaN', 'يًّ', output_text)
        output_text = re.sub(r'zzuu', 'زُّوْ', output_text)
        output_text = re.sub(r'zzii', 'زِّيْ', output_text)
        output_text = re.sub(r'zzaa', 'زَّا', output_text)
        output_text = re.sub(r'zzuN', 'زٌّ', output_text)
        output_text = re.sub(r'zziN', 'زٍّ', output_text)
        output_text = re.sub(r'zzaN', 'زًّ', output_text)
        output_text = re.sub(r'\'\'uu', 'عُّوْ', output_text)
        output_text = re.sub(r'\'\'ii', 'عِّيْ', output_text)
        output_text = re.sub(r'\'\'aa', 'عَّا', output_text)
        output_text = re.sub(r'\'\'uN', 'عٌّ', output_text)
        output_text = re.sub(r'\'\'iN', 'عٍّ', output_text)
        output_text = re.sub(r'\'\'aN', 'عًّ', output_text)
        output_text = re.sub(r'cchu', 'خُّ', output_text)
        output_text = re.sub(r'cchi', 'خِّ', output_text)
        output_text = re.sub(r'ccha', 'خَّ', output_text)
        output_text = re.sub(r'ddhu', 'ظُّ', output_text)
        output_text = re.sub(r'ddhi', 'ظِّ', output_text)
        output_text = re.sub(r'ddha', 'ظَّ', output_text)
        output_text = re.sub(r'ddlu', 'ضُّ', output_text)
        output_text = re.sub(r'ddli', 'ضِّ', output_text)
        output_text = re.sub(r'ddla', 'ضَّ', output_text)
        output_text = re.sub(r'ddzu', 'ذُّ', output_text)
        output_text = re.sub(r'ddzi', 'ذِّ', output_text)
        output_text = re.sub(r'ddza', 'ذَّ', output_text)
        output_text = re.sub(r'gghu', 'غُّ', output_text)
        output_text = re.sub(r'gghi', 'غِّ', output_text)
        output_text = re.sub(r'ggha', 'غَّ', output_text)
        output_text = re.sub(r'kkhu', 'حُّ', output_text)
        output_text = re.sub(r'kkhi', 'حِّ', output_text)
        output_text = re.sub(r'kkha', 'حَّ', output_text)
        output_text = re.sub(r'sshu', 'صُّ', output_text)
        output_text = re.sub(r'sshi', 'صِّ', output_text)
        output_text = re.sub(r'ssha', 'صَّ', output_text)
        output_text = re.sub(r'ssyu', 'شُّ', output_text)
        output_text = re.sub(r'ssyi', 'شِّ', output_text)
        output_text = re.sub(r'ssya', 'شَّ', output_text)
        output_text = re.sub(r'tthu', 'طُّ', output_text)
        output_text = re.sub(r'tthi', 'طِّ', output_text)
        output_text = re.sub(r'ttho', 'طَّ', output_text)
        output_text = re.sub(r'ttsu', 'ثُّ', output_text)
        output_text = re.sub(r'ttsi', 'ثِّ', output_text)
        output_text = re.sub(r'ttsa', 'ثَّ', output_text)
        output_text = re.sub(r'chuu', 'خُوْ', output_text)
        output_text = re.sub(r'chii', 'خِيْ', output_text)
        output_text = re.sub(r'choo', 'خَا', output_text)
        output_text = re.sub(r'chuN', 'خٌ', output_text)
        output_text = re.sub(r'chiN', 'خٍ', output_text)
        output_text = re.sub(r'chaN', 'خً', output_text)
        output_text = re.sub(r'dhuu', 'ظُوْ', output_text)
        output_text = re.sub(r'dhii', 'ظِيْ', output_text)
        output_text = re.sub(r'dhoo', 'ظَا', output_text)
        output_text = re.sub(r'dhuN', 'ظٌ', output_text)
        output_text = re.sub(r'dhiN', 'ظٍ', output_text)
        output_text = re.sub(r'dhaN', 'ظً', output_text)
        output_text = re.sub(r'dluu', 'ضُوْ', output_text)
        output_text = re.sub(r'dlii', 'ضِيْ', output_text)
        output_text = re.sub(r'dloo', 'ضَا', output_text)
        output_text = re.sub(r'dluN', 'ضٌ', output_text)
        output_text = re.sub(r'dliN', 'ضٍ', output_text)
        output_text = re.sub(r'dlaN', 'ضً', output_text)
        output_text = re.sub(r'dzuu', 'ذُوْ', output_text)
        output_text = re.sub(r'dzii', 'ذِيْ', output_text)
        output_text = re.sub(r'dzaa', 'ذَا', output_text)
        output_text = re.sub(r'dzuN', 'ذٌ', output_text)
        output_text = re.sub(r'dziN', 'ذٍ', output_text)
        output_text = re.sub(r'dzaN', 'ذً', output_text)
        output_text = re.sub(r'ghuu', 'غُوْ', output_text)
        output_text = re.sub(r'ghii', 'غِيْ', output_text)
        output_text = re.sub(r'ghoo', 'غَا', output_text)
        output_text = re.sub(r'ghuN', 'غٌ', output_text)
        output_text = re.sub(r'ghiN', 'غٍ', output_text)
        output_text = re.sub(r'ghaN', 'غً', output_text)
        output_text = re.sub(r'khuu', 'حُوْ', output_text)
        output_text = re.sub(r'khii', 'حِيْ', output_text)
        output_text = re.sub(r'khaa', 'حَا', output_text)
        output_text = re.sub(r'khuN', 'حٌ', output_text)
        output_text = re.sub(r'khiN', 'حٍ', output_text)
        output_text = re.sub(r'khaN', 'حً', output_text)
        output_text = re.sub(r'shuu', 'صُوْ', output_text)
        output_text = re.sub(r'shii', 'صِيْ', output_text)
        output_text = re.sub(r'shoo', 'صَا', output_text)
        output_text = re.sub(r'shuN', 'صٌ', output_text)
        output_text = re.sub(r'shiN', 'صٍ', output_text)
        output_text = re.sub(r'shaN', 'صً', output_text)
        output_text = re.sub(r'syuu', 'شُوْ', output_text)
        output_text = re.sub(r'syii', 'شِيْ', output_text)
        output_text = re.sub(r'syaa', 'شَا', output_text)
        output_text = re.sub(r'syuN', 'شٌ', output_text)
        output_text = re.sub(r'syiN', 'شٍ', output_text)
        output_text = re.sub(r'syaN', 'شً', output_text)
        output_text = re.sub(r'thuu', 'طُوْ', output_text)
        output_text = re.sub(r'thii', 'طِيْ', output_text)
        output_text = re.sub(r'thoo', 'طَا', output_text)
        output_text = re.sub(r'thuN', 'طٌ', output_text)
        output_text = re.sub(r'thiN', 'طٍ', output_text)
        output_text = re.sub(r'thon', 'طً', output_text)
        output_text = re.sub(r'tsuu', 'ثُوْ', output_text)
        output_text = re.sub(r'tsii', 'ثِيْ', output_text)
        output_text = re.sub(r'tsaa', 'ثَا', output_text)
        output_text = re.sub(r'tsuN', 'ثٌ', output_text)
        output_text = re.sub(r'tsiN', 'ثٍ', output_text)
        output_text = re.sub(r'tsaN', 'ثً', output_text)
        output_text = re.sub(r'lloo', 'للّٰ', output_text)
        output_text = re.sub(r'llo', 'للّٰ', output_text)
        output_text = re.sub(r'tta', 'تَّ', output_text)
        output_text = re.sub(r'ttu', 'تُّ', output_text)
        output_text = re.sub(r'tti', 'تِّ', output_text)
        output_text = re.sub(r'bbu', 'بُّ', output_text)
        output_text = re.sub(r'bbi', 'بِّ', output_text)
        output_text = re.sub(r'bba', 'بَّ', output_text)
        output_text = re.sub(r'ddu', 'دُّ', output_text)
        output_text = re.sub(r'ddi', 'دِّ', output_text)
        output_text = re.sub(r'dda', 'دَّ', output_text)
        output_text = re.sub(r'ffu', 'فُّ', output_text)
        output_text = re.sub(r'ffi', 'فِّ', output_text)
        output_text = re.sub(r'ffa', 'فَّ', output_text)
        output_text = re.sub(r'hhu', 'هُّ', output_text)
        output_text = re.sub(r'hhi', 'هِّ', output_text)
        output_text = re.sub(r'hha', 'هَّ', output_text)
        output_text = re.sub(r'jju', 'جُّ', output_text)
        output_text = re.sub(r'jji', 'جِّ', output_text)
        output_text = re.sub(r'jja', 'جَّ', output_text)
        output_text = re.sub(r'kku', 'كُّ', output_text)
        output_text = re.sub(r'kki', 'كِّ', output_text)
        output_text = re.sub(r'kka', 'كَّ', output_text)
        output_text = re.sub(r'llu', 'لُّ', output_text)
        output_text = re.sub(r'lli', 'لِّ', output_text)
        output_text = re.sub(r'lla', 'لَّ', output_text)
        output_text = re.sub(r'mmu', 'مُّ', output_text)
        output_text = re.sub(r'mmi', 'مِّ', output_text)
        output_text = re.sub(r'mma', 'مَّ', output_text)
        output_text = re.sub(r'nnu', 'نُّ', output_text)
        output_text = re.sub(r'nni', 'نِّ', output_text)
        output_text = re.sub(r'nna', 'نَّ', output_text)
        output_text = re.sub(r'qqu', 'قُّ', output_text)
        output_text = re.sub(r'qqi', 'قِّ', output_text)
        output_text = re.sub(r'qqo', 'قَّ', output_text)
        output_text = re.sub(r'rru', 'رُّ', output_text)
        output_text = re.sub(r'rri', 'رِّ', output_text)
        output_text = re.sub(r'rra', 'رَّ', output_text)
        output_text = re.sub(r'ssu', 'سُّ', output_text)
        output_text = re.sub(r'ssi', 'سِّ', output_text)
        output_text = re.sub(r'ssa', 'سَّ', output_text)
        output_text = re.sub(r'wwu', 'وُّ', output_text)
        output_text = re.sub(r'wwi', 'وِّ', output_text)
        output_text = re.sub(r'wwa', 'وَّ', output_text)
        output_text = re.sub(r'yyu', 'يُّ', output_text)
        output_text = re.sub(r'yyi', 'يِّ', output_text)
        output_text = re.sub(r'yya', 'يَّ', output_text)
        output_text = re.sub(r'zzu', 'زُّ', output_text)
        output_text = re.sub(r'zzi', 'زِّ', output_text)
        output_text = re.sub(r'zza', 'زَّ', output_text)
        output_text = re.sub(r'\'\'u', 'عُّ', output_text)
        output_text = re.sub(r'\'\'i', 'عِّ', output_text)
        output_text = re.sub(r'\'\'a', 'عَّ', output_text)
        output_text = re.sub(r'tuu', 'تُوْ', output_text)
        output_text = re.sub(r'tii', 'تِيْ', output_text)
        output_text = re.sub(r'taa', 'تَا', output_text)
        output_text = re.sub(r'tuN', 'تٌ', output_text)
        output_text = re.sub(r'tiN', 'تٍ', output_text)
        output_text = re.sub(r'taN', 'تً', output_text)
        output_text = re.sub(r'buu', 'بُوْ', output_text)
        output_text = re.sub(r'bii', 'بِيْ', output_text)
        output_text = re.sub(r'baa', 'بَا', output_text)
        output_text = re.sub(r'buN', 'بٌ', output_text)
        output_text = re.sub(r'biN', 'بٍ', output_text)
        output_text = re.sub(r'baN', 'بً', output_text)
        output_text = re.sub(r'duu', 'دُوْ', output_text)
        output_text = re.sub(r'dii', 'دِيْ', output_text)
        output_text = re.sub(r'daa', 'دَا', output_text)
        output_text = re.sub(r'duN', 'دٌ', output_text)
        output_text = re.sub(r'diN', 'دٍ', output_text)
        output_text = re.sub(r'daN', 'دً', output_text)
        output_text = re.sub(r'fuu', 'فُوْ', output_text)
        output_text = re.sub(r'fii', 'فِيْ', output_text)
        output_text = re.sub(r'faa', 'فَا', output_text)
        output_text = re.sub(r'fuN', 'فٌ', output_text)
        output_text = re.sub(r'fiN', 'فٍ', output_text)
        output_text = re.sub(r'faN', 'فً', output_text)
        output_text = re.sub(r'huu', 'هُوْ', output_text)
        output_text = re.sub(r'hii', 'هِيْ', output_text)
        output_text = re.sub(r'haa', 'هَا', output_text)
        output_text = re.sub(r'huN', 'هٌ', output_text)
        output_text = re.sub(r'hiN', 'هٍ', output_text)
        output_text = re.sub(r'haN', 'هً', output_text)
        output_text = re.sub(r'juu', 'جُوْ', output_text)
        output_text = re.sub(r'jii', 'جِيْ', output_text)
        output_text = re.sub(r'jaa', 'جَا', output_text)
        output_text = re.sub(r'juN', 'جٌ', output_text)
        output_text = re.sub(r'jiN', 'جٍ', output_text)
        output_text = re.sub(r'jaN', 'جً', output_text)
        output_text = re.sub(r'kuu', 'كُوْ', output_text)
        output_text = re.sub(r'kii', 'كِيْ', output_text)
        output_text = re.sub(r'kaa', 'كَا', output_text)
        output_text = re.sub(r'kuN', 'كٌ', output_text)
        output_text = re.sub(r'kiN', 'كٍ', output_text)
        output_text = re.sub(r'kaN', 'كً', output_text)
        output_text = re.sub(r'luu', 'لُوْ', output_text)
        output_text = re.sub(r'lii', 'لِيْ', output_text)
        output_text = re.sub(r'laa', 'لَا', output_text)
        output_text = re.sub(r'luN', 'لٌ', output_text)
        output_text = re.sub(r'liN', 'لٍ', output_text)
        output_text = re.sub(r'laN', 'لً', output_text)
        output_text = re.sub(r'muu', 'مُوْ', output_text)
        output_text = re.sub(r'mii', 'مِيْ', output_text)
        output_text = re.sub(r'maa', 'مَا', output_text)
        output_text = re.sub(r'muN', 'مٌ', output_text)
        output_text = re.sub(r'miN', 'مٍ', output_text)
        output_text = re.sub(r'maN', 'مً', output_text)
        output_text = re.sub(r'nuu', 'نُوْ', output_text)
        output_text = re.sub(r'nii', 'نِيْ', output_text)
        output_text = re.sub(r'naa', 'نَا', output_text)
        output_text = re.sub(r'nuN', 'نٌ', output_text)
        output_text = re.sub(r'niN', 'نٍ', output_text)
        output_text = re.sub(r'naN', 'نً', output_text)
        output_text = re.sub(r'quu', 'قُوْ', output_text)
        output_text = re.sub(r'qii', 'قِيْ', output_text)
        output_text = re.sub(r'qoo', 'قَا', output_text)
        output_text = re.sub(r'quN', 'قٌ', output_text)
        output_text = re.sub(r'qiN', 'قٍ', output_text)
        output_text = re.sub(r'qon', 'قً', output_text)
        output_text = re.sub(r'ruu', 'رُوْ', output_text)
        output_text = re.sub(r'rii', 'رِيْ', output_text)
        output_text = re.sub(r'roo', 'رَا', output_text)
        output_text = re.sub(r'ruN', 'رٌ', output_text)
        output_text = re.sub(r'riN', 'رٍ', output_text)
        output_text = re.sub(r'ron', 'رً', output_text)
        output_text = re.sub(r'suu', 'سُوْ', output_text)
        output_text = re.sub(r'sii', 'سِيْ', output_text)
        output_text = re.sub(r'saa', 'سَا', output_text)
        output_text = re.sub(r'suN', 'سٌ', output_text)
        output_text = re.sub(r'siN', 'سٍ', output_text)
        output_text = re.sub(r'saN', 'سً', output_text)
        output_text = re.sub(r'wuu', 'وُوْ', output_text)
        output_text = re.sub(r'wii', 'وِيْ', output_text)
        output_text = re.sub(r'waa', 'وَا', output_text)
        output_text = re.sub(r'wuN', 'وٌ', output_text)
        output_text = re.sub(r'wiN', 'وٍ', output_text)
        output_text = re.sub(r'waN', 'وً', output_text)
        output_text = re.sub(r'yuu', 'يُوْ', output_text)
        output_text = re.sub(r'yii', 'يِيْ', output_text)
        output_text = re.sub(r'yaa', 'يَا', output_text)
        output_text = re.sub(r'yuN', 'يٌ', output_text)
        output_text = re.sub(r'yiN', 'يٍ', output_text)
        output_text = re.sub(r'yaN', 'يً', output_text)
        output_text = re.sub(r'zuu', 'زُوْ', output_text)
        output_text = re.sub(r'zii', 'زِيْ', output_text)
        output_text = re.sub(r'zaa', 'زَا', output_text)
        output_text = re.sub(r'zuN', 'زٌ', output_text)
        output_text = re.sub(r'ziN', 'زٍ', output_text)
        output_text = re.sub(r'zaN', 'زً', output_text)
        output_text = re.sub(r'\'uu', 'عُوْ', output_text)
        output_text = re.sub(r'\'ii', 'عِيْ', output_text)
        output_text = re.sub(r'\'aa', 'عَا', output_text)
        output_text = re.sub(r'\'uN', 'عٌ', output_text)
        output_text = re.sub(r'\'iN', 'عٍ', output_text)
        output_text = re.sub(r'\'aN', 'عً', output_text)
        output_text = re.sub(r'chu', 'خُ', output_text)
        output_text = re.sub(r'chi', 'خِ', output_text)
        output_text = re.sub(r'cho', 'خَ', output_text)
        output_text = re.sub(r'dhu', 'ظُ', output_text)
        output_text = re.sub(r'dhi', 'ظِ', output_text)
        output_text = re.sub(r'dho', 'ظَ', output_text)
        output_text = re.sub(r'dlu', 'ضُ', output_text)
        output_text = re.sub(r'dli', 'ضِ', output_text)
        output_text = re.sub(r'dlo', 'ضَ', output_text)
        output_text = re.sub(r'dzu', 'ذُ', output_text)
        output_text = re.sub(r'dzi', 'ذِ', output_text)
        output_text = re.sub(r'dza', 'ذَ', output_text)
        output_text = re.sub(r'ghu', 'غُ', output_text)
        output_text = re.sub(r'ghi', 'غِ', output_text)
        output_text = re.sub(r'gho', 'غَ', output_text)
        output_text = re.sub(r'khu', 'حُ', output_text)
        output_text = re.sub(r'khi', 'حِ', output_text)
        output_text = re.sub(r'kha', 'حَ', output_text)
        output_text = re.sub(r'shu', 'صُ', output_text)
        output_text = re.sub(r'shi', 'صِ', output_text)
        output_text = re.sub(r'sho', 'صَ', output_text)
        output_text = re.sub(r'syu', 'شُ', output_text)
        output_text = re.sub(r'syi', 'شِ', output_text)
        output_text = re.sub(r'sya', 'شَ', output_text)
        output_text = re.sub(r'thu', 'طُ', output_text)
        output_text = re.sub(r'thi', 'طِ', output_text)
        output_text = re.sub(r'tho', 'طَ', output_text)
        output_text = re.sub(r'tsu', 'ثُ', output_text)
        output_text = re.sub(r'tsi', 'ثِ', output_text)
        output_text = re.sub(r'tsa', 'ثَ', output_text)
        output_text = re.sub(r'tu', 'تُ', output_text)
        output_text = re.sub(r'ti', 'تِ', output_text)
        output_text = re.sub(r'ta', 'تَ', output_text)
        output_text = re.sub(r'bu', 'بُ', output_text)
        output_text = re.sub(r'bi', 'بِ', output_text)
        output_text = re.sub(r'ba', 'بَ', output_text)
        output_text = re.sub(r'du', 'دُ', output_text)
        output_text = re.sub(r'di', 'دِ', output_text)
        output_text = re.sub(r'da', 'دَ', output_text)
        output_text = re.sub(r'fu', 'فُ', output_text)
        output_text = re.sub(r'fi', 'فِ', output_text)
        output_text = re.sub(r'fa', 'فَ', output_text)
        output_text = re.sub(r'hu', 'هُ', output_text)
        output_text = re.sub(r'hi', 'هِ', output_text)
        output_text = re.sub(r'ha', 'هَ', output_text)
        output_text = re.sub(r'ju', 'جُ', output_text)
        output_text = re.sub(r'ji', 'جِ', output_text)
        output_text = re.sub(r'ja', 'جَ', output_text)
        output_text = re.sub(r'ku', 'كُ', output_text)
        output_text = re.sub(r'ki', 'كِ', output_text)
        output_text = re.sub(r'ka', 'كَ', output_text)
        output_text = re.sub(r'lu', 'لُ', output_text)
        output_text = re.sub(r'li', 'لِ', output_text)
        output_text = re.sub(r'la', 'لَ', output_text)
        output_text = re.sub(r'mu', 'مُ', output_text)
        output_text = re.sub(r'mi', 'مِ', output_text)
        output_text = re.sub(r'ma', 'مَ', output_text)
        output_text = re.sub(r'nu', 'نُ', output_text)
        output_text = re.sub(r'ni', 'نِ', output_text)
        output_text = re.sub(r'na', 'نَ', output_text)
        output_text = re.sub(r'qu', 'قُ', output_text)
        output_text = re.sub(r'qi', 'قِ', output_text)
        output_text = re.sub(r'qo', 'قَ', output_text)
        output_text = re.sub(r'ru', 'رُ', output_text)
        output_text = re.sub(r'ri', 'رِ', output_text)
        output_text = re.sub(r'ro', 'رَ', output_text)
        output_text = re.sub(r'su', 'سُ', output_text)
        output_text = re.sub(r'si', 'سِ', output_text)
        output_text = re.sub(r'sa', 'سَ', output_text)
        output_text = re.sub(r'wu', 'وُ', output_text)
        output_text = re.sub(r'wi', 'وِ', output_text)
        output_text = re.sub(r'wa', 'وَ', output_text)
        output_text = re.sub(r'yu', 'يُ', output_text)
        output_text = re.sub(r'yi', 'يِ', output_text)
        output_text = re.sub(r'ya', 'يَ', output_text)
        output_text = re.sub(r'zu', 'زُ', output_text)
        output_text = re.sub(r'zi', 'زِ', output_text)
        output_text = re.sub(r'za', 'زَ', output_text)
        output_text = re.sub(r'\'u', 'عُ', output_text)
        output_text = re.sub(r'\'i', 'عِ', output_text)
        output_text = re.sub(r'\'a', 'عَ', output_text)
        output_text = re.sub(r'ch', 'خْ', output_text)
        output_text = re.sub(r'dh', 'ظْ', output_text)
        output_text = re.sub(r'dl', 'ضْ', output_text)
        output_text = re.sub(r'dz', 'ذْ', output_text)
        output_text = re.sub(r'gh', 'غْ', output_text)
        output_text = re.sub(r'kh', 'حْ', output_text)
        output_text = re.sub(r'sh', 'صْ', output_text)
        output_text = re.sub(r'sy', 'شْ', output_text)
        output_text = re.sub(r'th', 'طْ', output_text)
        output_text = re.sub(r'ts', 'ثْ', output_text)
        output_text = re.sub(r't', 'تْ', output_text)
        output_text = re.sub(r'b', 'بْ', output_text)
        output_text = re.sub(r'd', 'دْ', output_text)
        output_text = re.sub(r'f', 'فْ', output_text)
        output_text = re.sub(r'h', 'هْ', output_text)
        output_text = re.sub(r'j', 'جْ', output_text)
        output_text = re.sub(r'k', 'كْ', output_text)
        output_text = re.sub(r'l', 'لْ', output_text)
        output_text = re.sub(r'm', 'مْ', output_text)
        output_text = re.sub(r'n', 'نْ', output_text)
        output_text = re.sub(r'q', 'قْ', output_text)
        output_text = re.sub(r'r', 'رْ', output_text)
        output_text = re.sub(r's', 'سْ', output_text)
        output_text = re.sub(r'w', 'وْ', output_text)
        output_text = re.sub(r'y', 'يْ', output_text)
        output_text = re.sub(r'z', 'زْ', output_text)
        output_text = re.sub(r'\'', 'عْ', output_text)
        output_text = re.sub(r'AN', 'ءً', output_text)
        output_text = re.sub(r'IN', 'ءٍ', output_text)
        output_text = re.sub(r'UN', 'ءٌ', output_text)
        output_text = re.sub(r'A', 'ءَ', output_text)
        output_text = re.sub(r'I', 'ءِ', output_text)
        output_text = re.sub(r'U', 'ءُ', output_text)
        output_text = re.sub(r'aN', 'أً', output_text)
        output_text = re.sub(r'iN', 'إٍ', output_text)
        output_text = re.sub(r'uN', 'أٌ', output_text)
        output_text = re.sub(r'a', 'أَ', output_text)
        output_text = re.sub(r'i', 'إِ', output_text)
        output_text = re.sub(r'u', 'أُ', output_text)
        output_text = re.sub(r';', '', output_text)
        output_text = re.sub(r'saw', 'ﷺ', output_text)
        # Tampilkan hasil transliterasi
        self.text_output.setPlainText(output_text)
        self.text_output.verticalScrollBar().setValue(0)

    def copy_output(self):
        output_text = self.text_output.toPlainText()
        if output_text:
            QApplication.clipboard().setText(output_text)
            notification = NotificationDialog("\nHasil transliterasi telah disalin.", dark_mode=self.dark_mode, parent=self)
            notification.exec_()
        else:
            notification = NotificationDialog("\nTidak ada teks untuk disalin.", dark_mode=self.dark_mode, parent=self)
            notification.exec_()

    def reset_text(self):
        self.text_input.clear()
        self.text_output.clear()
        self.text_input.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Transliterator()
    window.show()
    sys.exit(app.exec_())
