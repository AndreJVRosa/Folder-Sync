import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ParentWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Sync Program")
        
        # Set custom size
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Set custom font and font size
        custom_font = ("Arial", 13)  # Replace with your custom font
        ttk.Style().configure("TButton", font=custom_font)

        

        # Add buttons with custom shapes and sizes
        btn1 = ttk.Button(self.root, text="Select", command=self.button1_click, style="TButton")
        btn1.place(relx=0.5, rely=0.3, anchor="center", width=150, height=50)  # Adjust position, width, and height

        btn2 = ttk.Button(self.root, text="Exit", command=self.button2_click, style="TButton")
        btn2.place(relx=0.5, rely=0.5, anchor="center", width=150, height=50)  # Adjust position, width, and height

        # Set window attributes
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.attributes("-topmost", True)  # Bring the window to the front


    def button1_click(self):
        messagebox.showinfo("Button 1 Clicked", "Button 1 was clicked!")

    def button2_click(self):
        messagebox.showinfo("Button 2 Clicked", "Button 2 was clicked!")

    def on_close(self):
        if messagebox.askokcancel("Close", "Do you want to close the application?"):
            self.root.destroy()




if __name__ == "__main__":
    root = tk.Tk()
    app = ParentWindow(root)
    root.mainloop()

