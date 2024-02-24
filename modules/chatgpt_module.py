# import customtkinter

# class ChatGPTFrame(customtkinter.CTkFrame):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)

#         # Design the Frame
#         # For demonstration purposes, let's add a label with "ChatGPT"
#         self.label_hello_world = customtkinter.CTkLabel(self, text="ChatGPT")
#         self.label_hello_world.pack(padx=20, pady=20)


# if __name__ == "__main__":
#     # Here, we demonstrate how you can test the ChatGPT by itself
#     root = customtkinter.CTk()
#     frame = ChatGPTFrame(root)
#     frame.pack(expand=True, fill="both")
#     root.mainloop()

import customtkinter
import tkinter as tk
from tkinter import ttk
from openai import OpenAI


class ChatGPTFrame(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.openai_client = OpenAI()  # Initialize OpenAI client

        self.setup_ui()

    def setup_ui(self):
        self.chat_history_frame = ttk.Frame(self)
        self.chat_history_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_history_canvas = tk.Canvas(
            self.chat_history_frame, bg='#3D3D3D')
        self.chat_history_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chat_history_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        scrollbar = ttk.Scrollbar(
            self.chat_history_frame, orient=tk.VERTICAL, command=self.chat_history_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_history_canvas.configure(yscrollcommand=scrollbar.set)

        self.chat_frame = tk.Frame(self.chat_history_canvas, bg='#3D3D3D')
        self.chat_history_canvas.create_window(
            (0, 0), window=self.chat_frame, anchor=tk.NW)

        input_frame = tk.Frame(self, bg="#3D3D3D")
        input_frame.pack(fill=tk.X)

        # Add some padding and margin to the input field
        self.input_field = tk.Entry(input_frame, font=(
            'arial', 18), foreground='white', background='#3D3D3D')
        self.input_field.pack(side=tk.LEFT, fill=tk.X,
                              expand=True, padx=20, pady=100, ipady=20)
        self.input_field.bind("<Return>", self.send_message)

        send_button = customtkinter.CTkButton(
            input_frame, text="Send", height=50, width=110, font=('arial', 15), fg_color='green', command=self.send_message)
        send_button.pack(padx=20, side=tk.RIGHT)

        # Define styles for chat bubbles
        self.style = ttk.Style()
        self.style.configure(
            "Chat.TFrame", background="#5DBCD2", font=('arial', 15), padding=10, wrapping=True)
        self.style.configure(
            "Chat.You.TLabel", background="gray", font=('arial', 15), padding=10, foreground="white", wrapping=True)
        self.style.configure(
            "Chat.AI.TLabel", background="#E5E5E5", font=('arial', 15), padding=10, wrapping=True)
        self.style.configure("CodeLabel.TLabel", font=(
            'arial', 15), pady=300, background="gray", foreground='white')
        self.style.configure("Chat.TFrame", font=(
            'arial', 15), padding=10, background="#5DBCD2")

    def send_message(self, event=None):
        # Retrieve the text from the input field after the user has entered it
        message = self.input_field.get()

        # Append the user message to the chat history with appropriate formatting
        self.append_to_chat_history(message, sender="You")

        # Generate AI response using OpenAI API
        completion = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ],
            temperature=0.7,
        )

        # Extract the AI response from the completion
        if completion.choices:
            first_choice = completion.choices[0]
            if hasattr(first_choice, "message"):
                # Access content from dictionary
                ai_response = first_choice.message.content

                # Append the AI response to the chat history with appropriate formatting
                self.append_to_chat_history(ai_response, sender="AI")

        # Clear the input field after sending the message
        self.input_field.delete(0, tk.END)

        # Scroll to the bottom to show the latest message
        self.chat_history_canvas.yview_moveto(1.0)

    def append_to_chat_history(self, text, sender="AI"):
        chat_frame = ttk.Frame(self.chat_frame,)
        chat_frame.pack(fill=tk.X, padx=5, pady=3, anchor=(
            "e" if sender == "You" else "w"))

        if "```" in text:
            # Response contains code block
            code_start = text.find("```")
            code_end = text.rfind("```")

            pre_text = text[:code_start]
            code_text = text[code_start+3:code_end]
            post_text = text[code_end+3:]

            inner_frame = ttk.Frame(chat_frame, style="Chat.TFrame")
            inner_frame.pack(fill=tk.X, expand=True)

            if pre_text.strip():
                pre_label = ttk.Label(
                    inner_frame, text=pre_text, style="Chat." + sender + ".TLabel", wraplength=900)
                pre_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)

            code_label = ttk.Label(
                inner_frame, text=code_text, style="CodeLabel.TLabel", wraplength=900)
            code_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)

            if post_text.strip():
                post_label = ttk.Label(
                    inner_frame, text=post_text, style="Chat." + sender + ".TLabel", wraplength=900)
                post_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)
        else:
            chat_label = ttk.Label(chat_frame, text=text,
                                   style="Chat." + sender + ".TLabel", wraplength=900)
            chat_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=3)

        # Update the chat history canvas to reflect changes in the chat frame size
        self.chat_frame.update_idletasks()
        self.chat_history_canvas.configure(
            scrollregion=self.chat_history_canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.chat_history_canvas.yview_scroll(-1*(event.delta//120), "units")


if __name__ == "__main__":
    app = ChatGPTFrame()
    app.mainloop()
