import tkinter as tk
from tkinter import filedialog, colorchooser, Label
import os

from src.ui.controls import ControlPanels
from src.ui.canvas import ImageCanvas
from PIL import Image, ImageTk
from src.utils.image_utils import ImageProcessor
from src.utils.grid_utils import GridRenderer, GridExporter
from scipy.special import comb
import numpy as np


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
        self.drawing_line = False
        self.line_start_x = 0
        self.line_start_y = 0
        self.current_line_id = None
        self.drawn_lines = []
        self.grid_color = "red"

        self.editing_line = False
        self.selected_line_id = None
        self.selected_point_index = None
        self.line_control_points = {} # Stores {line_id: [point_ids]}

        self.drawing_bezier = False
        self.bezier_points = []
        self.current_bezier_id = None
        self.drawn_bezier_curves = []

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
            'adjust_image_resize': self.adjust_image_resize,
            'update_grid': self.update_grid,
            'update_image_resize': self.update_image_resize,
            'start_drag': self.start_drag,
            'drag': self.drag,
            'end_drag': self.end_drag,
            'mouse_resize': self.mouse_resize,
            'start_line_draw': self.start_line_draw,
            'draw_line_drag': self.draw_line_drag,
            'end_line_draw': self.end_line_draw,
            'clear_lines': self.clear_lines,
            'adjust_canvas_zoom': self.adjust_canvas_zoom,
            'update_canvas_zoom': self.update_canvas_zoom,
            'start_bezier_draw': self.start_bezier_draw,
            'add_bezier_point': self.add_bezier_point,
            'end_bezier_draw': self.end_bezier_draw,
            'clear_bezier_curves': self.clear_bezier_curves,
            'toggle_line_edit_mode': self.toggle_line_edit_mode,
            'select_line_for_edit': self.select_line_for_edit,
            'drag_line_point': self.drag_line_point,
            'release_line_point': self.release_line_point
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
        new_value = self.controls.image_resize_scale.get() + amount
        if 0.1 <= new_value <= 10:
            self.controls.image_resize_scale.set(new_value)
            self.image_resize_factor = new_value
            self.update_grid()

    def reset_view(self):
        self.image_resize_factor = 1.0
        self.controls.image_resize_scale.set(1.0)
        self.pan_x = 0
        self.pan_y = 0
        self.update_grid()

    def update_image_resize(self, _=None):
        self.image_resize_factor = float(self.controls.image_resize_scale.get())
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

    def start_line_draw(self, event):
        self.drawing_line = True
        self.line_start_x = self.canvas_widget.canvas.canvasx(event.x)
        self.line_start_y = self.canvas_widget.canvas.canvasy(event.y)
        self.current_line_id = self.canvas_widget.draw_line(self.line_start_x, self.line_start_y, self.line_start_x, self.line_start_y, color="blue", width=2)

    def draw_line_drag(self, event):
        if not self.drawing_line:
            return
        
        current_x = self.canvas_widget.canvas.canvasx(event.x)
        current_y = self.canvas_widget.canvas.canvasy(event.y)
        self.canvas_widget.canvas.coords(self.current_line_id, self.line_start_x, self.line_start_y, current_x, current_y)

    def end_line_draw(self, event):
        self.drawing_line = False
        if self.current_line_id:
            self.drawn_lines.append(self.current_line_id)
        self.current_line_id = None

    def clear_lines(self):
        for line_id in self.drawn_lines:
            self.canvas_widget.delete_line(line_id)
        self.drawn_lines = []

    def bezier_curve(self, points, num_points=100):
        n_points = len(points)
        x_points = np.array([p[0] for p in points])
        y_points = np.array([p[1] for p in points])

        t = np.linspace(0.0, 1.0, num_points)

        polynomial_coefficients = comb(n_points - 1, range(n_points)) * (t ** np.arange(n_points)) * ((1 - t) ** (n_points - 1 - np.arange(n_points)))

        curve_x = np.dot(polynomial_coefficients, x_points)
        curve_y = np.dot(polynomial_coefficients, y_points)

        return list(zip(curve_x, curve_y))

    def start_bezier_draw(self, event):
        self.drawing_bezier = True
        self.bezier_points = []
        self.add_bezier_point(event)

    def add_bezier_point(self, event):
        if not self.drawing_bezier:
            return
        x, y = self.canvas_widget.canvas.canvasx(event.x), self.canvas_widget.canvas.canvasy(event.y)
        self.bezier_points.append((x, y))
        if len(self.bezier_points) > 1:
            if self.current_bezier_id:
                self.canvas_widget.delete_line(self.current_bezier_id)
            # Draw a temporary line or curve as feedback
            if len(self.bezier_points) == 2:
                self.current_bezier_id = self.canvas_widget.draw_line(self.bezier_points[0][0], self.bezier_points[0][1], x, y, color="purple", width=2)
            else:
                # For more than 2 points, draw a preview of the bezier curve
                curve_points = self.bezier_curve(self.bezier_points)
                self.current_bezier_id = self.canvas_widget.draw_bezier_curve(curve_points, color="purple", width=2)

    def end_bezier_draw(self, event):
        self.drawing_bezier = False
        if len(self.bezier_points) > 1:
            if self.current_bezier_id:
                self.canvas_widget.delete_line(self.current_bezier_id)
            curve_points = self.bezier_curve(self.bezier_points)
            bezier_id = self.canvas_widget.draw_bezier_curve(curve_points, color="purple", width=2)
            self.drawn_bezier_curves.append(bezier_id)
        self.bezier_points = []
        self.current_bezier_id = None

    def clear_bezier_curves(self):
        for bezier_id in self.drawn_bezier_curves:
            self.canvas_widget.delete_line(bezier_id)
        self.drawn_bezier_curves = []

    def clear_bezier_curves(self):
        for bezier_id in self.drawn_bezier_curves:
            self.canvas_widget.delete_line(bezier_id)
        self.drawn_bezier_curves = []

    def toggle_line_edit_mode(self):
        self.editing_line = not self.editing_line
        if self.editing_line:
            self.status_label.config(text="Line Edit Mode: ON. Click on a line to edit.")
            self.canvas_widget.canvas.bind("<ButtonPress-1>", self.select_line_for_edit)
            self.canvas_widget.canvas.bind("<B1-Motion>", self.drag_line_point)
            self.canvas_widget.canvas.bind("<ButtonRelease-1>", self.release_line_point)
        else:
            self.status_label.config(text="Line Edit Mode: OFF.")
            self.canvas_widget.canvas.bind("<ButtonPress-1>", self.start_drag)
            self.canvas_widget.canvas.bind("<B1-Motion>", self.drag)
            self.canvas_widget.canvas.bind("<ButtonRelease-1>", self.end_drag)
            self.canvas_widget.clear_control_points(self.line_control_points)
            self.selected_line_id = None
            self.selected_point_index = None

    def select_line_for_edit(self, event):
        if not self.editing_line:
            return
        
        x, y = self.canvas_widget.canvas.canvasx(event.x), self.canvas_widget.canvas.canvasy(event.y)
        
        # Check if a control point is clicked
        clicked_items = self.canvas_widget.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        for item_id in clicked_items:
            if item_id in [cp_id for sublist in self.line_control_points.values() for cp_id in sublist]:
                for line_id, cp_ids in self.line_control_points.items():
                    if item_id in cp_ids:
                        self.selected_line_id = line_id
                        self.selected_point_index = cp_ids.index(item_id)
                        self.canvas_widget.canvas.itemconfig(item_id, fill="green") # Highlight selected control point
                        return

        # If no control point is clicked, check if a line is clicked
        clicked_line_ids = self.canvas_widget.canvas.find_overlapping(x-2, y-2, x+2, y+2)
        for line_id in clicked_line_ids:
            if line_id in self.drawn_lines:
                self.selected_line_id = line_id
                self.canvas_widget.clear_control_points(self.line_control_points)
                self.line_control_points[line_id] = self.canvas_widget.draw_line_control_points(line_id)
                self.status_label.config(text=f"Selected line {line_id} for editing.")
                return
        
        self.selected_line_id = None
        self.selected_point_index = None
        self.canvas_widget.clear_control_points(self.line_control_points)
        self.status_label.config(text="No line selected.")

    def drag_line_point(self, event):
        if not self.editing_line or self.selected_line_id is None or self.selected_point_index is None:
            return
        
        x, y = self.canvas_widget.canvas.canvasx(event.x), self.canvas_widget.canvas.canvasy(event.y)
        
        coords = list(self.canvas_widget.canvas.coords(self.selected_line_id))
        coords[self.selected_point_index * 2] = x
        coords[self.selected_point_index * 2 + 1] = y
        self.canvas_widget.canvas.coords(self.selected_line_id, *coords)
        
        # Update control point position
        cp_id = self.line_control_points[self.selected_line_id][self.selected_point_index]
        self.canvas_widget.canvas.coords(cp_id, x-3, y-3, x+3, y+3)

    def release_line_point(self, event):
        if not self.editing_line or self.selected_line_id is None:
            return
        
        # Reset highlight for control point
        if self.selected_point_index is not None:
            cp_id = self.line_control_points[self.selected_line_id][self.selected_point_index]
            self.canvas_widget.canvas.itemconfig(cp_id, fill="blue")
        
        self.selected_point_index = None
        self.status_label.config(text=f"Line {self.selected_line_id} updated.")

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
            text=f"Loaded: {info['filename'] if info else 'None'} | Image Resize: {self.image_resize_factor:.1f}x | Canvas Zoom: {self.canvas_zoom_factor:.1f}x | {grid_info} | Color: {self.grid_color}")

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
            self.line_thickness, self.grid_color, self.image_resize_factor
        )
        
        if success:
            self.status_label.config(text=f"Exported image to: {file_path}")
        else:
            self.status_label.config(text="Export failed")


if __name__ == "__main__":
    root = tk.Tk()
    app = ArtGridApp(root)
    root.mainloop()