import os
import tkinter as tk
from tkinter import ttk

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_created(self, event):
        # Call the callback function when a file or directory is created
        self.callback()

class FileExplorer(tk.Frame):
    def __init__(self, master=None, parent_frame=None, **kwargs):
        super().__init__(master, **kwargs)
        self.parent_frame = parent_frame

        # Create custom style
        custom_style = ttk.Style()

        # Configure Treeview style
        custom_style.configure(
            'Custom.Treeview',
            foreground='black',
        )

        # Configure Frame style for the timeline
        custom_style.configure(
            'Custom.TFrame',
            highlightbackground="blue", highlightcolor="blue", highlightthickness=5,
            foreground='blue',
        )

        # Create Treeview widget
        self.tree = ttk.Treeview(self, style='Custom.Treeview')
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Define icons for folders and files
        self.folder_icon = tk.PhotoImage(
            file="/home/abhishekaslk/Temporal-DEV/assets/images/folder_icon.png").subsample(10, 10)
        self.file_icon = tk.PhotoImage(
            file="/home/abhishekaslk/Temporal-DEV/assets/images/file_icon.png").subsample(10, 10)

        # Bind double click event to handle folder opening
        self.tree.bind('<Button-1>', self.on_click)

        # Create the timeline frame
        self.timeline_frame = ttk.Frame(
            self, style='Custom.TFrame',  relief=tk.SOLID,)

        self.options_visible = False
        self.selected_option = tk.StringVar()
        self.selected_option.set(" ▶ " + " Timeline")

        self.selected_option_label = ttk.Label(
            self.timeline_frame, textvariable=self.selected_option,
            foreground="black", anchor="w", cursor="hand2")
        self.selected_option_label.pack(
            side=tk.TOP, fill=tk.X, pady=5)
        self.selected_option_label.bind(
            "<Button-1>", lambda event: self.toggle_options())

        self.dropdown_options_frame = ttk.Frame(
            self.timeline_frame, style='Custom.TFrame')

        self.dropdown_options_canvas = tk.Canvas(
            self.dropdown_options_frame)
        self.dropdown_options_frame.bind(
            "<Configure>", lambda e: self.configure_dropdown_canvas())

        self.dropdown_options_scrollbar = ttk.Scrollbar(
            self.dropdown_options_frame, orient="vertical", command=self.dropdown_options_canvas.yview)
        self.dropdown_options_scrollable_frame = ttk.Frame(
            self.dropdown_options_canvas)

        self.dropdown_options_canvas.create_window(
            (0, 0), window=self.dropdown_options_scrollable_frame, anchor="nw")
        self.dropdown_options_canvas.configure(
            yscrollcommand=self.dropdown_options_scrollbar.set)
        texts = ["Tkinter", "Flutter","PyQt-5"]
        for text in texts:
            # Create a frame for each option to hold the border
            option_frame = ttk.Frame(
                self.dropdown_options_scrollable_frame, borderwidth=1, relief="solid")
            option_frame.pack(side=tk.TOP, fill=tk.X)

            # Create a label inside the frame with the text
            option_label = ttk.Label(
                option_frame, text=text, anchor="w", cursor="hand2", wraplength=460,
                foreground=""
            )
            option_label.pack(side=tk.TOP, fill=tk.X,
                              padx=10, pady=(2, 2))
            option_label.bind(
                "<Button-1>", lambda event, text=text: self.select_option(text))

        self.dropdown_options_canvas.pack(
            side="left", fill="both", expand=True)

        self.dropdown_options_scrollbar.pack(side="right", fill="y")
        self.dropdown_options_frame.pack_forget()

        self.timeline_frame.pack(side=tk.BOTTOM, fill=tk.X)
        # Schedule periodic refresh of the file explorer
        # Adjust the interval as needed
        self. refresh_file_explorer()
        self.event_handler = FileChangeHandler(self.refresh_file_explorer)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path='.', recursive=True)
        self.observer.start()

    def refresh_file_explorer(self):
        # Update the file explorer contents
        self.populate_tree()
        # Schedule the next refresh
        # Adjust the interval as needed

        # self.after(3000, self.refresh_file_explorer)

    def configure_dropdown_canvas(self):
        self.dropdown_options_canvas.config(
            scrollregion=self.dropdown_options_canvas.bbox("all"))
        self.dropdown_options_canvas.config(
            width=self.dropdown_options_frame.winfo_width())

    def toggle_options(self):
        if self.options_visible:
            self.dropdown_options_frame.pack_forget()
            self.selected_option.set(" ▶ Timeline")
        else:
            self.dropdown_options_frame.pack(
                side=tk.TOP, fill=tk.X, expand=True)
            self.selected_option.set(" ▼ Timeline")
        self.options_visible = not self.options_visible

    def select_option(self, option):
        self.selected_option.set(option)
        self.toggle_options()

    def populate_tree(self, path=os.getcwd()):
        # Clear existing items in the tree
        self.tree.delete(*self.tree.get_children())

        # Populate the tree recursively
        self._populate_tree(path)

    def _populate_tree(self, path, parent=""):
        style = ttk.Style()

        # Set the font size explicitly when configuring Treeview
        style.configure("Treeview", font=("Arial", 18))

        # Set row height directly from font size
        style.configure("Treeview", rowheight=int(40))
        # Get the full path to the sessions folder
        sessions_path = os.path.join(path, "sessions")

        # Check if the sessions folder exists
        if not os.path.exists(sessions_path):
            return

        # Get a list of directories directly inside the sessions folder
        session_folders = [folder for folder in os.listdir(sessions_path) if os.path.isdir(
            os.path.join(sessions_path, folder)) and folder.startswith('session')]

        # Iterate through session folders and insert contents into tree
        for session_folder in session_folders:
            session_folder_path = os.path.join(sessions_path, session_folder)
            session_folder_id = self.tree.insert(parent, "end", text=session_folder, tags=(
                "folder",), image=self.folder_icon)

            # Get contents of the session folder
            session_contents = os.listdir(session_folder_path)

            # Iterate through contents and insert into tree
            for content in session_contents:
                content_path = os.path.join(session_folder_path, content)
                content_type = "folder" if os.path.isdir(
                    content_path) else "file"

                # Insert content with appropriate icon
                if content_type == "folder":
                    content_id = self.tree.insert(session_folder_id, "end", text=content, tags=(
                        "folder",), image=self.folder_icon)
                else:
                    content_id = self.tree.insert(session_folder_id, "end", text=content, tags=(
                        "file",), image=self.file_icon)
    def on_click(self, event):
        # Get the selected item in the tree
        item_id = self.tree.identify_row(event.y)
        if item_id:
            # Get the full path of the selected item
            item_path = self.get_full_item_path(item_id)
            if item_path:
                # Update the path variable in the parent frame only if it's a file
                if os.path.isfile(item_path) and self.parent_frame:
                    self.parent_frame.path = item_path
                    # Call the openfile method of the parent frame
                    self.parent_frame.openfile()

    def get_full_item_path(self, item_id):
        # Initialize an empty list to store path components
        path_components = []

        # Traverse up the tree to get the full path
        while item_id:
            item_text = self.tree.item(item_id, "text")
            # Insert at the beginning to maintain order
            path_components.insert(0, item_text)
            item_id = self.tree.parent(item_id)

        # Join path components and normalize the path
        full_path = os.path.normpath(os.path.join(*path_components))

        # Remove spaces from the full path
        full_path = full_path.replace(" ", "")

        # Get the current working directory and join with the full path
        full_path = os.path.join(os.getcwd(), full_path)

        # Return the full path
        return full_path


# Sample usage
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")

    file_explorer = FileExplorer(root)
    file_explorer.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
