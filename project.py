import os
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import (QApplication, QGroupBox, QMainWindow, QFileDialog, QInputDialog, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog, QGridLayout, QListWidget, QTextEdit)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFilter
import json
import sys


class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Калькулятор")
        self.setFixedSize(750, 500)

        self.expression_line_edit = QLineEdit()
        self.result_label = QLabel()

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.expression_line_edit, 0, 0, 1, 4)
        grid_layout.addWidget(self.result_label, 1, 0, 1, 4)

        row = 2
        col = 0
        for button_text in buttons:
            button = QPushButton(button_text)
            button.clicked.connect(lambda _, text=button_text: self.append_to_expression(text))
            grid_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        layout = QVBoxLayout()
        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def append_to_expression(self, text):
        current_expression = self.expression_line_edit.text()
        last_char = current_expression[-1:] if current_expression else ""
        if text == "=":
            self.calculate_expression()
        elif text in ['*', '/', '-', '+', '.'] and last_char in ['*', '/', '-', '+', '.']:
            return
        else:
            self.expression_line_edit.setText(current_expression + text)

    def calculate_expression(self):
        expression = self.expression_line_edit.text()
        try:
            result = eval(expression)
            self.result_label.setText(str(result))
        except Exception as e:
            self.result_label.setText("Error")




class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Поиск")
        self.setFixedSize(750, 500)

        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Поиск")
        self.web_view = QWebEngineView()

        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.search_button)
        layout.addWidget(self.web_view)

        self.setLayout(layout)

        self.search_button.clicked.connect(self.perform_search)

    def perform_search(self):
        search_query = self.search_bar.text()
        if search_query:
            url = QUrl("https://www.google.com/search?q={}".format(search_query))
            self.web_view.load(url)


def search_button_clicked():
    if layout_qgb2.count() > 0:
        # Очищаем qgb2
        while layout_qgb2.count() > 0:
            item = layout_qgb2.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    else:
        # Добавляем поисковик в qgb2
        search_widget = SearchWidget()
        layout_qgb2.addWidget(search_widget)


class FinanceWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Учет финансов")
        self.setFixedSize(800, 600)

        self.shopping_line_edit = QLineEdit()
        self.transport_line_edit = QLineEdit()
        self.cafe_line_edit = QLineEdit()
        self.home_line_edit = QLineEdit()
        self.purchases_line_edit = QLineEdit()
        self.total_label = QLabel()

        calculate_button = QPushButton("Рассчитать")
        calculate_button.clicked.connect(self.calculate_expenses)

        layout = QVBoxLayout()
        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("Шоппинг:"), 0, 0, Qt.AlignTop | Qt.AlignLeft)
        grid_layout.addWidget(self.shopping_line_edit, 1, 0, Qt.AlignTop | Qt.AlignRight)
        grid_layout.addWidget(QLabel("Транспорт:"), 0, 1, Qt.AlignTop | Qt.AlignCenter)
        grid_layout.addWidget(self.transport_line_edit, 1, 1, Qt.AlignTop | Qt.AlignCenter)
        grid_layout.addWidget(QLabel("Кафе:"), 0, 2, Qt.AlignTop | Qt.AlignRight)
        grid_layout.addWidget(self.cafe_line_edit, 1, 2, Qt.AlignTop | Qt.AlignRight)
        grid_layout.addWidget(QLabel("Дом:"), 2, 0, Qt.AlignVCenter | Qt.AlignLeft)
        grid_layout.addWidget(self.home_line_edit, 3, 0, Qt.AlignVCenter | Qt.AlignRight)
        grid_layout.addWidget(QLabel("Покупки:"), 2, 2, Qt.AlignVCenter | Qt.AlignRight)
        grid_layout.addWidget(self.purchases_line_edit, 3, 2, Qt.AlignVCenter | Qt.AlignRight)
        grid_layout.addWidget(self.total_label, 4, 1, Qt.AlignCenter)
        grid_layout.addWidget(calculate_button, 5, 1, Qt.AlignCenter)

        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def calculate_expenses(self):
        shopping_expenses = float(self.shopping_line_edit.text()) if self.shopping_line_edit.text() else 0.0
        transport_expenses = float(self.transport_line_edit.text()) if self.transport_line_edit.text() else 0.0
        cafe_expenses = float(self.cafe_line_edit.text()) if self.cafe_line_edit.text() else 0.0
        home_expenses = float(self.home_line_edit.text()) if self.home_line_edit.text() else 0.0
        purchases_expenses = float(self.purchases_line_edit.text()) if self.purchases_line_edit.text() else 0.0

        total_expenses = shopping_expenses + transport_expenses + cafe_expenses + home_expenses + purchases_expenses
        self.total_label.setText("Сумма: {}".format(total_expenses))


class NotesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_notes()

    def initUI(self):
        self.setWindowTitle('Заметки')

        # Виджеты для заметок
        self.list_notes = QListWidget()
        self.list_notes_label = QLabel('Список заметок')

        self.button_note_create = QPushButton('Створити замітку')
        self.button_note_del = QPushButton('Видалити замітку')
        self.button_note_save = QPushButton('Зберегти замітку')

        # Виджеты для тегов
        self.field_tag = QLineEdit('')
        self.field_tag.setPlaceholderText('Введіть тег...')
        self.field_text = QTextEdit()

        self.button_tag_add = QPushButton('Додати до замітки')
        self.button_tag_del = QPushButton('Відкріпити від замітки')
        self.button_tag_search = QPushButton('Шукати замітки за тегом')

        self.list_tags = QListWidget()
        self.list_tags_label = QLabel('Список тегів')

        # Лейауты
        layout_notes = QHBoxLayout()
        col_1 = QVBoxLayout()
        col_1.addWidget(self.field_text)

        col_2 = QVBoxLayout()
        col_2.addWidget(self.list_notes_label)
        col_2.addWidget(self.list_notes)
        row_1 = QHBoxLayout()
        row_1.addWidget(self.button_note_create)
        row_1.addWidget(self.button_note_del)
        row_2 = QHBoxLayout()
        row_2.addWidget(self.button_note_save)
        col_2.addLayout(row_1)
        col_2.addLayout(row_2)

        col_2.addWidget(self.list_tags_label)
        col_2.addWidget(self.list_tags)
        col_2.addWidget(self.field_tag)
        row_3 = QHBoxLayout()
        row_3.addWidget(self.button_tag_add)
        row_3.addWidget(self.button_tag_del)
        row_4 = QHBoxLayout()
        row_4.addWidget(self.button_tag_search)
        col_2.addLayout(row_3)
        col_2.addLayout(row_4)

        layout_notes.addLayout(col_1, stretch=2)
        layout_notes.addLayout(col_2, stretch=1)
        self.setLayout(layout_notes)

        # Подключение сигналов к слотам
        self.button_note_create.clicked.connect(self.add_note)
        self.list_notes.itemClicked.connect(self.show_note)
        self.button_note_save.clicked.connect(self.save_note)
        self.button_note_del.clicked.connect(self.del_note)
        self.button_tag_add.clicked.connect(self.add_tag)
        self.button_tag_del.clicked.connect(self.del_tag)
        self.button_tag_search.clicked.connect(self.search_tag)

    def load_notes(self):
        try:
            with open("notes_data.json", "r", encoding="utf-8") as file:
                self.notes = json.load(file)
        except FileNotFoundError:
            self.notes = {}

        self.list_notes.clear()
        self.list_tags.clear()

        self.list_notes.addItems(self.notes.keys())

    def save_notes(self):
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(self.notes, file, ensure_ascii=False)

    def add_note(self):
        note_name, ok = QInputDialog.getText(self, "Добавить заметку", "Название заметки:")
        if ok and note_name != "":
            self.notes[note_name] = {"текст": "", "теги": []}
            self.list_notes.addItem(note_name)
            self.list_tags.addItems(self.notes[note_name]["теги"])
            self.save_notes()

    def show_note(self):
        if self.list_notes.selectedItems():
            key = self.list_notes.selectedItems()[0].text()
            self.field_text.setText(self.notes[key]["текст"])
            self.list_tags.clear()
            self.list_tags.addItems(self.notes[key]["теги"])

    def save_note(self):
        if self.list_notes.selectedItems():
            key = self.list_notes.selectedItems()[0].text()
            self.notes[key]["текст"] = self.field_text.toPlainText()
            self.save_notes()

    def del_note(self):
        if self.list_notes.selectedItems():
            key = self.list_notes.selectedItems()[0].text()
            del self.notes[key]
            self.list_notes.clear()
            self.list_tags.clear()
            self.field_text.clear()
            self.list_notes.addItems(self.notes)
            self.save_notes()

    def add_tag(self):
        if self.list_notes.selectedItems():
            key = self.list_notes.selectedItems()[0].text()
            tag = self.field_tag.text()
            if not tag in self.notes[key]["теги"]:
                self.notes[key]["теги"].append(tag)
                self.field_tag.clear()
                self.save_notes()

    def del_tag(self):
        if self.list_notes.selectedItems():
            key = self.list_notes.selectedItems()[0].text()
            if self.list_tags.selectedItems():
                tag = self.list_tags.selectedItems()[0].text()
                self.notes[key]["теги"].remove(tag)
                self.list_tags.clear()
                self.list_tags.addItems(self.notes[key]["теги"])
                self.save_notes()

    def search_tag(self):
        tag = self.field_tag.text()
        if self.button_tag_search.text() == "Шукати замітки за тегом" and tag:
            notes_f = {}
            for note in self.notes:
                if tag in self.notes[note]["теги"]:
                    notes_f[note] = self.notes[note]
            self.button_tag_search.setText("Скинути пошук")
            self.list_notes.clear()
            self.list_tags.clear()
            self.list_notes.addItems(notes_f)
        else:
            self.field_tag.clear()
            self.list_notes.clear()
            self.list_notes.addItems(self.notes)
            self.button_tag_search.setText("Шукати замітки за тегом")



class PhotoEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Editor")
        self.setGeometry(100, 100, 600, 400)

        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        
        self.open_button = QPushButton("Открыть картинку")
        self.grayscale_button = QPushButton("Ч/Б")
        self.rotate_right_button = QPushButton("Вправо")
        self.rotate_left_button = QPushButton("Влево")
        self.mirror_button = QPushButton("Отзеркалить")
        self.sharpen_button = QPushButton("Резкость")
        self.save_button = QPushButton("Сохранить картинку")

        
        self.open_button.clicked.connect(self.open_image)
        self.grayscale_button.clicked.connect(self.convert_to_grayscale)
        self.rotate_right_button.clicked.connect(self.rotate_right)
        self.rotate_left_button.clicked.connect(self.rotate_left)
        self.mirror_button.clicked.connect(self.mirror)
        self.sharpen_button.clicked.connect(self.sharpen)
        self.save_button.clicked.connect(self.save_image)

        
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.open_button)
        buttons_layout.addWidget(self.grayscale_button)
        buttons_layout.addWidget(self.rotate_right_button)
        buttons_layout.addWidget(self.rotate_left_button)
        buttons_layout.addWidget(self.mirror_button)
        buttons_layout.addWidget(self.sharpen_button)
        buttons_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(buttons_layout)

        
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        
        self.image = None

    def open_image(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")

        if file_path:
            
            self.image = cv2.imread(file_path)

            
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            
            self.display_image()

    def display_image(self):
        
        height, width, channel = self.image.shape
        bytes_per_line = 3 * width
        q_image = QImage(self.image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        
        q_pixmap = QPixmap.fromImage(q_image).scaled(self.image_label.width(), self.image_label.height(),
                                                     Qt.KeepAspectRatio)

        
        self.image_label.setPixmap(q_pixmap)

    def convert_to_grayscale(self):
        if self.image is not None:
            
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

            
            self.image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)

            
            self.display_image()

    def rotate_right(self):
        if self.image is not None:
            
            self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)

            
            self.display_image()

    def rotate_left(self):
        if self.image is not None:
            
            self.image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)

            
            self.display_image()

    def mirror(self):
        if self.image is not None:
            
            self.image = cv2.flip(self.image, 1)

            
            self.display_image()

    def sharpen(self):
        if self.image is not None:
            
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            self.image = cv2.filter2D(self.image, -1, kernel)

            
            self.display_image()

    def save_image(self):
        if self.image is not None:
            
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg *.bmp)")

            if file_path:
                
                cv2.imwrite(file_path, self.image)
                print("Image saved successfully!")



