import customtkinter as tk

class Application:
    def __init__(self):
        self.pieces = []

        # Set theme
        tk.set_appearance_mode("Dark")
        tk.set_default_color_theme('themes/red.json')
        self.my_font = lambda size: tk.CTkFont(size=size, weight='bold', family='Ariel')

        # Configure app window
        self.root = tk.CTk()
        self.root.geometry('440x440')
        self.root.title('Checkers')
        self.root.resizable(False, False)

        # Canvas
        self.canvas = tk.CTkCanvas(self.root, width=400, height=400, bg='black')
        self.canvas.pack(padx=20, pady=20)
        self.canvas.bind('<Button-1>', self.on_canvas_click)

        # Run app
        self.draw_board()
        self.root.mainloop()

    
    def draw_board(self):
        for y in range(8):
            for x in range(0, 7, 2):
                self.canvas.create_rectangle((x+y%2)*50, y*50, (x+y%2)*50+50, y*50+50, fill='white')

    
    def draw_pieces(self):
        pass


    def on_canvas_click(self, event):
        x = event.x // 50
        y = event.y // 50
        print(x, y)

    
if __name__ == '__main__':
    app = Application()
