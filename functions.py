"""
This script is responsible for writing, updating and keeping the notes in 'Notes.txt' file.
"""


class Scripts:
    def __init__(self, txt_file_path: str):
        self.filepath = txt_file_path

    def get_notes(self):
        with open(self.filepath, 'r') as custom_file:
            todos_custom = custom_file.readlines()
            return todos_custom

    def write_notes(self, todos_arg):
        with open(self.filepath, 'w') as file:
            file.writelines(todos_arg)
