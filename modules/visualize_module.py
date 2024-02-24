import customtkinter
import webbrowser
from urllib.parse import quote
from modules.idle_module import IDLEFrame

class VisualizeFrame(customtkinter.CTkFrame):
    def __init__(self, master,current_code_to_visualize, **kwargs):
        self.current_code = current_code_to_visualize
        super().__init__(master, **kwargs)
        # Encode the code parameter
        # Design the Frame
        # For demonstration purposes, let's add a label with "Visualize"
        self.visualize_button = customtkinter.CTkButton(self, text="Visualize the code",font=('arial', 20),height=60,width=100,command=self.open_website)
        self.visualize_button.pack(padx=40, pady=20,expand=True)

    def open_website(self):
        url = f"http://pythontutor.com/iframe-embed.html#code={quote(self.current_code)}&origin=opt-frontend.js&cumulative=false&heapPrimitives=false&textReferences=false&py=3&rawInputLstJSON=%5B%5D&curInstr=0"
        webbrowser.open(url)

if __name__ == "__main__":
    # Here, we demonstrate how you can test the Visualize by itself
    root = customtkinter.CTk()
    frame = VisualizeFrame(root)
    frame.pack(expand=True, fill="both")
    root.mainloop()