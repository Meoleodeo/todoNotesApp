import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTabWidget, QLabel, QLineEdit, 
                            QPushButton, QTextEdit, QListWidget, QCheckBox,
                            QMessageBox, QInputDialog)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from database import Database

class TodoNotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo & Notes Manager")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize database
        try:
            self.db = Database()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", 
                               f"Failed to connect to SQL Server: {str(e)}\n\n"
                               "Please ensure SQL Server is running and credentials are correct.")
            sys.exit(1)
        
        # Set theme colors
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgba(0, 100, 100, 0.9);
            }
            QWidget {
                background-color: rgba(0, 120, 120, 0.8);
                color: white;
            }
            QPushButton {
                background-color: rgba(0, 150, 150, 0.9);
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(0, 170, 170, 0.9);
            }
            QLineEdit, QTextEdit {
                background-color: rgba(255, 255, 255, 0.9);
                color: black;
                border-radius: 3px;
            }
        """)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Always on top checkbox
        self.always_on_top_cb = QCheckBox("Always on Top")
        self.always_on_top_cb.stateChanged.connect(self.toggle_always_on_top)
        layout.addWidget(self.always_on_top_cb)

        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Todo tab
        todo_tab = QWidget()
        todo_layout = QVBoxLayout(todo_tab)
        
        # Todo input
        todo_input_layout = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Enter todo item...")
        self.todo_link_input = QLineEdit()
        self.todo_link_input.setPlaceholderText("Enter link (optional)...")
        add_todo_btn = QPushButton("Add Todo")
        add_todo_btn.clicked.connect(self.add_todo)
        
        todo_input_layout.addWidget(self.todo_input)
        todo_input_layout.addWidget(self.todo_link_input)
        todo_input_layout.addWidget(add_todo_btn)
        todo_layout.addLayout(todo_input_layout)

        # Todo list
        self.todo_list = QListWidget()
        self.todo_list.itemDoubleClicked.connect(self.edit_todo)
        todo_layout.addWidget(self.todo_list)

        # Todo buttons
        todo_btn_layout = QHBoxLayout()
        delete_todo_btn = QPushButton("Delete")
        delete_todo_btn.clicked.connect(self.delete_todo)
        edit_todo_btn = QPushButton("Edit")
        edit_todo_btn.clicked.connect(lambda: self.edit_todo(self.todo_list.currentItem()))
        open_link_btn = QPushButton("Open Link")
        open_link_btn.clicked.connect(self.open_todo_link)
        
        todo_btn_layout.addWidget(delete_todo_btn)
        todo_btn_layout.addWidget(edit_todo_btn)
        todo_btn_layout.addWidget(open_link_btn)
        todo_layout.addLayout(todo_btn_layout)

        # Notes tab
        notes_tab = QWidget()
        notes_layout = QVBoxLayout(notes_tab)
        
        # Notes input
        notes_input_layout = QVBoxLayout()
        self.note_title_input = QLineEdit()
        self.note_title_input.setPlaceholderText("Enter note title...")
        self.note_content_input = QTextEdit()
        self.note_content_input.setPlaceholderText("Enter note content...")
        add_note_btn = QPushButton("Add Note")
        add_note_btn.clicked.connect(self.add_note)
        
        notes_input_layout.addWidget(self.note_title_input)
        notes_input_layout.addWidget(self.note_content_input)
        notes_input_layout.addWidget(add_note_btn)
        notes_layout.addLayout(notes_input_layout)

        # Notes list
        self.notes_list = QListWidget()
        self.notes_list.itemDoubleClicked.connect(self.edit_note)
        notes_layout.addWidget(self.notes_list)

        # Notes buttons
        notes_btn_layout = QHBoxLayout()
        delete_note_btn = QPushButton("Delete")
        delete_note_btn.clicked.connect(self.delete_note)
        edit_note_btn = QPushButton("Edit")
        edit_note_btn.clicked.connect(lambda: self.edit_note(self.notes_list.currentItem()))
        pin_note_btn = QPushButton("Toggle Pin")
        pin_note_btn.clicked.connect(self.toggle_pin_note)
        
        notes_btn_layout.addWidget(delete_note_btn)
        notes_btn_layout.addWidget(edit_note_btn)
        notes_btn_layout.addWidget(pin_note_btn)
        notes_layout.addLayout(notes_btn_layout)

        # Add tabs
        tabs.addTab(todo_tab, "Todo")
        tabs.addTab(notes_tab, "Notes")

        # Load existing items
        self.load_todos()
        self.load_notes()

    def toggle_always_on_top(self, state):
        if state == Qt.CheckState.Checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    # Todo functions
    def add_todo(self):
        task = self.todo_input.text().strip()
        link = self.todo_link_input.text().strip()
        
        if task:
            try:
                self.db.add_todo(task, link)
                self.todo_input.clear()
                self.todo_link_input.clear()
                self.load_todos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add todo: {str(e)}")

    def load_todos(self):
        try:
            self.todo_list.clear()
            todos = self.db.get_todos()
            for todo_id, task, link in todos:
                item_text = f"{task}"
                if link:
                    item_text += f" [🔗]"
                item = QListWidget.Item(item_text)
                item.setData(Qt.ItemDataRole.UserRole, (todo_id, link))
                self.todo_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load todos: {str(e)}")

    def edit_todo(self, item):
        if item:
            todo_id = item.data(Qt.ItemDataRole.UserRole)[0]
            current_text = item.text().split(" [🔗]")[0]
            new_text, ok = QInputDialog.getText(self, "Edit Todo", "Edit task:", text=current_text)
            
            if ok and new_text.strip():
                try:
                    self.db.update_todo(todo_id, new_text)
                    self.load_todos()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update todo: {str(e)}")

    def delete_todo(self):
        current_item = self.todo_list.currentItem()
        if current_item:
            todo_id = current_item.data(Qt.ItemDataRole.UserRole)[0]
            try:
                self.db.delete_todo(todo_id)
                self.load_todos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete todo: {str(e)}")

    def open_todo_link(self):
        current_item = self.todo_list.currentItem()
        if current_item:
            link = current_item.data(Qt.ItemDataRole.UserRole)[1]
            if link:
                QDesktopServices.openUrl(QUrl(link))

    # Notes functions
    def add_note(self):
        title = self.note_title_input.text().strip()
        content = self.note_content_input.toPlainText().strip()
        
        if title:
            try:
                self.db.add_note(title, content)
                self.note_title_input.clear()
                self.note_content_input.clear()
                self.load_notes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add note: {str(e)}")

    def load_notes(self):
        try:
            self.notes_list.clear()
            notes = self.db.get_notes()
            for note_id, title, content, pinned in notes:
                prefix = "📌 " if pinned else ""
                item = QListWidget.Item(f"{prefix}{title}")
                item.setData(Qt.ItemDataRole.UserRole, (note_id, content, pinned))
                self.notes_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load notes: {str(e)}")

    def edit_note(self, item):
        if item:
            note_id, content, pinned = item.data(Qt.ItemDataRole.UserRole)
            current_title = item.text().replace("📌 ", "")
            
            dialog = QInputDialog(self)
            dialog.setWindowTitle("Edit Note")
            dialog.setLabelText("Edit title:")
            dialog.setTextValue(current_title)
            
            if dialog.exec():
                new_title = dialog.textValue()
                if new_title.strip():
                    try:
                        self.db.update_note(note_id, new_title)
                        self.load_notes()
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to update note: {str(e)}")

    def delete_note(self):
        current_item = self.notes_list.currentItem()
        if current_item:
            note_id = current_item.data(Qt.ItemDataRole.UserRole)[0]
            try:
                self.db.delete_note(note_id)
                self.load_notes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete note: {str(e)}")

    def toggle_pin_note(self):
        current_item = self.notes_list.currentItem()
        if current_item:
            note_id, _, current_pinned = current_item.data(Qt.ItemDataRole.UserRole)
            new_pinned = not current_pinned
            try:
                self.db.toggle_note_pin(note_id, new_pinned)
                self.load_notes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to toggle pin: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TodoNotesApp()
    window.show()
    sys.exit(app.exec())