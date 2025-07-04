import tkinter as tk
from tkinter import filedialog, colorchooser, Label
import os

from src.ui.controls import ControlPanels
from src.ui.canvas import ImageCanvas
from PIL import Image, ImageTk
from src.utils.image_utils import ImageProcessor
from src.utils.grid_utils import GridRenderer, GridExporter
from src.utils.unit_converter import UnitConverter



class ArtGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Art Grid with Coordinates")
        self.root.geometry("1000x800")

        self.grid_size = 1.0
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
            'adjust_grid_size': self.adjust_grid_size,
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



    def calculate_resize_factor(self):
        """Calculate the resize factor based on user's target dimensions"""
        if not self.controls.resize_enabled.get():
            return 1.0
            
        try:
            target_value = float(self.controls.resize_value.get())
            target_unit = self.controls.resize_unit.get()
            dimension = self.controls.resize_dimension.get()
            
            # Convert target to pixels
            target_pixels = UnitConverter.to_pixels(target_value, target_unit)
            
            # Get current image dimensions
            original_width, original_height = self.image_processor.original_image.size
            
            if dimension == 'width':
                resize_factor = target_pixels / original_width
            else:  # height
                resize_factor = target_pixels / original_height
                
            return max(0.1, min(10.0, resize_factor))  # Clamp between 0.1x and 10x
            
        except (ValueError, AttributeError, ZeroDivisionError):
            return 1.0

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
        current_unit = self.controls.grid_unit.get()
        
        # Adjust increment based on unit
        if current_unit == 'mm':
            increment = amount * 0.1
        elif current_unit == 'cm':
            increment = amount * 0.1
        elif current_unit == 'inch':
            increment = amount * 0.1
        else:  # px
            increment = amount
            
        new_value = self.controls.grid_size_scale.get() + increment
        if 0.1 <= new_value <= 50:
            self.controls.grid_size_scale.set(new_value)
            self.grid_size = new_value
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
        # Reset image resize controls
        self.controls.resize_enabled.set(0)
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

        # Get the current unit
        current_unit = self.controls.grid_unit.get()

        # Manual size mode: use square grid controls
        self.grid_size = self.controls.grid_size_scale.get()
        # Convert grid size to pixels
        grid_width = int(UnitConverter.to_pixels(self.grid_size, current_unit))
        grid_height = int(UnitConverter.to_pixels(self.grid_size, current_unit))

        self.line_thickness = self.controls.thickness_scale.get()

        canvas_width = self.canvas_widget.canvas.winfo_width()
        canvas_height = self.canvas_widget.canvas.winfo_height()

        if canvas_width <= 1:
            self.root.after(100, self.update_grid)
            return

        # Calculate resize factor based on user input
        target_resize_factor = self.calculate_resize_factor()
        displayed_image, original_scaled_width, original_scaled_height = self.image_processor.resize_image(target_resize_factor)
        
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

        # Grid size should remain constant in actual units, not scaled with image
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
        
        # Create image size tooltip with all units
        size_info = ""
        if info and self.image_processor.original_image:
            original_width, original_height = self.image_processor.original_image.size
            
            # Get resized dimensions if resize is enabled
            target_resize_factor = self.calculate_resize_factor()
            current_width = int(original_width * target_resize_factor)
            current_height = int(original_height * target_resize_factor)
            
            # Convert to all units
            def format_size_all_units(width_px, height_px):
                cm_w = UnitConverter.from_pixels(width_px, 'cm')
                cm_h = UnitConverter.from_pixels(height_px, 'cm')
                mm_w = UnitConverter.from_pixels(width_px, 'mm')
                mm_h = UnitConverter.from_pixels(height_px, 'mm')
                inch_w = UnitConverter.from_pixels(width_px, 'inch')
                inch_h = UnitConverter.from_pixels(height_px, 'inch')
                
                return f"{width_px}×{height_px}px | {cm_w:.1f}×{cm_h:.1f}cm | {mm_w:.0f}×{mm_h:.0f}mm | {inch_w:.2f}×{inch_h:.2f}in"
            
            if target_resize_factor != 1.0:
                size_info = f"Original: {format_size_all_units(original_width, original_height)} | Current: {format_size_all_units(current_width, current_height)}"
            else:
                size_info = f"Size: {format_size_all_units(original_width, original_height)}"
        
        # Add canvas zoom info
        zoom_info = f"Canvas Zoom: {self.canvas_zoom_factor:.1f}x"
        
        # Build status message
        filename = info['filename'] if info else 'None'
        if size_info:
            self.status_label.config(text=f"Loaded: {filename} | {zoom_info} | {size_info}")
        else:
            self.status_label.config(text=f"Loaded: {filename} | {zoom_info}")

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

        # Calculate grid dimensions for export (manual size mode)
        current_unit = self.controls.grid_unit.get()
        grid_width = int(UnitConverter.to_pixels(self.grid_size, current_unit))
        grid_height = int(UnitConverter.to_pixels(self.grid_size, current_unit))

        # Use the resize factor for export (canvas zoom is display-only)
        target_resize_factor = self.calculate_resize_factor()
        dpi = UnitConverter.DEFAULT_DPI
        success = self.grid_exporter.export_image_with_grid(
            self.image_processor.original_image, file_path, grid_width, grid_height,
            self.line_thickness, self.grid_color, target_resize_factor, dpi
        )
        
        if success:
            self.status_label.config(text=f"Exported image to: {file_path}")
        else:
            self.status_label.config(text="Export failed")


if __name__ == "__main__":
    root = tk.Tk()
    app = ArtGridApp(root)
    root.mainloop()