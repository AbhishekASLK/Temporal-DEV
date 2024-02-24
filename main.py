import customtkinter
import os
from PIL import Image
import tkinter as tk
from modules.audioaura_module import AudioAuraFrame
from modules.chatgpt_module import ChatGPTFrame
from modules.fileexplorer import FileExplorer
from modules.idle_module import IDLEFrame
from modules.techupdates_module import TechUpdatesFrame
from modules.visualize_module import VisualizeFrame

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Temporal DEV")
        self.geometry(
            "{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.current_code = ""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "assets/images")
        self.logo_image = customtkinter.CTkImage(Image.open(
            os.path.join(image_path, "logo.png")), size=(30, 30))
        self.idle_icon_image = customtkinter.CTkImage(dark_image=Image.open(
            os.path.join(image_path, "idle_icon.png")), size=(30, 30))
        self.chatgpt_icon_image = customtkinter.CTkImage(dark_image=Image.open(
            os.path.join(image_path, "chatgpt_icon.png")), size=(30, 30))
        self.news_icon_image = customtkinter.CTkImage(dark_image=Image.open(
            os.path.join(image_path, "news_icon.png")), size=(30, 30))
        self.audioaura_icon_image = customtkinter.CTkImage(dark_image=Image.open(
            os.path.join(image_path, "music_icon.png")), size=(30, 30))
        self.visualize_icon_image = customtkinter.CTkImage(dark_image=Image.open(
            os.path.join(image_path, "visualize_icon.png")), size=(30, 30))

        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Temporal DEV", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.idle_button = customtkinter.CTkButton(self.navigation_frame, font=("Public Sans", 16, "bold"), corner_radius=0, height=40, border_spacing=10, text="IDLE",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "green"),
                                                   image=self.idle_icon_image, anchor="w", command=self.idle_button_event)
        self.idle_button.grid(row=1, column=0, sticky="ew")

        self.chatgpt_button = customtkinter.CTkButton(self.navigation_frame, font=("Public Sans", 16, "bold"), corner_radius=0, height=40, border_spacing=10, text="ChatGPT",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "green"),
                                                      image=self.chatgpt_icon_image, anchor="w", command=self.chatgpt_button_event)
        self.chatgpt_button.grid(row=2, column=0, sticky="ew")

        self.techupdates_button = customtkinter.CTkButton(self.navigation_frame, font=("Public Sans", 16, "bold"), corner_radius=0, height=40, border_spacing=10, text="Tech Updates",
                                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "green"),
                                                          image=self.news_icon_image, anchor="w", command=self.techupdates_button_event)
        self.techupdates_button.grid(row=3, column=0, sticky="ew")

        self.audioaura_button = customtkinter.CTkButton(self.navigation_frame, font=("Public Sans", 16, "bold"), corner_radius=0, height=40, border_spacing=10, text="Audio Aura",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "green"),
                                                        image=self.audioaura_icon_image, anchor="w", command=self.audioaura_button_event)
        self.audioaura_button.grid(row=4, column=0, sticky="ew")

        self.visualize_button = customtkinter.CTkButton(self.navigation_frame, font=("Public Sans", 16, "bold"), corner_radius=0, height=40, border_spacing=10, text="Visualize",
                                                        fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "green"),
                                                        image=self.visualize_icon_image, anchor="w", command=self.visualize_button_event)
        self.visualize_button.grid(row=5, column=0, sticky="ew")

        self.idle_frame = IDLEFrame(self)
        self.chatgpt_frame = ChatGPTFrame(self)
        self.techupdates_frame = TechUpdatesFrame(self)
        self.audioaura_frame = AudioAuraFrame(
            self, corner_radius=0, fg_color="transparent")

        self.select_frame_by_name("IDLE")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.idle_button.configure(
            fg_color=("gray75", "gray25") if name == "IDLE" else "transparent")
        self.chatgpt_button.configure(
            fg_color=("gray75", "gray25") if name == "ChatGPT" else "transparent")
        self.techupdates_button.configure(
            fg_color=("gray75", "gray25") if name == "Tech Updates" else "transparent")
        self.audioaura_button.configure(
            fg_color=("gray75", "gray25") if name == "Audio Aura" else "transparent")
        self.visualize_button.configure(
            fg_color=("gray75", "gray25") if name == "Visualize" else "transparent")

        if name == "IDLE":
            # File Explorer Frame
            self.file_explorer_frame = tk.Frame(
                self, bg='white', width=200)  # Set width to 100
            self.file_explorer_frame.grid(
                row=0, column=1, sticky="nsew", padx=10, pady=(0, 0))

            # Set the width of the column containing the File Explorer to 100
            self.grid_columnconfigure(1, minsize=200)
            # Additional icons for file/folder creation in the file_explorer_frame
            # Load icons
            # Load icons
            create_file_icon = tk.PhotoImage(
                file="./assets/images/file_icon.png").subsample(7, 7)
            create_folder_icon = tk.PhotoImage(
                file="./assets/images/folder_icon.png").subsample(7, 7)
            create_push_icon = tk.PhotoImage(
                file="./assets/images/up_arrow.png").subsample(7, 7)

            # Create a frame for icons
            icon_frame = tk.Frame(self.file_explorer_frame,
                                  width=200, height=60, bg='white')
            icon_frame.pack(side=tk.TOP, pady=15, fill=tk.X)

            # Create File button with icon
            create_push_button = tk.Button(
                icon_frame, image=create_push_icon, command=self.push_and_populate,
                borderwidth=0, highlightthickness=0, cursor="hand2")
            create_push_button.image = create_push_icon  # Keep a reference to the image
            create_push_button.pack(side=tk.LEFT, padx=10)
            create_file_button = tk.Button(
                icon_frame, image=create_file_icon, command=self.idle_frame.new,
                borderwidth=0, highlightthickness=0, cursor="hand2")
            create_file_button.image = create_file_icon  # Keep a reference to the image
            create_file_button.pack(side=tk.RIGHT, padx=10)

            # Create Folder button with icon
            create_folder_button = tk.Button(
                icon_frame, image=create_folder_icon, command=lambda: print(
                    "Create Folder button clicked"),
                borderwidth=0, highlightthickness=0, cursor="hand2")
            create_folder_button.image = create_folder_icon  # Keep a reference to the image
            create_folder_button.pack(side=tk.RIGHT, padx=10)

            # Create File Explorer widget
            self.file_explorer = FileExplorer(
                parent_frame=self.idle_frame, master=self.file_explorer_frame)
            self.file_explorer.pack(fill=tk.BOTH, expand=True)

            # create idle frame
            self.idle_frame.grid_columnconfigure(0, weight=1)
            self.idle_frame.config(background='green')
            self.idle_frame.grid(row=0, column=2, sticky='nsew')

        else:
            if hasattr(self, 'idle_frame'):
                self.idle_frame.grid_forget()
                # Forget the File Explorer widget
            if hasattr(self, 'file_explorer_frame'):
                self.file_explorer_frame.grid_forget()

        if name == "ChatGPT":
            # create chatgpt frame
            self.chatgpt_frame.grid(row=0, column=1, sticky="nsew")
        else:
            if hasattr(self, 'chatgpt_frame'):
                self.chatgpt_frame.grid_forget()

        if name == "Tech Updates":
            self.techupdates_frame.grid(row=0, column=1, sticky="nsew")
        else:
            if hasattr(self, 'techupdates_frame'):
                self.techupdates_frame.grid_forget()

        if name == "Audio Aura":

            self.audioaura_frame.grid(row=0, column=1, sticky="nsew")
        else:
            if hasattr(self, 'audioaura_frame'):
                self.audioaura_frame.grid_forget()

        if name == "Visualize":
            self.visualize_frame = VisualizeFrame(
                self, self.current_code, corner_radius=0, fg_color="transparent")
            self.visualize_frame.grid(row=0, column=1, sticky="nsew")
        else:
            if hasattr(self, 'visualize_frame'):
                self.visualize_frame.grid_forget()

    def idle_button_event(self):
        self.select_frame_by_name("IDLE")

    def chatgpt_button_event(self):
        self.select_frame_by_name("ChatGPT")

    def techupdates_button_event(self):
        self.select_frame_by_name("Tech Updates")

    def audioaura_button_event(self):
        self.select_frame_by_name("Audio Aura")

    def visualize_button_event(self):
        self.select_frame_by_name("Visualize")

    def toggle_fullscreen(self, event=None):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def end_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)

    def push_and_populate(self):
        # Call the push_to_github method
        self.idle_frame.push_to_github()

        # Call the populate method of file_explorer
        self.file_explorer.refresh_file_explorer()


if __name__ == "__main__":
    app = App()
    app.mainloop()
