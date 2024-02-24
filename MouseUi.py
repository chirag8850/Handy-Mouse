import sys
import tkinter as tk
from PIL import ImageTk, Image

class HandyMouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HandyMouse")
        self.root.geometry("400x400")

        self.WIDTH = 400
        self.HEIGHT = 400

        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(fill="both", expand=True)

        self.load_background_image()

        self.create_title()

        self.create_buttons()

    def load_background_image(self):
        background_photo = Image.open('aiHand.png')
        resized_image = background_photo.resize((self.WIDTH, self.HEIGHT),  Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(resized_image)
        self.background = self.canvas.create_image(0, 0, image=self.background_image, anchor=tk.NW)

    def create_title(self):
        self.title_text = self.canvas.create_text(
            self.WIDTH // 2, 40, text="AI Virtual Mouse", font=("Helvetica", 20), fill="white"
        )

    def start_script(self):
        exec(open('AiVirtualMouseProject.py').read())

    def exit_app(self):
        self.root.quit()
        sys.exit()

    def create_buttons(self):
        start_button = tk.Button(self.root, text="Start", padx=40, pady=5, command=self.start_script, fg="white", bg="green")
        exit_button = tk.Button(self.root, text="Exit", padx=40, pady=5, command=self.exit_app, fg="white", bg="red")

        self.start_button = self.canvas.create_window(30, 200, anchor="w", window=start_button)
        self.exit_button = self.canvas.create_window(self.WIDTH - 30, 200, anchor="e", window=exit_button)

def main():
    root = tk.Tk()
    app = HandyMouseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
