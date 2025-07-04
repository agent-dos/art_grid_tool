import tkinter as tk
from tkinter import Scale, Label, Button, Frame, Radiobutton, IntVar, StringVar, Entry
from tkinter.ttk import Combobox


class ControlPanels:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.grid_unit = StringVar(value='px')
        
        # Image resize controls
        self.resize_enabled = IntVar(value=0)
        self.resize_dimension = StringVar(value='width')  # 'width' or 'height'
        self.resize_value = StringVar(value='10.0')
        self.resize_unit = StringVar(value='cm')

        self.create_grid_controls(root)

    def create_grid_controls(self, parent_frame):
        self.create_control_frame(parent_frame)
        self.create_image_resize_frame(parent_frame)
        self.create_slider_frame(parent_frame)

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

    def create_image_resize_frame(self, parent_frame):
        self.image_resize_frame = Frame(parent_frame)
        self.image_resize_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Checkbox to enable image resizing
        self.resize_checkbox = tk.Checkbutton(self.image_resize_frame, text="Resize Image to:", 
                                            variable=self.resize_enabled,
                                            command=self.callbacks['update_grid'])
        self.resize_checkbox.pack(side=tk.LEFT, padx=5)

        # Dimension selector (Width/Height)
        self.dimension_combo = Combobox(self.image_resize_frame, textvariable=self.resize_dimension,
                                       values=['width', 'height'], state='readonly', width=8)
        self.dimension_combo.pack(side=tk.LEFT, padx=5)
        self.dimension_combo.bind('<<ComboboxSelected>>', self.callbacks['update_grid'])

        # Size input
        self.resize_entry = Entry(self.image_resize_frame, textvariable=self.resize_value, width=8)
        self.resize_entry.pack(side=tk.LEFT, padx=5)
        self.resize_entry.bind('<Return>', self.callbacks['update_grid'])
        self.resize_entry.bind('<FocusOut>', self.callbacks['update_grid'])

        # Unit selector
        self.resize_unit_combo = Combobox(self.image_resize_frame, textvariable=self.resize_unit,
                                         values=['px', 'cm', 'mm', 'inch'], state='readonly', width=6)
        self.resize_unit_combo.pack(side=tk.LEFT, padx=5)
        self.resize_unit_combo.bind('<<ComboboxSelected>>', self.callbacks['update_grid'])



    def create_slider_frame(self, parent_frame):
        self.slider_frame = Frame(parent_frame)
        self.slider_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.create_square_grid_controls(self.slider_frame)
        self.create_thickness_controls(self.slider_frame)
        self.create_canvas_zoom_controls(self.slider_frame)

    def create_square_grid_controls(self, parent_frame):
        self.square_grid_frame = Frame(parent_frame)
        self.square_grid_frame.pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        Label(self.square_grid_frame, text="Grid Size:").pack(side=tk.TOP)

        # Unit selection
        unit_frame = Frame(self.square_grid_frame)
        unit_frame.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        Label(unit_frame, text="Unit:").pack(side=tk.LEFT)
        self.unit_combo = Combobox(unit_frame, textvariable=self.grid_unit, 
                                  values=['px', 'cm', 'mm', 'inch'], 
                                  state='readonly', width=8)
        self.unit_combo.pack(side=tk.LEFT, padx=5)
        self.unit_combo.bind('<<ComboboxSelected>>', self.callbacks['update_grid'])

        grid_control_frame = Frame(self.square_grid_frame)
        grid_control_frame.pack(side=tk.TOP, fill=tk.X)

        Button(grid_control_frame, text="-",
            command=lambda: self.callbacks['adjust_grid_size'](-1)).pack(side=tk.LEFT)
        self.grid_size_scale = Scale(grid_control_frame, from_=0.1, to=50, orient=tk.HORIZONTAL,
                                    length=150, command=self.callbacks['update_grid'], resolution=0.1)
        self.grid_size_scale.set(1.0)
        self.grid_size_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        Button(grid_control_frame, text="+",
            command=lambda: self.callbacks['adjust_grid_size'](1)).pack(side=tk.LEFT)


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
