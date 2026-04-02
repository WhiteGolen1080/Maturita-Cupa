from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QGridLayout,
    QMessageBox,
    QListWidget,
    QListWidgetItem
)

from sql import get_data, update_text_color, update_bg_color, update_border_color, update_tags
import os
import json
import string


class Admin(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Profiler Admin App")
        self.rozlozeni = QVBoxLayout()
        self.setLayout(self.rozlozeni)

        self.users_button = QPushButton("To Users")
        self.users_button.clicked.connect(self.openUsers)
        self.rozlozeni.addWidget(self.users_button)

    def openUsers(self):
        self.detail_window = UserSelect()
        self.detail_window.show()

class UserDetail(QWidget):
    def __init__(self, name, role, tags, display, textc, bgc, borderc):
        super().__init__()
        self.name = name
        self.role = role
        self.tags = tags
        self.display = display
        self.textc = textc
        self.bgc = bgc
        self.borderc = borderc
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setWindowTitle(self.name)

        layout = QVBoxLayout()

        username_label = QLabel(f"Display name: {self.display}")
        layout.addWidget(username_label)

        role_label = QLabel(f"Role: {self.role}")
        layout.addWidget(role_label)

        tags_label = QLabel(f"Tags: {self.tags}")
        layout.addWidget(tags_label)

        textc_label = QLabel(f"Text color: {self.textc}")
        layout.addWidget(textc_label)

        textc_label = QLabel(f"BG color: {self.bgc}")
        layout.addWidget(textc_label)

        textc_label = QLabel(f"Border color: {self.borderc}")
        layout.addWidget(textc_label)

        # CHANGE THE STUFF
        #name_label = QLabel("Username:")
        #name_input = QLineEdit()
        #layout.addWidget(name_label)
        #layout.addWidget(name_input)

        tagc_label = QLabel("Change Tags/Bio:")
        self.tagc_input = QLineEdit()
        layout.addWidget(tagc_label)
        layout.addWidget(self.tagc_input)

        self.tagc_input.setText(self.tags)

        tagc_button = QPushButton("Set New Tags/Bio")
        tagc_button.clicked.connect(self.change_user_tag)
        layout.addWidget(tagc_button)

        textc_label = QLabel("Change Text Color:")
        self.textc_input = QLineEdit()
        layout.addWidget(textc_label)
        layout.addWidget(self.textc_input)

        textc_button = QPushButton("Set New Text Color")
        textc_button.clicked.connect(self.change_user_text_color)
        layout.addWidget(textc_button)

        bgc_label = QLabel("Change BG Color:")
        self.bgc_input = QLineEdit()
        layout.addWidget(bgc_label)
        layout.addWidget(self.bgc_input)

        bgc_button = QPushButton("Set New BG Color")
        bgc_button.clicked.connect(self.change_user_bg_color)
        layout.addWidget(bgc_button)

        borderc_label = QLabel("Change Border Color:")
        self.borderc_input = QLineEdit()
        layout.addWidget(borderc_label)
        layout.addWidget(self.borderc_input)

        borderc_button = QPushButton("Set New Border Color")
        borderc_button.clicked.connect(self.change_user_border_color)
        layout.addWidget(borderc_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def change_user_tag(self):
        tag = self.tagc_input.text()
        username = self.name

        #self.textc_input.setText("")
        #self.name_input.setText("")

        update_tags(username, tag)
        print("Tags updated!")
        #UserSelect.refresh_user_list(get_data("MATURITA_CUPA_USERS"))
        #print("List refrehed!")
        self.close()

    def change_user_text_color(self):
        color = self.textc_input.text()
        username = self.name

        #self.textc_input.setText("")
        #self.name_input.setText("")

        update_text_color(username, color)
        print("Color updated!")
        #UserSelect.refresh_user_list(get_data("MATURITA_CUPA_USERS"))
        #print("List refrehed!")
        self.close()

    def change_user_bg_color(self):
        color = self.bgc_input.text()
        username = self.name

        #self.textc_input.setText("")
        #self.name_input.setText("")

        update_bg_color(username, color)
        print("Color updated!")
        #UserSelect.refresh_user_list(get_data("MATURITA_CUPA_USERS"))
        #print("List refrehed!")
        self.close()

    def change_user_border_color(self):
        color = self.borderc_input.text()
        username = self.name

        #self.textc_input.setText("")
        #self.name_input.setText("")

        update_border_color(username, color)
        print("Color updated!")
        #UserSelect.refresh_user_list(get_data("MATURITA_CUPA_USERS"))
        #print("List refrehed!")
        self.close()

class UserSelect(QWidget):
    def __init__(self):
        super().__init__()

        self.data_path = "./static/data/"
        self.users = get_data("MATURITA_CUPA_USERS")

        self.setWindowTitle("Profiler Admin App - Users")
        self.rozlozeni = QVBoxLayout()
        self.setLayout(self.rozlozeni)

        #name_label = QLabel("Name:")
        #self.name_input = QLineEdit()
        #self.rozlozeni.addWidget(name_label)
        #self.rozlozeni.addWidget(self.name_input)

        #ing_label = QLabel("Password:")
        #self.ing_input = QLineEdit()
        #self.rozlozeni.addWidget(ing_label)
        #self.rozlozeni.addWidget(self.ing_input)

        #rec_label = QLabel("role:")
        #self.rec_input = QLineEdit()
        #self.rozlozeni.addWidget(rec_label)
        #self.rozlozeni.addWidget(self.rec_input)

        #self.add_button = QPushButton("Add User")
        #self.add_button.clicked.connect(self.save_user)
        #self.rozlozeni.addWidget(self.add_button)

        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.show_detail)
        self.refresh_user_list(self.users)
        self.rozlozeni.addWidget(self.list_widget)

    def load_user(self, path):
        get_data(path)

    def save_user(self):
        nazev = self.name_input.text()
        ing = self.ing_input.text()
        rec = self.rec_input.text()
        if not nazev or not ing or not rec:
            QMessageBox.warning(self, "Chyba", "Zadejte název, ingredience a postup.")
            return
        if len(ing) < 20 or len(rec) < 20:
            QMessageBox.warning(self, "Chyba",
                                "Ingredience nebo postup jsou kratší než 20 znaků")
            return
        self.name_input.setText("")
        self.ing_input.setText("")
        self.rec_input.setText("")
        recept = {"name": nazev, "ingredients": ing, "recipe": rec}
        self.recipes.append(recept)
        with open(self.rec_path, "w") as f:
            json.dump(self.recipes, f)
        self.refresh_recipe_list(self.recipes)

    def refresh_user_list(self, recipes):
        self.list_widget.clear()
        for r in recipes:
            name = r["username"]
            item = QListWidgetItem(name)
            self.list_widget.addItem(item)

    def show_detail(self, item):
        name = item.text()
        role = None
        display = None
        tags = None

        for entry in self.users:
            if entry["username"] == name:
                role = entry["role"]
                display = entry["display"]
                tags = entry["tags"]
                textc = entry["textc"]
                bgc = entry["backgroundc"]
                borderc = entry["borderc"]
                break

        if role is not None and display is not None:
            self.detail_window = UserDetail(name, role, tags, display, textc, bgc, borderc)
            self.detail_window.show()
        else:
            QMessageBox.warning(self, "Chyba", f"Učet s názvem {name} nebyl nalezen.")

app = QApplication([])
okno = Admin()
okno.show()
app.exec()