import os
import psutil


class Installer:
    FOLDER_NAME = "HS Softworks"
    SUBFOLDER_NAME = "My Notes"
    FILE_NAME = "Notes.txt"

    def __init__(self):
        self.parent_dir = Installer.disk_check()
        self.folder_path = os.path.join(self.parent_dir, Installer.FOLDER_NAME, Installer.SUBFOLDER_NAME)
        self.file_path = os.path.join(self.folder_path, Installer.FILE_NAME)

    @staticmethod
    def disk_check() -> str:
        """
        :return: dir to folder of non-C disk if exists, otherwise returns C
            E:\Program Files (x86)
        """
        # Get a list of all available disk partitions
        partitions = psutil.disk_partitions()

        for partition in partitions:
            drive_letter = partition.device[:2]
            if drive_letter != 'C:':
                selected_drive = drive_letter
                break
            else:
                selected_drive = 'C'

        parent_dir = fr"{selected_drive}\Program Files (x86)"

        return parent_dir


class Installation(Installer):

    def create_folder(self) -> None:
        """
        Creates the folder path.

        This function creates a text file named 'Notes.txt'

        Example:
        E://Program Files (x86)/HS Softworks/My Notes
        """

        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            exit()
        else:
            pass

    def create_file(self) -> None:
        """
        Creates the Notes.txt file.

        This function creates a text file named 'Notes.txt'

        Example:
        E://Program Files (x86)/HS Softworks/My Notes/Notes.txt
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                f.write("")
                exit()
        else:
            pass


class InstallerMain:
    filepath = None

    @property
    def get_filepath(self) -> str:
        """ Returns the filepath of Notes.txt"""
        return InstallerMain.filepath

    @staticmethod
    def make_repository():
        # initializing the parent installer object and activating the values
        installer_obj = Installer()

        # defining the available disk for the folder
        installer_obj.disk_check()

        # initializing the subclass to  create a folder and a file
        installation_obj = Installation()

        # creating the folder
        installation_obj.create_folder()

        # creating the file
        installation_obj.create_file()

        # saving the filepath in the class
        InstallerMain.filepath = installation_obj.file_path


if __name__ == '__main__':
    InstallerMain.make_repository()
    print(InstallerMain().get_filepath)
