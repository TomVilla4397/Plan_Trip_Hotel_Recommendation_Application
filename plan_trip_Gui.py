import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit,QRadioButton
from plan_trip import plan_trip_and_find_hotels_gui

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.radio_no.toggled.connect(self.hide_text_childeren)
        self.radio_yes.toggled.connect(self.show_text_childeren)
    def initUI(self):
        self.setWindowTitle("User Inputs")
        self.setGeometry(300, 300, 300, 200)

        # Create labels
        label_destination = QLabel("Please enter the destination:")
        label_start_date = QLabel("Please enter the start date (YYYY-MM-DD):")
        label_end_date = QLabel("Please enter the end date (YYYY-MM-DD):")
        label_adults_num = QLabel("Please enter the number of adults:")
        label_is_children = QLabel("Are you traveling with children? (yes/no):")
        # self.button_is_children = QPushButton("No",self)
        # self.button_is_children.setGeometry(0,0,100,30)
        # self.button_is_children.clicked.connect(self.is_childeren_button_clicked)
        self.radio_yes = QRadioButton("Yes")
        self.radio_no = QRadioButton("No")
        self.radio_yes.setChecked(True) 
        self.label_children_num = QLabel("Please enter the ages of children separated by comma:")
        label_attraction = QLabel("Please enter attractions you are interested in (e.g: museums, theme parks, landmarks, nature trails, historical sites, etc):")
        label_transportation = QLabel("Please enter the mode of transportation (e.g: bus, rental car, taxi, bicycle, walking, etc):")

        # Create input fields
        self.input_destination = QLineEdit()
        self.input_start_date = QLineEdit()
        self.input_end_date = QLineEdit()
        self.input_adults_num = QLineEdit()
        self.input_is_children = QLineEdit()
        self.input_children_num = QLineEdit()
        self.input_attraction = QLineEdit()
        self.input_transportation = QLineEdit()

        # Create submit button
        btn_submit = QPushButton("Submit")
        btn_submit.clicked.connect(self.submit_clicked)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(label_destination)
        layout.addWidget(self.input_destination)
        layout.addWidget(label_start_date)
        layout.addWidget(self.input_start_date)
        layout.addWidget(label_end_date)
        layout.addWidget(self.input_end_date)
        layout.addWidget(label_adults_num)
        layout.addWidget(self.input_adults_num)
        layout.addWidget(label_is_children)
        layout.addWidget(self.radio_yes)
        layout.addWidget(self.radio_no)
        layout.addWidget(self.label_children_num)
        layout.addWidget(self.input_children_num)
        layout.addWidget(label_attraction)
        layout.addWidget(self.input_attraction)
        layout.addWidget(label_transportation)
        layout.addWidget(self.input_transportation)
        layout.addWidget(btn_submit)
        self.setLayout(layout)

    def submit_clicked(self):
        # Retrieve the user inputs from the input fields
        destination = self.input_destination.text()
        start_date = self.input_start_date.text()
        end_date = self.input_end_date.text()
        adults_num = int(self.input_adults_num.text())
        is_children = "Yes" if self.radio_yes.isChecked() else "No"
        children_num = [int(age) for age in self.input_children_num.text().split(',')] if is_children == 'yes' else []
        attraction = self.input_attraction.text()
        transportation = self.input_transportation.text()

        # Call the plan_trip_and_find_hotels function
        result = plan_trip_and_find_hotels_gui(destination, start_date, end_date, adults_num, children_num, attraction, transportation)

        # Create a result window
        result_window = ResultWindow(result)
        result_window.show()
    def hide_text_childeren(self):
        if self.radio_no.isChecked():
            self.label_children_num.hide()
            self.input_children_num.hide()
    def show_text_childeren(self):
        if self.radio_yes.isChecked():
            self.label_children_num.show()
            self.input_children_num.show()
        
class ResultWindow(QWidget):
    def __init__(self, result):
        super().__init__()
        self.result = result
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Result")
        self.setGeometry(300, 300, 500, 400)

        # Create a text edit widget to display the result
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(self.result)

        # Create a layout
        layout = QVBoxLayout()
        layout.addWidget(text_edit)

        self.setLayout(layout)

def main():
    # Create the PyQt application
    app = QApplication([])

    # Create an instance of the GUI input window
    input_window = InputWindow()

    # Show the input window
    input_window.show()

    # Run the PyQt application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
