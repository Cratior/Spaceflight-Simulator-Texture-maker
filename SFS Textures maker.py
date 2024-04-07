from PIL import Image, ImageTk
import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
import sv_ttk

class TextureGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Texture Generator")
        self.master.geometry("600x450")
        self.output_directory = ""
        self.current_frame = None
        
        self.create_widgets()
        
    def create_widgets(self):
        self.frame_selection = ttk.Frame(self.master)
        self.frame_selection.pack(pady=10)
        
        ttk.Button(self.frame_selection, text="Select Output Directory", command=self.select_output_directory).grid(row=0, column=0, columnspan=2, padx=10)
        
        self.btn_color_generator = ttk.Button(self.frame_selection, text="Color Texture Generator", command=self.show_color_generator)
        self.btn_color_generator.grid(row=1, column=0, padx=10)
        
        self.btn_image_generator = ttk.Button(self.frame_selection, text="Image Texture Generator", command=self.show_image_generator)
        self.btn_image_generator.grid(row=1, column=1, padx=10)
        
        self.show_color_generator()  # Show Color Texture Generator by default
    
    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory(title="Select Output Directory")
    
    def show_color_generator(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.master)
        self.current_frame.pack(pady=10)
        
        self.colors_entries = []
        self.next_row = 0
        self.next_column = 0
        
        # Add the "Save Colors" and "Add Color Entry" buttons
        ttk.Button(self.current_frame, text="Save Colors", command=self.save_colors).grid(row=self.next_row, column=0, columnspan=2, pady=5)
        ttk.Button(self.current_frame, text="Add Color Entry", command=self.add_color_entry).grid(row=self.next_row, column=3, columnspan=2, pady=5)
        
        # Create the grid layout for color entries
        for i in range(16):  # 8 rows x 2 columns
            if self.next_column == 2:
                self.next_column = 0
                self.next_row += 1
            
            ttk.Frame(self.current_frame, width=50, height=30).grid(row=self.next_row + 1, column=self.next_column, padx=10, pady=5)
            self.next_column += 1
    def add_color_entry(self):
        color_entry_frame = ttk.Frame(self.current_frame, width=50, height=30)
        color_entry_frame.grid(row=self.next_row + 1, column=self.next_column)
        
        hex_color = '#FFFFFF'  # Default color
        color_preview = tk.Label(color_entry_frame, width=3, bg=hex_color)
        color_preview.grid(row=0, column=0)
        
        color_entry = ttk.Entry(color_entry_frame, width=8)  # Adjusted width for color code
        color_entry.grid(row=0, column=1)
        color_entry.insert(0, hex_color)
        
        def remove_color():
            color_entry_frame.destroy()
            self.colors_entries.remove(color_entry_frame)
            self.rearrange_color_entries()
            
        remove_button = ttk.Button(color_entry_frame, text="X", command=remove_color)
        remove_button.grid(row=0, column=2, padx=5)
        
        def pick_color(entry=color_entry, preview=color_preview):
            color = colorchooser.askcolor(initialcolor=entry.get())
            if color[1]:
                entry.delete(0, tk.END)
                entry.insert(0, color[1])
                preview.config(bg=color[1])
        
        pick_color_button = ttk.Button(color_entry_frame, text="Pick Color", command=lambda: pick_color(color_entry, color_preview))
        pick_color_button.grid(row=0, column=3)
        
        self.colors_entries.append(color_entry_frame)
        self.rearrange_color_entries()
        
    def rearrange_color_entries(self):
        self.next_row = 0
        self.next_column = 0
        for color_entry_frame in self.colors_entries:
            color_entry_frame.grid(row=self.next_row + 1, column=self.next_column)
            self.next_column += 1
            if self.next_column == 2:
                self.next_column = 0
                self.next_row += 1
    
    def save_colors(self):
        if not self.output_directory:
            tk.messagebox.showerror("Error", "Please select an output directory.")
            return

        for color_entry_frame in self.colors_entries:
            color_entry = color_entry_frame.winfo_children()[1]  # Get the color entry widget
            hex_color = color_entry.get()

            image = Image.new("RGB", (32, 32), hex_color)
            image_path = os.path.join(self.output_directory, "Textures", f"Color_{hex_color}.png")
            image.save(image_path)
            json_content = {
                "colorTex": {
                    "textures": [
                        {
                            "texture": f"Color_{hex_color}.png",
                            "ideal": 0.0
                        }
                    ],
                    "border_Bottom": {
                        "uvSize": 0.0,
                        "sizeMode": 0,
                        "size": 0.5
                    },
                    "border_Top": {
                        "uvSize": 0.0,
                        "sizeMode": 0,
                        "size": 0.5
                    },
                    "center": {
                        "mode": 0,
                        "sizeMode": 0,
                        "size": 0.5,
                        "logoHeightPercent": 0.5,
                        "scaleLogoToFit": False
                    },
                    "fixedWidth": False,
                    "fixedWidthValue": 1.0,
                    "flipToLight_X": False,
                    "flipToLight_Y": False,
                    "metalTexture": False,
                    "icon": None
                },
                "tags": ["tank", "cone", "fairing"],
                "pack_Redstone_Atlas": False,
                "multiple": False,
                "segments": [],
                "name": f"Color_{hex_color}",
                "hideFlags": 0
            }
            
            txt_path = os.path.join(self.output_directory, "Color Textures", f"Color_{hex_color}.txt")
            with open(txt_path, "w") as txt_file:
                txt_file.write(json.dumps(json_content, indent=2))
    
    def show_image_generator(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self.master)
        self.current_frame.pack(pady=10)
        
        self.select_image_button = ttk.Button(self.current_frame, text="Select Image", command=self.select_image)
        self.select_image_button.pack()
    
    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        self.save_image(file_path)
    
    def save_image(self, selected_image_path):
        if not self.output_directory:
            tk.messagebox.showerror("Error", "Please select an output directory.")
            return
        
        if selected_image_path:
            image = Image.open(selected_image_path)
            image_name = os.path.basename(selected_image_path)
            image_path = os.path.join(self.output_directory, "Textures", image_name)
            image.save(image_path)

            json_content = {
                "colorTex": {
                    "textures": [
                        {
                            "texture": image_name,
                            "ideal": 0.0
                        }
                    ],
                    "border_Bottom": {
                        "uvSize": 0.0,
                        "sizeMode": 0,
                        "size": 0.5
                    },
                    "border_Top": {
                        "uvSize": 0.0,
                        "sizeMode": 0,
                        "size": 0.5
                    },
                    "center": {
                        "mode": 0,
                        "sizeMode": 0,
                        "size": 0.5,
                        "logoHeightPercent": 0.5,
                        "scaleLogoToFit": False
                    },
                    "fixedWidth": False,
                    "fixedWidthValue": 1.0,
                    "flipToLight_X": False,
                    "flipToLight_Y": False,
                    "metalTexture": False,
                    "icon": None
                },
                "tags": ["tank", "cone", "fairing"],
                "pack_Redstone_Atlas": False,
                "multiple": False,
                "segments": [],
                "name": os.path.splitext(image_name)[0],
                "hideFlags": 0
            }

            txt_path = os.path.join(self.output_directory, "Color Textures", f"{os.path.splitext(image_name)[0]}.txt")
            with open(txt_path, "w") as txt_file:
                txt_file.write(json.dumps(json_content, indent=2))

            print("Image and TXT file created successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    sv_ttk.set_theme("dark")  # Set the theme to dark
    app = TextureGeneratorApp(root)
    root.mainloop()
