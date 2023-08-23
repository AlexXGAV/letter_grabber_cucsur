"""
Capturador de letras
Aplicación para capturar y guardar datos de coordenadas X,Y y tiempo 
de letras manuscritas en un recuadro de maximo 400x400 de resolución.
"""
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        self.root.geometry("500x600")  # Tamaño fijo para la ventana

        self.content_frame = tk.Frame(root)
        self.content_frame.pack(fill="both", expand=True)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.content_frame, width=400, height=400, bg="lightgray")
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        self.name_label = tk.Label(root, text="Nombre:")
        self.name_label.pack()
        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.grade_label = tk.Label(root, text="Promedio escolar:")
        self.grade_label.pack()
        self.grade_entry = tk.Entry(root)
        self.grade_entry.pack()

        self.letter_label = tk.Label(root, text="Letra:")
        self.letter_label.pack()
        self.letter_entry = tk.Entry(root)
        self.letter_entry.pack()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        self.capture_button = tk.Button(self.buttons_frame, text="Capture", command=self.capture, bg="green", fg="white", padx=5, width=10)
        self.capture_button.grid(row=0, column=0, padx=(0, 100), pady=(10, 10))

        self.clear_button = tk.Button(self.buttons_frame, text="Clear", command=self.clear, bg="red", fg="white", padx=5, width=10)
        self.clear_button.grid(row=0, column=1, padx=(100, 0), pady=(10, 10))

        self.coordinates = []
        self.current_stroke = []
        self.is_drawing = False

    def start_drawing(self, event):
        self.is_drawing = True
        self.current_stroke = [(event.x, 400 - event.y, datetime.now())]  # Inverting Y

    def draw(self, event):
        if self.is_drawing:
            x, y = event.x, event.y
            self.current_stroke.append((x, 400 - y, datetime.now()))  # Inverting Y
            self.canvas.create_oval(x, y, x + 2, y + 2, fill="black")

    def stop_drawing(self, event):
        if self.is_drawing:
            self.coordinates.append(self.current_stroke)
            self.current_stroke = []
            self.is_drawing = False

    def capture(self):
        name = self.name_entry.get()
        grade = self.grade_entry.get()
        letter = self.letter_entry.get()

        if not name or not grade or not letter:
            tk.messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        folder_name = f"{name.lower()}-{grade}"
        os.makedirs(folder_name, exist_ok=True)

        #timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(folder_name, f"{name.lower()}-{grade}-{letter.upper()}.txt")

        with open(filename, "w") as file:
            file.write("Time,X,Y\n")
            for stroke in self.coordinates:
                for x, y, time in stroke:
                    time_ms = (time - self.coordinates[0][0][2]).total_seconds() * 1000
                    file.write(f"{time_ms},{x},{y}\n")
                if not self.is_drawing:
                    file.write(f"{time_ms},NaN,NaN\n")

        print("Data captured and saved to", filename)

    def clear(self):
        self.canvas.delete("all")
        self.coordinates = []

root = tk.Tk()
root.resizable(False, False)  # Evitar redimensionar la ventana
app = DrawingApp(root)
root.mainloop()
