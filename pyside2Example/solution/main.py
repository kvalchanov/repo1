from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMainWindow, QButtonGroup
from PySide2.QtGui import QIcon, QImage, QBrush, QPainter, QPixmap, QWindow, QColor, QFont
from PySide2.QtCore import QSize, Qt, QRect
import json

with open('characters_fixed.json') as file:
    chars = json.load(file)

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Family Guy')
        self.setFixedSize(750, 750)

        main_layout = QHBoxLayout()
        self.buttons_group = QButtonGroup()

        buttons_container = QWidget()
        buttons_container.setFixedSize(240, 730)

        desc_container = QWidget()
        desc_container.setFixedSize(480, 730)

        buttons_layout = QVBoxLayout()
        buttons_layout.setContentsMargins(5, 5, 5, 5)
        self._create_buttons(chars, buttons_layout)
        self.buttons_group.buttonClicked.connect(self._button_click)

        btns_widget = QWidget()
        btns_widget.setStyleSheet('border: 0px;')
        btns_widget.setLayout(buttons_layout)
        btns_widget.setParent(buttons_container)

        self.pic_name_and_role_layout = QHBoxLayout()
        self.name_and_role_layout = QVBoxLayout()
        
        self.picture = QLabel()
        self.picture.setStyleSheet('border: 0px;')

        self.name = QLabel()
        self.name.setStyleSheet('border: 0px; margin: 20px;')
        self.name.setFont(QFont('Times', 20))

        self.role = QLabel()
        self.role.setStyleSheet('border: 0px; margin: 20px;')
        self.role.setFont(QFont('Times', 15, italic=True))

        self.name_and_role_layout.addWidget(self.name, alignment = Qt.AlignTop | Qt.AlignRight)
        self.name_and_role_layout.addWidget(self.role, alignment = Qt.AlignBottom | Qt.AlignRight)
        self.pic_name_and_role_layout.addWidget(self.picture)
        self.pic_name_and_role_layout.addLayout(self.name_and_role_layout)

        self.desc = QLabel()
        self.desc.setWordWrap(True)
        self.desc.setFixedSize(460, 300)
        self.desc.setFont(QFont('Times', 12))
        self.desc.setContentsMargins(5, 5, 5, 5)
        self.desc.setAlignment(Qt.AlignTop)

        desc_layout = QVBoxLayout()
        desc_layout.addLayout(self.pic_name_and_role_layout)
        desc_layout.addWidget(self.desc, alignment=Qt.AlignRight)

        desc_widget = QWidget()
        desc_widget.setContentsMargins(5, 5, 5, 5)
        desc_widget.setStyleSheet('border: 0px; margin: 5px;')
        desc_widget.setParent(desc_container)
        desc_container.setLayout(desc_layout)

        main_layout.addWidget(buttons_container, alignment=Qt.AlignTop)
        main_layout.addWidget(desc_container, alignment=Qt.AlignTop)

        widget = QWidget()
        widget.setLayout(main_layout)
        widget.setStyleSheet('border:1px solid black;')

        self.setCentralWidget(widget)

    def _create_buttons(self, data: list, layout: QVBoxLayout):
        for char in data:
            full_name = char['first_name'] + ' ' + char['last_name']
            icon_path = char['pic']
            pixmap = self._crop_icon(icon_path)
            button = QPushButton(icon=QIcon(pixmap), text=full_name)
            button.setFont(QFont('Times', 20))
            button.setFixedSize(230, 75)
            button.setIconSize(QSize(60, 60))
            button.setStyleSheet('border: 1px solid black;')
            layout.addWidget(button, alignment=Qt.AlignTop)
            self.buttons_group.addButton(button)

    def _button_click(self, button):
        names = button.text().split(' ')
        for char in chars:
            if char['first_name'] == names[0] and char['last_name'] == names[1]:
                text = char['bio']
                picture_pixmap = QPixmap(char['pic'])
                break
        self.picture.setPixmap(picture_pixmap)
        self.name.setText(button.text())
        self.role.setText(char['position'])
        self.desc.setText(text)

    def _crop_icon(self, path, imgtype ='png', size = 64):
        with open(path,'rb') as file:
            imgdata = file.read()

        image = QImage.fromData(imgdata, imgtype)
    
        image.convertToFormat(QImage.Format_ARGB32)
    
        height = image.height()
        width = image.width()
        rect = QRect(0, 0, width, height / 2)
        image = image.copy(rect)
    
        out_img = QImage(width, height / 2, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)
    
        brush = QBrush(image)
    
        painter = QPainter(out_img)
        painter.setBrush(brush)
    
        painter.setPen(QColor('solid black'))
    
        painter.drawRect(0, 0, width, height / 2)
    
        painter.end()
    
        pr = QWindow().devicePixelRatio()
        pm = QPixmap.fromImage(out_img)
        pm.setDevicePixelRatio(pr)
        size *= pr
        pm = pm.scaled(size, size, Qt.KeepAspectRatio,
                                Qt.SmoothTransformation)
    
        return pm


app = QApplication()
window = Window()
window.show()
app.exec_()