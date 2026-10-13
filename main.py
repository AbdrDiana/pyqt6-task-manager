
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QRadioButton,
    QCheckBox,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QButtonGroup,
    QListWidget,
    QMessageBox,
)


class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tasks = []

        self.setWindowTitle("Task Manager")
        self.resize(600, 700)

        #Центральный виджет и главный layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Заголовок приложения
        title_label = QLabel("Task Manager")
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )
        main_layout.addWidget(title_label)

        # Название задачи
        task_label = QLabel("Task")
        main_layout.addWidget(task_label)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText(
            "Enter task name"
        )
        main_layout.addWidget(self.task_input)

        # Описание задачи
        description_label = QLabel("Description")
        main_layout.addWidget(description_label)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Enter task description"
        )
        self.description_input.setMaximumHeight(110)
        main_layout.addWidget(self.description_input)

        # Выбор приоритета
        priority_label = QLabel("Priority")
        main_layout.addWidget(priority_label)

        priority_layout = QHBoxLayout()

        self.low_radio = QRadioButton("Low")
        self.medium_radio = QRadioButton("Medium")
        self.high_radio = QRadioButton("High")

        self.priority_group = QButtonGroup(self)
        self.priority_group.addButton(self.low_radio)
        self.priority_group.addButton(self.medium_radio)
        self.priority_group.addButton(self.high_radio)

        self.medium_radio.setChecked(True)

        priority_layout.addWidget(self.low_radio)
        priority_layout.addWidget(self.medium_radio)
        priority_layout.addWidget(self.high_radio)

        main_layout.addLayout(priority_layout)

        # Дополнительные настройки
        settings_layout = QHBoxLayout()

        self.important_checkbox = QCheckBox("Important")
        self.notification_checkbox = QCheckBox(
            "Send notification"
        )

        settings_layout.addWidget(self.important_checkbox)
        settings_layout.addWidget(self.notification_checkbox)

        main_layout.addLayout(settings_layout)

        # Кнопки создания и очистки
        buttons_layout = QHBoxLayout()

        self.create_button = QPushButton("Create task")
        self.clear_button = QPushButton("Clear")

        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.clear_button)

        main_layout.addLayout(buttons_layout)

        # Счётчик созданных задач
        self.counter_label = QLabel("Created tasks: 0")
        main_layout.addWidget(self.counter_label)

        # Фильтр задач
        filter_layout = QHBoxLayout()

        filter_label = QLabel("Filter:")
        self.filter_combo = QComboBox()

        self.filter_combo.addItems([
            "All",
            "Low",
            "Medium",
            "High"
        ])

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)

        main_layout.addLayout(filter_layout)

        # Список созданных задач
        tasks_label = QLabel("Tasks")
        main_layout.addWidget(tasks_label)

        self.tasks_list = QListWidget()
        main_layout.addWidget(self.tasks_list)

        # Кнопка удаления
        self.delete_button = QPushButton(
            "Delete last task"
        )
        main_layout.addWidget(self.delete_button)

        # Строка состояния
        self.status_label = QLabel("Status: Ready")
        main_layout.addWidget(self.status_label)

        # 13. Подключение сигналов
        self.create_button.clicked.connect(
            self.create_task
        )

        self.clear_button.clicked.connect(
            self.clear_form
        )

        self.delete_button.clicked.connect(
            self.delete_last_task
        )

        self.filter_combo.currentTextChanged.connect(
            self.update_task_list
        )

    def create_task(self):
        # Получаем название и описание
        task_name = self.task_input.text().strip()
        description = (
            self.description_input.toPlainText().strip()
        )

        # Проверяем название
        if not task_name:
            QMessageBox.warning(
                self,
                "Error",
                "Please enter a task name."
            )
            return

        # Определяем приоритет
        if self.low_radio.isChecked():
            priority = "Low"
        elif self.high_radio.isChecked():
            priority = "High"
        else:
            priority = "Medium"

        # Получаем дополнительные настройки
        important = self.important_checkbox.isChecked()
        notification = (
            self.notification_checkbox.isChecked()
        )

        # Создаём словарь с информацией
        task = {
            "name": task_name,
            "description": description,
            "priority": priority,
            "important": important,
            "notification": notification
        }

        # Сохраняем задачу в список Python
        self.tasks.append(task)

        # Выводим задачу в консоль
        print("Task created:")
        print(task)
        print()

        # Обновляем интерфейс
        self.update_task_list()
        self.update_counter()

        self.status_label.setText(
            "Status: Task created"
        )

        # Очищаем форму
        self.clear_form()

    def clear_form(self):
        self.task_input.clear()
        self.description_input.clear()

        self.medium_radio.setChecked(True)

        self.important_checkbox.setChecked(False)
        self.notification_checkbox.setChecked(False)

    def update_task_list(self, _selected_filter=None):
        # Удаляем старые элементы из отображения
        self.tasks_list.clear()

        selected_filter = self.filter_combo.currentText()

        # Показываем задачи с учётом фильтра
        for task in self.tasks:
            if (
                selected_filter != "All"
                and task["priority"] != selected_filter
            ):
                continue

            task_text = (
                f"{task['name']}\n"
                f"Description: {task['description']}\n"
                f"Priority: {task['priority']}\n"
                f"Important: {task['important']}\n"
                f"Send notification: {task['notification']}"
            )

            self.tasks_list.addItem(task_text)

    def update_counter(self):
        self.counter_label.setText(
            f"Created tasks: {len(self.tasks)}"
        )

    def delete_last_task(self):
        if not self.tasks:
            QMessageBox.information(
                self,
                "Information",
                "There are no tasks to delete."
            )
            return

        # Удаляем последнюю созданную задачу
        self.tasks.pop()

        self.update_task_list()
        self.update_counter()

        self.status_label.setText(
            "Status: Last task deleted"
        )


def main():
    app = QApplication(sys.argv)

    window = TaskManagerWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
