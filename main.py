import tkinter as tk
from tkinter import filedialog, colorchooser, Label
import os

from src.ui.controls import ControlPanels
from src.ui.canvas import ImageCanvas
from PIL import Image, ImageTk
from src.utils.image_utils import ImageProcessor
from src.utils.grid_utils import GridRenderer, GridExporter



class ArtGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Art Grid with Coordinates")
        self.root.geometry("1000x800")

        self.grid_size = 50
        self.grid_width = 50
        self.grid_height = 50
        self.line_thickness = 1
        self.image_resize_factor = 1.0
        self.canvas_zoom_factor = 1.0
        self.current_canvas_scale = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.grid_color = "red"
        self.drawn_lines = []

        self.image_processor = ImageProcessor()
        self.grid_renderer = GridRenderer()
        self.grid_exporter = GridExporter()

        callbacks = {
            'load_image': self.load_image,
            'reset_view': self.reset_view,
            'export_image': self.export_image,
            'choose_color': self.choose_color,
            'update_grid_type': self.update_grid_type,
            'adjust_grid_size': self.adjust_grid_size,
            'adjust_grid_width': self.adjust_grid_width,
            'adjust_grid_height': self.adjust_grid_height,
            'adjust_thickness': self.adjust_thickness,
            'update_grid': self.update_grid,
            'start_drag': self.start_drag,
            'drag': self.drag,
            'end_drag': self.end_drag,
            'mouse_resize': self.mouse_resize,
            'adjust_canvas_zoom': self.adjust_canvas_zoom,
            'update_canvas_zoom': self.update_canvas_zoom
        }

        self.controls = ControlPanels(root, callbacks)
        self.canvas_widget = ImageCanvas(root, callbacks)

        self.status_label = Label(
            root, text="Ready. Please load an image.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def update_grid_type(self):
        if self.controls.grid_type.get() == 0:
            self.controls.rect_grid_frame.pack_forget()
            self.controls.square_grid_frame.pack(
                side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            self.grid_width = self.grid_size
            self.grid_height = self.grid_size
            self.controls.grid_width_scale.set(self.grid_width)
            self.controls.grid_height_scale.set(self.grid_height)
        else:
            self.controls.square_grid_frame.pack_forget()
            self.controls.rect_grid_frame.pack(
                side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            self.grid_size = self.grid_width
            self.controls.grid_size_scale.set(self.grid_size)
        
        self.update_grid()

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if not file_path:
            return
        
        if self.image_processor.load_image(file_path):
            info = self.image_processor.get_image_info()
            self.status_label.config(text=f"Loaded: {info['filename']}")
            self.reset_view()

    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.grid_color,
                                      title="Choose Grid Color")
        if color[1]:
            self.grid_color = color[1]
            self.update_grid()

    def adjust_grid_size(self, amount):
        new_value = self.controls.grid_size_scale.get() + amount
        if 10 <= new_value <= 200:
            self.controls.grid_size_scale.set(new_value)
            self.grid_size = new_value
            
            if self.controls.grid_type.get() == 0:
                self.grid_width = new_value
                self.grid_height = new_value
                self.controls.grid_width_scale.set(new_value)
                self.controls.grid_height_scale.set(new_value)
            
            self.update_grid()

    def adjust_grid_width(self, amount):
        new_value = self.controls.grid_width_scale.get() + amount
        if 10 <= new_value <= 200:
            self.controls.grid_width_scale.set(new_value)
            self.grid_width = new_value
            self.update_grid()

    def adjust_grid_height(self, amount):
        new_value = self.controls.grid_height_scale.get() + amount
        if 10 <= new_value <= 200:
            self.controls.grid_height_scale.set(new_value)
            self.grid_height = new_value
            self.update_grid()

    def adjust_thickness(self, amount):
        new_value = self.controls.thickness_scale.get() + amount
        if 1 <= new_value <= 10:
            self.controls.thickness_scale.set(new_value)
            self.line_thickness = new_value
            self.update_grid()

    def adjust_image_resize(self, amount):
        new_value = self.controls.canvas_zoom_scale.get() + amount
        if 0.1 <= new_value <= 10:
            self.controls.canvas_zoom_scale.set(new_value)
            self.image_resize_factor = new_value
            self.update_grid()

    def reset_view(self):
        self.image_resize_factor = 1.0
        self.controls.canvas_zoom_scale.set(1.0)
        self.pan_x = 0
        self.pan_y = 0
        self.update_grid()

    def update_image_resize(self, _=None):
        self.image_resize_factor = float(self.controls.canvas_zoom_scale.get())
        self.update_grid()

    def adjust_canvas_zoom(self, amount):
        new_value = self.controls.canvas_zoom_scale.get() + amount
        if 0.1 <= new_value <= 10:
            self.controls.canvas_zoom_scale.set(new_value)
            self.canvas_zoom_factor = new_value
            self.update_grid()

    def update_canvas_zoom(self, _=None):
        self.canvas_zoom_factor = float(self.controls.canvas_zoom_scale.get())
        self.update_grid()

    def mouse_resize(self, event):
        x, y = self.canvas_widget.canvas.canvasx(event.x), self.canvas_widget.canvas.canvasy(event.y)

        if event.num == 4 or event.delta > 0:
            zoom_factor = 1.1
        elif event.num == 5 or event.delta < 0:
            zoom_factor = 0.9
        else:
            return

        new_zoom = self.canvas_zoom_factor * zoom_factor

        if 0.1 <= new_zoom <= 10:
            self.pan_x = x - (x - self.pan_x) * zoom_factor
            self.pan_y = y - (y - self.pan_y) * zoom_factor

            self.canvas_zoom_factor = new_zoom
            self.controls.canvas_zoom_scale.set(new_zoom)

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

    

    def update_grid(self, _=None):
        if self.image_processor.original_image is None:
            return

        if self.controls.grid_type.get() == 0:
            self.grid_size = self.controls.grid_size_scale.get()
            grid_width = self.grid_size
            grid_height = self.grid_size
        else:
            self.grid_width = self.controls.grid_width_scale.get()
            self.grid_height = self.controls.grid_height_scale.get()
            grid_width = self.grid_width
            grid_height = self.grid_height

        self.line_thickness = self.controls.thickness_scale.get()

        canvas_width = self.canvas_widget.canvas.winfo_width()
        canvas_height = self.canvas_widget.canvas.winfo_height()

        if canvas_width <= 1:
            self.root.after(100, self.update_grid)
            return

        displayed_image, original_scaled_width, original_scaled_height = self.image_processor.resize_image(self.image_resize_factor)
        
        # Apply canvas zoom to the image
        scaled_width = int(original_scaled_width * self.canvas_zoom_factor)
        scaled_height = int(original_scaled_height * self.canvas_zoom_factor)
        
        # Resize the displayed image based on canvas zoom
        if displayed_image:
            displayed_image = displayed_image.resize((scaled_width, scaled_height), Image.LANCZOS)
            self.canvas_widget.canvas.image = ImageTk.PhotoImage(displayed_image) # Keep a reference!
            displayed_image = self.canvas_widget.canvas.image

        self.canvas_widget.canvas.delete("image_tag")
        self.canvas_widget.canvas.delete("grid_tag")
        self.canvas_widget.canvas.delete("coordinate_tag")
        # Preserve drawn lines by not deleting them here
        for line_id in self.drawn_lines:
            self.canvas_widget.canvas.tag_raise(line_id)

        img_x = canvas_width//2 - scaled_width//2 + self.pan_x
        img_y = canvas_height//2 - scaled_height//2 + self.pan_y

        if displayed_image:
            self.canvas_widget.canvas.create_image(img_x, img_y, image=displayed_image, anchor=tk.NW, tags="image_tag")

        scaled_grid_width = grid_width
        scaled_grid_height = grid_height

        if scaled_grid_width < 5:
            scaled_grid_width = 5
        if scaled_grid_height < 5:
            scaled_grid_height = 5

        self.grid_renderer.draw_grid_on_canvas(
            self.canvas_widget.canvas, img_x, img_y, original_scaled_width, original_scaled_height,
            scaled_grid_width, scaled_grid_height, self.line_thickness, self.grid_color, self.canvas_zoom_factor
        )
        
        self.grid_renderer.draw_coordinates_on_canvas(
            self.canvas_widget.canvas, img_x, img_y, original_scaled_width, original_scaled_height,
            scaled_grid_width, scaled_grid_height, self.canvas_zoom_factor
        )

        info = self.image_processor.get_image_info()
        grid_info = f"Grid: {grid_width}x{grid_height}px" if self.controls.grid_type.get() == 1 else f"Grid: {self.grid_size}px"
        self.status_label.config(
            text=f"Loaded: {info['filename'] if info else 'None'} | Canvas Zoom: {self.canvas_zoom_factor:.1f}x | {grid_info} | Color: {self.grid_color}")

    def export_image(self):
        if self.image_processor.original_image is None:
            self.status_label.config(text="No image loaded to export")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                       ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if not file_path:
            return

        if self.controls.grid_type.get() == 0:
            grid_width = self.grid_size
            grid_height = self.grid_size
        else:
            grid_width = self.grid_width
            grid_height = self.grid_height

        success = self.grid_exporter.export_image_with_grid(
            self.image_processor.original_image, file_path, grid_width, grid_height,
            self.line_thickness, self.grid_color, 1.0
        )
        
        if success:
            self.status_label.config(text=f"Exported image to: {file_path}")
        else:
            self.status_label.config(text="Export failed")


if __name__ == "__main__":
    root = tk.Tk()
    app = ArtGridApp(root)
    root.mainloop()