def notes_button_clicked():
    if layout_qgb2.count() > 0:
        # Очищаем qgb2
        while layout_qgb2.count() > 0:
            item = layout_qgb2.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    else:
        # Добавляем поисковик в qgb2
        notes_widget = NotesWidget()
        layout_qgb2.addWidget(notes_widget)




app = QApplication([])
assistant = QWidget()
assistant.setWindowTitle("My Virtual Assistant")
assistant.setFixedSize(1000, 600)

qgb1 = QGroupBox()
qgb2 = QGroupBox()
qgb1.setMaximumSize(200, 600)
qgb2.setMaximumSize(800, 600)

main_layout_1 = QVBoxLayout()
main_layout_2 = QHBoxLayout()

# Кнопки для qgb1
calculator_button = QPushButton("Калькулятор")
finance_button = QPushButton("Учет финансов")
search_button = QPushButton("Поисковик")
notes_button = QPushButton("Заметки")
photo_editor_button = QPushButton("Фото редактор")

layout_qgb1 = QVBoxLayout()
layout_qgb1.addWidget(calculator_button)
layout_qgb1.addSpacing(10)  # Отступ между кнопками
layout_qgb1.addWidget(finance_button)
layout_qgb1.addSpacing(10)
layout_qgb1.addWidget(search_button)
layout_qgb1.addSpacing(10)
layout_qgb1.addWidget(notes_button)
layout_qgb1.addSpacing(10)
layout_qgb1.addWidget(photo_editor_button)

qgb1.setLayout(layout_qgb1)

layout_qgb2 = QVBoxLayout()
qgb2.setLayout(layout_qgb2)

main_layout_2.addWidget(qgb1)
main_layout_2.addWidget(qgb2)
main_layout_1.addLayout(main_layout_2)

assistant.setLayout(main_layout_1)


def photoeditor_button_clicked():
    if layout_qgb2.count() > 0:
        # Очищаем qgb2
        while layout_qgb2.count() > 0:
            item = layout_qgb2.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    else:
        # Добавляем поисковик в qgb2
        photo_widget = PhotoEditor()
        layout_qgb2.addWidget(photo_widget)


def calculator_button_clicked():
    if layout_qgb2.count() > 0:
        # Очищаем qgb2
        while layout_qgb2.count() > 0:
            item = layout_qgb2.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    else:
        # Добавляем калькулятор в qgb2
        calculator_widget = CalculatorWidget()
        layout_qgb2.addWidget(calculator_widget)

def finance_button_clicked():
    if layout_qgb2.count() > 0:
        # Очищаем qgb2
        while layout_qgb2.count() > 0:
            item = layout_qgb2.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    else:
        # Добавляем учет финансов в qgb2
        finance_widget = FinanceWidget()
        layout_qgb2.addWidget(finance_widget)


# Подключаем функции к кнопкам
photo_editor_button.clicked.connect(photoeditor_button_clicked)
notes_button.clicked.connect(notes_button_clicked)
calculator_button.clicked.connect(calculator_button_clicked)
finance_button.clicked.connect(finance_button_clicked)
search_button.clicked.connect(search_button_clicked)
assistant.show()
app.exec_()