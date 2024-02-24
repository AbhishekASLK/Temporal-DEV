# import customtkinter

# class IDLEFrame(customtkinter.CTkFrame):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)

#         # Design the Frame
#         # For demonstration purposes, let's add a label with "IDLE"
#         self.label_hello_world = customtkinter.CTkLabel(self, text="IDLE")
#         self.label_hello_world.pack(padx=20, pady=20)


# if __name__ == "__main__":
#     # Here, we demonstrate how you can test the IDLE by itself
#     root = customtkinter.CTk()
#     frame = IDLEFrame(root)
#     frame.pack(expand=True, fill="both")
#     root.mainloop()

import shlex
import customtkinter
import os
import subprocess
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog
import git

from modules.gitHandler import GitHubHandler


class IDLEFrame(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.app = master
        self.path = ''
        self.font_size = 18
        self.check = StringVar(value='light')
        self.create_widgets()

    def create_widgets(self):
        self.myMenu = Menu(self.master)
        self.master.config(menu=self.myMenu)

        self.button_frame = Frame(self)
        self.button_frame.config(bg='white')
        self.button_frame.pack(side='top', fill='x')

        save_btn = customtkinter.CTkButton(
            self.button_frame, fg_color='green', text='Save',command=self.save)
        save_btn.pack(side='left', padx=20, ipadx=10,pady=7, ipady=5)
        save_as_btn = customtkinter.CTkButton(
            self.button_frame, fg_color='green', text='Save as', command=self.saveas)
        save_as_btn.pack(side='left', padx=20, ipadx=10,pady=7, ipady=5)
        exit_btn = customtkinter.CTkButton(
            self.button_frame, fg_color='green', text='Exit', command=self.iexit)
        exit_btn.pack(side='left', padx=20, ipadx=10,pady=7, ipady=5)
        run_btn = customtkinter.CTkButton(
            self.button_frame, fg_color='green', text='Run', command=self.run_code)
        run_btn.pack(side='left', padx=20, ipadx=10,pady=7, ipady=5)
        clear_btn = customtkinter.CTkButton(
            self.button_frame, fg_color='green', text='Clear', command=self.clear)
        clear_btn.pack(side='left', padx=20, ipadx=10,pady=7, ipady=5)
        light_theme_btn = customtkinter.CTkButton(
            self.button_frame, fg_color='green', text='Light Theme', command=self.light_theme)
        light_theme_btn.pack(side='left', padx=20, ipadx=10,pady=7, ipady=5)
        dark_theme_btn = customtkinter.CTkButton(
            self.button_frame, fg_color='green', text='Dark Theme', command=self.dark_theme)
        dark_theme_btn.pack(side='left', padx=20, ipadx=10,pady=7, ipady=5)

        # Remote Repo
        # remote_btn = Button(button_frame, text='Set Remote', command=self.set_remote_repo)
        # remote_btn.pack(side='left', padx=5)

        editFrame = Frame(self, bg='white')
        editFrame.pack(side=TOP, fill=BOTH, expand=True)

        scrollbar = Scrollbar(editFrame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.textarea = Text(editFrame, font=(
            'arial', self.font_size, 'bold'), yscrollcommand=scrollbar.set)
        self.textarea.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.textarea.yview)

        self.outputFrame = LabelFrame(
            self, text='Output', font=('arial', 12, 'bold'))
        self.outputFrame.pack(side=BOTTOM, fill=BOTH, expand=True)

        scrollbar1 = Scrollbar(self.outputFrame, orient=VERTICAL)
        scrollbar1.pack(side=RIGHT, fill=Y)
        self.outputarea = Text(self.outputFrame, font=(
            'arial', self.font_size, 'bold'), yscrollcommand=scrollbar1.set)
        self.outputarea.pack(fill=BOTH, expand=True)
        scrollbar1.config(command=self.textarea.yview)

    # ******************* Github Functionality **********************

    def push_to_github(self):
        github_handler = GitHubHandler()
        github_handler.push_to_github()

    def new(self):
        # Open file dialog to get the location to save the new file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                                                 ("Text files", "*.txt"), ("All files", "*.*")])

        if file_path:
            try:
                with open(file_path, 'w') as new_file:
                    new_file.write(
                        "This is a new file created using tkinter!")

                self.path = file_path

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error creating file: {str(e)}")

    def openfile(self, event=None):
        if self.path == "":
            self.path = filedialog.askopenfilename(
                filetypes=[('Python Files', '*.py')], defaultextension=('.py'))
        if self.path != '':
            if os.path.isfile(self.path):
                with open(self.path, 'r') as file:
                    self.app.current_code = file.read()
                self.textarea.delete(1.0, END)
                self.textarea.insert(1.0, self.app.current_code)

    def save(self, event=None):
        # Use 'end-1c' to exclude the trailing newline
        self.app.current_code = self.textarea.get(1.0, 'end-1c')
        if self.path == '':
            self.saveas()
        else:
            # Extract the directory name from the path
            directory_name = os.path.basename(os.path.dirname(self.path))
            if directory_name.lower().startswith('session'):
                isfile = os.path.basename(self.path).endswith('.py')
                if isfile:
                    with open(self.path, 'w') as file:
                        file.write(self.app.current_code)
                else:
                    messagebox.showerror(
                        'ERROR', message="File must be .py extension")
                    with open(self.path, 'w') as file:
                        file.write(self.app.current_code)
            else:
                messagebox.showerror(
                    "Error", "File can only be saved in a directory starting with 'session'")

    def saveas(self, event=None):
        self.path = filedialog.asksaveasfilename(
            filetypes=[('Python Files', '*.py')], defaultextension=('.py'))
        if self.path != '':
            self.save()

    def iexit(self, event=None):
        result = messagebox.askyesno('Confirm', 'Do you want to exit?')
        if result:
            self.master.destroy()

    def clear(self):
        self.textarea.delete(1.0, END)
        self.outputarea.delete(1.0, END)

    def run_code(self):
        if self.path == '':
            messagebox.showerror(
                'Error', 'Please save the file before running')
        else:
            # Extract the file name from the path
            script_directory = os.path.dirname(self.path)
            os.chdir(script_directory)
            command = ['python', self.path]

            # Now you can execute the script
            run_file = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            output, error = run_file.communicate()
            print(output, error)

            # Change back to the parent directory after the code execution
            os.chdir(os.path.abspath(os.path.join(script_directory, os.pardir)))

            self.outputarea.delete(1.0, END)
            # Assuming output is bytes
            self.outputarea.insert(1.0, output.decode())
            self.outputarea.insert(1.0, error.decode())  # Ass

    def light_theme(self):
        self.button_frame.config(bg='white')
        self.textarea.config(bg='white', fg='black')
        self.outputarea.config(bg='white', fg='black')

    def dark_theme(self):
        self.button_frame.config(bg='gray20')
        self.textarea.config(bg='gray20', fg='white')
        self.outputarea.config(bg='gray20', fg='white')

    def font_inc(self, event=None):
        self.font_size += 1
        self.textarea.config(font=('arial', self.font_size, 'bold'))

    def font_dec(self, event=None):
        self.font_size -= 1
        self.textarea.config(font=('arial', self.font_size, 'bold'))


if __name__ == '__main__':
    root = Tk()
    root.geometry('1270x670+0+0')
    root.title('IDLE - Temporal DEV')

    app = IDLEFrame(master=root)
    app.pack(fill='both', expand=True)

    root.mainloop()
