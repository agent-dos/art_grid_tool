import tkinter as tk
from tkinter import filedialog, Scale, Label, Button, Frame
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import string

class ArtGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Art Grid with Coordinates")
        self.root.geometry("1000x800")
        
        # Variables
        self.image_path = None
        self.original_image = None
        self.displayed_image = None
        self.grid_size = 50
        self.line_thickness = 1
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Create frames
        self.control_frame = Frame(root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        self.canvas_frame = Frame(root)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Controls
        Button(self.control_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT, padx=5)
        
        Label(self.control_frame, text="Grid Size:").pack(side=tk.LEFT, padx=5)
        self.grid_size_scale = Scale(self.control_frame, from_=10, to=200, orient=tk.HORIZONTAL, 
                                    length=150, command=self.update_grid)
        self.grid_size_scale.set(self.grid_size)
        self.grid_size_scale.pack(side=tk.LEFT, padx=5)
        
        Label(self.control_frame, text="Line Thickness:").pack(side=tk.LEFT, padx=5)
        self.thickness_scale = Scale(self.control_frame, from_=1, to=10, orient=tk.HORIZONTAL, 
                                    length=150, command=self.update_grid)
        self.thickness_scale.set(self.line_thickness)
        self.thickness_scale.pack(side=tk.LEFT, padx=5)
        
        # Zoom controls
        Label(self.control_frame, text="Zoom:").pack(side=tk.LEFT, padx=5)
        self.zoom_scale = Scale(self.control_frame, from_=1, to=10, resolution=0.1, orient=tk.HORIZONTAL, 
                               length=150, command=self.update_zoom)
        self.zoom_scale.set(self.zoom_level)
        self.zoom_scale.pack(side=tk.LEFT, padx=5)
        
        Button(self.control_frame, text="Reset View", command=self.reset_view).pack(side=tk.LEFT, padx=5)
        Button(self.control_frame, text="Export", command=self.export_image).pack(side=tk.LEFT, padx=5)
        
        # Canvas
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<MouseWheel>", self.mouse_zoom)  # Windows
        self.canvas.bind("<Button-4>", self.mouse_zoom)    # Linux scroll up
        self.canvas.bind("<Button-5>", self.mouse_zoom)    # Linux scroll down
        
        # Status label
        self.status_label = Label(root, text="Ready. Please load an image.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if not file_path:
            return
            
        self.image_path = file_path
        self.original_image = Image.open(file_path)
        self.status_label.config(text=f"Loaded: {os.path.basename(file_path)}")
        
        # Reset view when loading new image
        self.reset_view()
    
    def reset_view(self):
        self.zoom_level = 1.0
        self.zoom_scale.set(1.0)
        self.pan_x = 0
        self.pan_y = 0
        self.update_grid()
    
    def update_zoom(self, _=None):
        self.zoom_level = float(self.zoom_scale.get())
        self.update_grid()
    
    def mouse_zoom(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        
        if event.num == 4 or event.delta > 0:
            zoom_factor = 1.1
        elif event.num == 5 or event.delta < 0:
            zoom_factor = 0.9
        else:
            return
        
        new_zoom = self.zoom_level * zoom_factor
        
        if 0.1 <= new_zoom <= 10:
            self.pan_x = x - (x - self.pan_x) * zoom_factor
            self.pan_y = y - (y - self.pan_y) * zoom_factor
            
            self.zoom_level = new_zoom
            self.zoom_scale.set(new_zoom)
            
            self.update_grid()
    
    def start_drag(self, event):
        self.dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def drag(self, event):
        if not self.dragging:
            return
        
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        
        self.pan_x += dx
        self.pan_y += dy
        
        self.update_grid()
    
    def end_drag(self, event):
        self.dragging = False
    
    def get_column_letter(self, col_num):
        # Convert column number to Excel-style letter (A, B, C... Z, AA, AB...)
        result = ""
        while col_num >= 0:
            remainder = col_num % 26
            result = string.ascii_uppercase[remainder] + result
            col_num = col_num // 26 - 1
            if col_num < 0:
                break
        return result
    
    def update_grid(self, _=None):
        if self.original_image is None:
            return
            
        self.grid_size = self.grid_size_scale.get()
        self.line_thickness = self.thickness_scale.get()
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            self.root.after(100, self.update_grid)
            return
            
        img_width, img_height = self.original_image.size
        
        scaled_width = int(img_width * self.zoom_level)
        scaled_height = int(img_height * self.zoom_level)
        
        resized_image = self.original_image.resize((scaled_width, scaled_height), Image.LANCZOS)
        self.displayed_image = ImageTk.PhotoImage(resized_image)
        
        self.canvas.delete("all")
        
        img_x = canvas_width//2 - scaled_width//2 + self.pan_x
        img_y = canvas_height//2 - scaled_height//2 + self.pan_y
        
        self.canvas.create_image(img_x, img_y, image=self.displayed_image, anchor=tk.NW)
        
        scaled_grid_size = int(self.grid_size * self.zoom_level)
        if scaled_grid_size < 5:
            scaled_grid_size = 5
            
        # Draw grid lines
        for x in range(0, scaled_width + 1, scaled_grid_size):
            x_pos = img_x + x
            self.canvas.create_line(x_pos, img_y, x_pos, img_y + scaled_height, 
                                   width=self.line_thickness, fill="red")
            
        for y in range(0, scaled_height + 1, scaled_grid_size):
            y_pos = img_y + y
            self.canvas.create_line(img_x, y_pos, img_x + scaled_width, y_pos, 
                                   width=self.line_thickness, fill="red")
        
        # Add column letters across the top (centered in each grid cell)
        for x in range(0, scaled_width, scaled_grid_size):
            col_letter = self.get_column_letter(x // scaled_grid_size)
            cell_center_x = img_x + x + scaled_grid_size // 2
            self.canvas.create_text(cell_center_x, img_y - 15, 
                                  text=col_letter, fill="blue", 
                                  font=("Arial", max(8, min(12, scaled_grid_size // 4))))
        
        # Add row numbers along the left side (centered in each grid cell)
        for y in range(0, scaled_height, scaled_grid_size):
            row_num = y // scaled_grid_size + 1
            cell_center_y = img_y + y + scaled_grid_size // 2
            self.canvas.create_text(img_x - 15, cell_center_y, 
                                  text=str(row_num), fill="blue", 
                                  font=("Arial", max(8, min(12, scaled_grid_size // 4))))
        
        self.status_label.config(text=f"Loaded: {os.path.basename(self.image_path) if self.image_path else 'None'} | Zoom: {self.zoom_level:.1f}x")

    def export_image(self):
        if self.original_image is None:
            self.status_label.config(text="No image loaded to export")
            return
        
        # Get save file location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        # Calculate the space needed for coordinates
        margin = max(30, self.grid_size // 2)
        
        # Create a new image with margins for coordinates
        img_width, img_height = self.original_image.size
        export_width = img_width + margin * 2
        export_height = img_height + margin * 2
        
        export_image = Image.new('RGBA', (export_width, export_height), (255, 255, 255, 255))
        export_image.paste(self.original_image, (margin, margin))
        
        # Create a drawing context
        draw = ImageDraw.Draw(export_image)
        
        # Try to load a font, use default if not available
        try:
            font = ImageFont.truetype("arial.ttf", max(10, min(16, self.grid_size // 3)))
        except IOError:
            font = ImageFont.load_default()
        
        # Draw grid lines
        for x in range(0, img_width + 1, self.grid_size):
            draw.line([(x + margin, margin), (x + margin, img_height + margin)], 
                     fill="red", width=self.line_thickness)
            
        for y in range(0, img_height + 1, self.grid_size):
            draw.line([(margin, y + margin), (img_width + margin, y + margin)], 
                     fill="red", width=self.line_thickness)
        
        # Add column letters across the top
        for x in range(0, img_width, self.grid_size):
            col_letter = self.get_column_letter(x // self.grid_size)
            cell_center_x = x + margin + self.grid_size // 2
            
            # Get text size for centering
            text_width, text_height = draw.textsize(col_letter, font=font) if hasattr(draw, 'textsize') else (self.grid_size // 3, self.grid_size // 3)
            
            draw.text(
                (cell_center_x - text_width // 2, margin // 2 - text_height // 2),
                col_letter, 
                fill="blue", 
                font=font
            )
        
        # Add row numbers along the left side
        for y in range(0, img_height, self.grid_size):
            row_num = str(y // self.grid_size + 1)
            cell_center_y = y + margin + self.grid_size // 2
            
            # Get text size for centering
            text_width, text_height = draw.textsize(row_num, font=font) if hasattr(draw, 'textsize') else (self.grid_size // 3, self.grid_size // 3)
            
            draw.text(
                (margin // 2 - text_width // 2, cell_center_y - text_height // 2),
                row_num, 
                fill="blue", 
                font=font
            )
        
        # Save the image
        export_image.save(file_path)
        self.status_label.config(text=f"Exported image to: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ArtGridApp(root)
    root.mainloop()