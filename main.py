import PySimpleGUI as sg
import time
import os

from installment import InstallerMain
from functions import Scripts


class GUIApp:
    ICON_PATH = os.path.abspath(os.path.join(os.getcwd(), 'logo.ico'))
    FILEPATH = None

    def __init__(self):
        # creating a repository
        InstallerMain.make_repository()

        # invoking the filepath
        self.FILEPATH = InstallerMain().get_filepath

        # activating scripts
        self.scripts = Scripts(txt_file_path=self.FILEPATH)

        # getting current records from db
        self.todos = self.scripts.get_notes()

        # setting up the options
        sg.theme("DarkPurple4")
        sg.set_options(icon=self.ICON_PATH)

        # defining the elements
        clock = sg.Text('', key="clock")
        label = sg.Text("Type in a Note", text_color="orange")

        input_box = sg.InputText(tooltip="Enter a note", size=32, key='todo')
        add_button = sg.Button("Add")
        list_box = sg.Listbox(values=self.scripts.get_notes(), key='todos_listbox',
                              enable_events=True, size=(30, 7))
        edit_button = sg.Button("Edit", tooltip="Select a note")
        remove_button = sg.Button("Remove")
        exit_button = sg.Button("Exit", button_color=('orange', None))

        buttons_col = sg.Column([[edit_button], [remove_button]], justification='center')

        # setting up the main window
        self.window = sg.Window("My Notes",
                                layout=[[clock],
                                        [label],
                                        [input_box, add_button],
                                        [list_box, buttons_col],
                                        [exit_button]],
                                font=('Helvetica', 12, 'bold'),
                                icon=self.ICON_PATH)

    def refresh(self, input_key='todo', listbox_key='todos_listbox'):
        """ Updates the list-box """
        self.window[listbox_key].update(values=self.todos)
        self.window[input_key].update(value='')


class GuiAppMain(GUIApp):
    def run(self):
        while True:
            event, value = self.window.read(timeout=500)
            self.window["clock"].update(
                value=time.strftime("%Y-%b-%d, "
                                    "%H:%M:%S"))
            match event:

                case "Add":
                    todo_to_add = value['todo'] + "\n"
                    self.todos.append(todo_to_add)
                    self.scripts.write_notes(self.todos)
                    self.refresh()

                case "Edit":
                    if len(value['todos_listbox']) != 0:
                        try:
                            todo_to_remove = value['todos_listbox'][0]
                            index = self.todos.index(todo_to_remove)
                            todo_to_add = value['todo']  # + "\n"
                            self.todos[index] = todo_to_add
                            self.scripts.write_notes(self.todos)
                            self.refresh()

                        except IndexError:
                            sg.popup(
                                "Please select an item first", title='Oops',
                                font=('Helvetica', 12, 'bold'), icon=self.ICON_PATH, non_blocking=True)
                            continue
                    else:
                        sg.popup(
                            "Please enter a note before editing it", title='Oops',
                            font=('Helvetica', 12, 'bold'), icon=self.ICON_PATH, non_blocking=True)
                        continue

                case "Remove":
                    if len(value['todos_listbox']) != 0:
                        try:
                            todo_to_remove = value['todos_listbox'][0]
                            index = self.todos.index(todo_to_remove)
                            self.todos.pop(index)
                            self.scripts.write_notes(self.todos)
                            self.refresh()

                        except IndexError:
                            sg.popup(
                                "Please select an item first", title='Ouch',
                                font=('Helvetica', 12, 'bold'), icon=self.ICON_PATH, non_blocking=True)
                            continue
                    else:
                        sg.popup("The list is empty!", title='Ouch',
                                 font=('Helvetica', 12, 'bold'), icon=self.ICON_PATH, non_blocking=True)
                        continue

                case sg.WIN_CLOSED:
                    break
                case "Exit":
                    break

        self.window.close()


if __name__ == '__main__':
    gui = GUIApp()
    main = GuiAppMain()
    main.run()
