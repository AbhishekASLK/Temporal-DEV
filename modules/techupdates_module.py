# import customtkinter

# class TechUpdatesFrame(customtkinter.CTkFrame):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)

#         # Design the Frame
#         # For demonstration purposes, let's add a label with "TechUpdatesFrame"
#         self.label_hello_world = customtkinter.CTkLabel(self, text="TechUpdates")
#         self.label_hello_world.pack(padx=20, pady=20)


# if __name__ == "__main__":
#     # Here, we demonstrate how you can test the TechUpdatesFrame by itself
#     root = customtkinter.CTk()
#     frame = TechUpdatesFrame(root)
#     frame.pack(expand=True, fill="both")
#     root.mainloop()

import customtkinter as tk
import requests
import io
from PIL import Image, ImageTk
import webbrowser

class TechUpdatesFrame(tk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.loader_image = ImageTk.PhotoImage(Image.open('assets/images/loader.gif')) # Loader image
        self.loading_label = tk.CTkLabel(master=self, image=self.loader_image) # Create a label for loader image
        self.load_data()

    def load_data(self):
        # Fetch the data using the requests module in json format
        self.data = requests.get('https://newsapi.org/v2/everything?domains=techcrunch.com,thenextweb.com&apiKey=92b0d30aa4c941d18bec50e86abdd320').json()

        # Remove the loading screen and load the 1st NEWS Item
        self.clear()
        self.newsItem(0)
        
    def clear(self):
        for i in self.winfo_children():
            i.destroy()
        
    def newsItem(self,index):
        # clear screen for next news, old should be vanished
        self.clear()
        
        # ==================== Image of News Item ========================
        
        # If there is an issue with fetching the image then a default image will be loaded
        try:
            # Get the URL of Image
            self.image_url = self.data['articles'][index]['urlToImage']
            
            # Use requests module to get the image content
            response = requests.get(self.image_url)
            
            # Open the image using PIL
            image_data = Image.open(io.BytesIO(response.content)).resize((850, 500))
            
            # Convert the image for tkinter
            self.image = ImageTk.PhotoImage(image_data)
            
        except Exception as e:
            # If an error occurs, load a default image
            default_image = Image.open('assets/images/loader.gif').resize((850, 500))
            self.image = ImageTk.PhotoImage(default_image)
         
        # Created the label for image to display on screen
        self.img_frame = tk.CTkFrame(master=self, height=300, width=100)
        self.img_frame.grid(row=0, column=0, columnspan=3,)  

        self.image_label = tk.CTkLabel(self.img_frame, image=self.image,text="",corner_radius=50)
        self.image_label.grid(row=0, column=0, columnspan=3, sticky='nsew', pady=10,ipadx=12,ipady=15)

        self.label_text = "{}/{}".format(index+1, len(self.data['articles']))
        self.count_label=tk.CTkLabel(master=self,text=self.label_text,font=('Verdana', 20), wraplength=700, justify='left')
        self.count_label.grid(row=1, column=0, columnspan=3, pady=10, sticky='we', padx=(20, 20))
        
        # ==================== Heading of News Item ======================== 

         # ==================== Content Frame ========================
        
        # Creating the content frame
        self.content_frame = tk.CTkFrame(master=self, height=300, width=100)
        
        # Grid configuration to center the content frame
        # self.grid_rowconfigure(4, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        self.content_frame.grid(row=2, column=0, columnspan=3)  
        
        # Getting the heading of the news item
        self.heading = self.data['articles'][index]['title']
        
        # Creating the label for that news heading
        self.heading_label = tk.CTkLabel(self.content_frame, text=self.heading, font=('Verdana', 25,"bold"), wraplength=700, justify='left')
        
        # Packing it into the screen
        self.heading_label.grid(row=2, column=0, columnspan=3, pady=10, sticky='we', padx=(20, 20))
        
        # ==================== Description of News Item ========================
        
        # Getting the description of an news item
        self.description = self.data['articles'][index]['description']
        
        # Creating the label for the description 
        self.description_label = tk.CTkLabel(self.content_frame, text=self.description, wraplength=700, font=('Verdana', 15), justify='left')
        
        # Packing it into the screen
        self.description_label.grid(row=3, column=0, columnspan=3, pady=(0, 30), sticky='we', padx=(20, 20))
        
        # ==================== Navigation Buttons for Items ========================
        
        # Prev Button
        if index != 0:
            self.prev_btn = tk.CTkButton(self, text='Prev', width=80, height=50, font=('Verdana', 20, 'bold'), command=lambda: self.newsItem(index-1))
            self.prev_btn.grid(row=3, column=0, padx=(0, 10))
        
        # Read Button==>Changes as per News index for frame adjustment
        if index == 0:
            self.read_btn = tk.CTkButton(self, text='Read', width=80, height=50, font=('Verdana', 20, 'bold'), command=lambda: self.read_more(self.data['articles'][index]['url']))
            self.read_btn.grid(row=3, column=1, padx=(0, 10))
        elif 0 < index < len(self.data['articles']):
            self.read_btn = tk.CTkButton(self, text='Read', width=80, height=50, font=('Verdana', 20, 'bold'), command=lambda: self.read_more(self.data['articles'][index]['url']))
            self.read_btn.grid(row=3, column=1, padx=(0, 10))
        else:
            self.read_btn = tk.CTkButton(self, text='Read', width=80, height=50, font=('Verdana', 20, 'bold'), command=lambda: self.read_more(self.data['articles'][index]['url']))
            self.read_btn.grid(row=3, column=1, padx=(0, 10))
        
        # Next Button
        if len(self.data['articles']) != index+1:
            self.next_btn = tk.CTkButton(self, text='Next', width=80, height=50, font=('Verdana', 20, 'bold'), command=lambda: self.newsItem(index+1))
            self.next_btn.grid(row=3, column=2, padx=(0, 10))
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
    def read_more(self, url):
        webbrowser.open(url)

if __name__ == '__main__':
    root = tk.CTk()
    news_frame = TechUpdatesFrame(master=root)
    news_frame.mainloop()
