import tkinter as tk
from tkinter import Scale, Label, Button, Frame, Radiobutton, IntVar, ttk


class ControlPanels:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.grid_type = IntVar(value=0)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.grid_tab = Frame(self.notebook)
        self.drawing_tab = Frame(self.notebook)

        self.notebook.add(self.grid_tab, text="Grid Controls")
        self.notebook.add(self.drawing_tab, text="Drawing Tools")

        self.create_grid_controls(self.grid_tab)
        self.create_drawing_controls(self.drawing_tab)

    def create_grid_controls(self, parent_frame):
        self.create_control_frame(parent_frame)
        self.create_grid_type_frame(parent_frame)
        self.create_slider_frame(parent_frame)

    def create_drawing_controls(self, parent_frame):
        drawing_control_frame = Frame(parent_frame)
        drawing_control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        Button(drawing_control_frame, text="Clear Lines",
            command=self.callbacks['clear_lines']).pack(side=tk.LEFT, padx=5)
        Button(drawing_control_frame, text="Clear Bezier Curves",
            command=self.callbacks['clear_bezier_curves']).pack(side=tk.LEFT, padx=5)
        Button(drawing_control_frame, text="Toggle Line Edit",
            command=self.callbacks['toggle_line_edit_mode']).pack(side=tk.LEFT, padx=5)

    def create_control_frame(self, parent_frame):
        self.control_frame = Frame(parent_frame)
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        Button(self.control_frame, text="Load Image",
            command=self.callbacks['load_image']).pack(side=tk.LEFT, padx=5)
        Button(self.control_frame, text="Reset View",
            command=self.callbacks['reset_view']).pack(side=tk.LEFT, padx=5)
        Button(self.control_frame, text="Export",
            command=self.callbacks['export_image']).pack(side=tk.LEFT, padx=5)
        Button(self.control_frame, text="Grid Color",
            command=self.callbacks['choose_color']).pack(side=tk.LEFT, padx=5)

    def create_grid_type_frame(self, parent_frame):
        self.grid_type_frame = Frame(parent_frame)
        self.grid_type_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        Radiobutton(self.grid_type_frame, text="Square Grid", variable=self.grid_type, value=0,
                    command=self.callbacks['update_grid_type']).pack(side=tk.LEFT, padx=5)
        Radiobutton(self.grid_type_frame, text="Rectangular Grid", variable=self.grid_type, value=1,
                    command=self.callbacks['update_grid_type']).pack(side=tk.LEFT, padx=5)

    def create_slider_frame(self, parent_frame):
        self.slider_frame = Frame(parent_frame)
        self.slider_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.create_square_grid_controls(self.slider_frame)
        self.create_rectangular_grid_controls(self.slider_frame)
        self.create_thickness_controls(self.slider_frame)
        self.create_image_resize_controls(self.slider_frame)
        self.create_canvas_zoom_controls(self.slider_frame)

    def create_square_grid_controls(self, parent_frame):
        self.square_grid_frame = Frame(parent_frame)
        self.square_grid_frame.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        Label(self.square_grid_frame, text="Grid Size:").pack(side=tk.TOP)

        grid_control_frame = Frame(self.square_grid_frame)
        grid_control_frame.pack(side=tk.TOP, fill=tk.X)

        Button(grid_control_frame, text="-",
            command=lambda: self.callbacks['adjust_grid_size'](-1)).pack(side=tk.LEFT)
        self.grid_size_scale = Scale(grid_control_frame, from_=10, to=200, orient=tk.HORIZONTAL,
                                    length=150, command=self.callbacks['update_grid'])
        self.grid_size_scale.set(50)
        self.grid_size_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        Button(grid_control_frame, text="+",
            command=lambda: self.callbacks['adjust_grid_size'](1)).pack(side=tk.LEFT)

    def create_rectangular_grid_controls(self, parent_frame):
        self.rect_grid_frame = Frame(parent_frame)

        width_frame = Frame(self.rect_grid_frame)
        width_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        Label(width_frame, text="Grid Width:").pack(side=tk.TOP)

        width_control_frame = Frame(width_frame)
        width_control_frame.pack(side=tk.TOP, fill=tk.X)

        Button(width_control_frame, text="-",
            command=lambda: self.callbacks['adjust_grid_width'](-1)).pack(side=tk.LEFT)
        self.grid_width_scale = Scale(width_control_frame, from_=10, to=200, orient=tk.HORIZONTAL,
                                    length=150, command=self.callbacks['update_grid'])
        self.grid_width_scale.set(50)
        self.grid_width_scale.pack(
            side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        Button(width_control_frame, text="+",
            command=lambda: self.callbacks['adjust_grid_width'](1)).pack(side=tk.LEFT)

        height_frame = Frame(self.rect_grid_frame)
        height_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        Label(height_frame, text="Grid Height:").pack(side=tk.TOP)

        height_control_frame = Frame(height_frame)
        height_control_frame.pack(side=tk.TOP, fill=tk.X)

        Button(height_control_frame, text="-",
            command=lambda: self.callbacks['adjust_grid_height'](-1)).pack(side=tk.LEFT)
        self.grid_height_scale = Scale(height_control_frame, from_=10, to=200, orient=tk.HORIZONTAL,
                                    length=150, command=self.callbacks['update_grid'])
        self.grid_height_scale.set(50)
        self.grid_height_scale.pack(
            side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        Button(height_control_frame, text="+",
            command=lambda: self.callbacks['adjust_grid_height'](1)).pack(side=tk.LEFT)

    def create_thickness_controls(self, parent_frame):
        thickness_frame = Frame(parent_frame)
        thickness_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        Label(thickness_frame, text="Line Thickness:").pack(side=tk.TOP)

        thickness_control_frame = Frame(thickness_frame)
        thickness_control_frame.pack(side=tk.TOP, fill=tk.X)

        Button(thickness_control_frame, text="-",
            command=lambda: self.callbacks['adjust_thickness'](-1)).pack(side=tk.LEFT)
        self.thickness_scale = Scale(thickness_control_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                    length=150, command=self.callbacks['update_grid'])
        self.thickness_scale.set(1)
        self.thickness_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        Button(thickness_control_frame, text="+",
            command=lambda: self.callbacks['adjust_thickness'](1)).pack(side=tk.LEFT)

    def create_image_resize_controls(self, parent_frame):
        image_resize_frame = Frame(parent_frame)
        image_resize_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        Label(image_resize_frame, text="Image Resize:").pack(side=tk.TOP)

        image_resize_control_frame = Frame(image_resize_frame)
        image_resize_control_frame.pack(side=tk.TOP, fill=tk.X)

        Button(image_resize_control_frame, text="-",
            command=lambda: self.callbacks['adjust_image_resize'](-0.1)).pack(side=tk.LEFT)
        self.image_resize_scale = Scale(image_resize_control_frame, from_=0.1, to=10, resolution=0.1, orient=tk.HORIZONTAL,
                                length=150, command=self.callbacks['update_image_resize'])
        self.image_resize_scale.set(1.0)
        self.image_resize_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        Button(image_resize_control_frame, text="+",
            command=lambda: self.callbacks['adjust_image_resize'](0.1)).pack(side=tk.LEFT)

    def create_canvas_zoom_controls(self, parent_frame):
        canvas_zoom_frame = Frame(parent_frame)
        canvas_zoom_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        Label(canvas_zoom_frame, text="Canvas Zoom:").pack(side=tk.TOP)

        canvas_zoom_control_frame = Frame(canvas_zoom_frame)
        canvas_zoom_control_frame.pack(side=tk.TOP, fill=tk.X)

        Button(canvas_zoom_control_frame, text="-",
            command=lambda: self.callbacks['adjust_canvas_zoom'](-0.1)).pack(side=tk.LEFT)
        self.canvas_zoom_scale = Scale(canvas_zoom_control_frame, from_=0.1, to=10, resolution=0.1, orient=tk.HORIZONTAL,
                                length=150, command=self.callbacks['update_canvas_zoom'])
        self.canvas_zoom_scale.set(1.0)
        self.canvas_zoom_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        Button(canvas_zoom_control_frame, text="+",
            command=lambda: self.callbacks['adjust_canvas_zoom'](0.1)).pack(side=tk.LEFT)
