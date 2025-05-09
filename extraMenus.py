import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Nautilus", "4.0")
from gi.repository import Nautilus, GObject, Gtk
from typing import List
import os
import subprocess

class FehMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files: List[Nautilus.FileInfo]) -> List[Nautilus.MenuItem]:

        feh_menu_item = Nautilus.MenuItem(
            name="feh",
            label="Open With Feh",
            tip="",
            icon="Keyboard", # TODO icon
        )

        feh_menu_item.connect("activate", self.open_with_feh, files)

        return [
            feh_menu_item,
        ]
    
    def open_with_feh(self, user_data, files: List[Nautilus.FileInfo]) -> None:
        
        file_paths = [file.get_location().get_path() for file in files]
        process = subprocess.Popen(["feh", "--recursive", "-dF"] + file_paths, stderr=subprocess.PIPE)
        # TODO do all the stuff below in the same process, see multiprocessing in python
        # process.wait() 
        # print(process.returncode)
        # if process.returncode is not None and  process.returncode != 0:
        #     dialog = Gtk.MessageDialog(
        #         message_type=Gtk.MessageType.ERROR,
        #         buttons=Gtk.ButtonsType.OK,
        #         text="something went wrong")
        #     dialog.connect("response", self.on_button_clicked)
        #     dialog.show()

    def on_button_clicked(self, dialog: Gtk.Dialog, response_id: int):
        dialog.close()


class VlcMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files: List[Nautilus.FileInfo]) -> List[Nautilus.MenuItem]:

        feh_menu_item = Nautilus.MenuItem(
            name="vlc",
            label="Open With VLC",
            tip="",
            icon="", # TODO icon
        )

        feh_menu_item.connect("activate", self.open_with_vlc, files)

        return [
            feh_menu_item,
        ]
    
    def open_with_vlc(self, menu: Nautilus.MenuItem, files: List[Nautilus.FileInfo]) -> None:
    
        file_paths = [file.get_location().get_path() for file in files]
        subprocess.Popen(["vlc"] + file_paths)


class zipMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files: list[Nautilus.FileInfo]) -> list[Nautilus.MenuItem]:

        zip_menu = Nautilus.MenuItem(
            name="7zip",
            label="7zip",
            tip="",
            icon="", # TODO icon
        )

        submenu = Nautilus.Menu()
        zip_menu.set_submenu(submenu)

        extract_here_item = Nautilus.MenuItem(
            name="zipmenuprovider::extract here",
            label="Extract here",
            tip="",
            icon="",
        )
        extract_here_item.connect("activate", self.extract_here, files)
        submenu.append_item(extract_here_item)

        extract_to_item = Nautilus.MenuItem(
            name="zipmenuprovider::extract to */",
            label="Extract to */",
            tip="",
            icon="",
        )
        extract_to_item.connect("activate", self.extract_to, files)
        submenu.append_item(extract_to_item)

        return [
            zip_menu,
        ]

    def extract_here(self, _, files) -> None:

        file_location_paths =  [f"'{file.get_location().get_path()}'" for file in files]
        files_string = " ".join(file_location_paths)
        script = f'for file in {files_string}; do 7z x "$file" -o"$(dirname "$file")"; done; exec'
        
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c" , script], cwd=os.path.dirname(file_location_paths[0].strip("'")))
        
    
    def extract_to(self, _, files) -> None:

        file_location_paths =  [f"'{file.get_location().get_path()}'" for file in files]
        files_string = " ".join(file_location_paths)
        script = f'for file in {files_string}; do 7z x "$file" -o"$(dirname "$file")"/*; done; exec'
        subprocess.Popen(["gnome-terminal", "--", "bash", "-c" , script])
        

        