import tkinter as tk
from tkinter import Scale, Label, Button, Frame, Radiobutton, IntVar, StringVar, Entry
from tkinter.ttk import Combobox


class ControlPanels:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.grid_type = IntVar(value=0)
        self.grid_unit = StringVar(value='px')
        self.cell_count_mode = IntVar(value=0)  # 0 = manual size, 1 = cell count, 2 = fixed cell size
        self.target_cells = StringVar(value='20')
        self.fixed_cell_size = StringVar(value='1.0')
        self.fixed_cell_unit = StringVar(value='cm')

        self.create_grid_controls(root)

    def create_grid_controls(self, parent_frame):
        self.create_control_frame(parent_frame)
        self.create_grid_type_frame(parent_frame)
        self.create_cell_count_frame(parent_frame)
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

    def create_grid_type_frame(self, parent_frame):
        self.grid_type_frame = Frame(parent_frame)
        self.grid_type_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        Radiobutton(self.grid_type_frame, text="Square Grid", variable=self.grid_type, value=0,
                    command=self.callbacks['update_grid_type']).pack(side=tk.LEFT, padx=5)
        Radiobutton(self.grid_type_frame, text="Rectangular Grid", variable=self.grid_type, value=1,
                    command=self.callbacks['update_grid_type']).pack(side=tk.LEFT, padx=5)

    def create_cell_count_frame(self, parent_frame):
        self.cell_count_frame = Frame(parent_frame)
        self.cell_count_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # First row: Radio buttons
        radio_frame = Frame(self.cell_count_frame)
        radio_frame.pack(side=tk.TOP, fill=tk.X)
        
        Radiobutton(radio_frame, text="Manual Size", variable=self.cell_count_mode, value=0,
                    command=self.callbacks['update_grid_mode']).pack(side=tk.LEFT, padx=5)
        Radiobutton(radio_frame, text="Cell Count", variable=self.cell_count_mode, value=1,
                    command=self.callbacks['update_grid_mode']).pack(side=tk.LEFT, padx=5)
        Radiobutton(radio_frame, text="Fixed Cell Size", variable=self.cell_count_mode, value=2,
                    command=self.callbacks['update_grid_mode']).pack(side=tk.LEFT, padx=5)
        
        # Second row: Controls
        controls_frame = Frame(self.cell_count_frame)
        controls_frame.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        # Cell count controls
        Label(controls_frame, text="Target Cells:").pack(side=tk.LEFT, padx=5)
        self.cell_count_entry = Entry(controls_frame, textvariable=self.target_cells, width=8)
        self.cell_count_entry.pack(side=tk.LEFT, padx=5)
        self.cell_count_entry.bind('<Return>', self.callbacks['update_grid'])
        self.cell_count_entry.bind('<FocusOut>', self.callbacks['update_grid'])
        
        # Fixed cell size controls
        Label(controls_frame, text="Cell Size:").pack(side=tk.LEFT, padx=(20, 5))
        self.fixed_cell_entry = Entry(controls_frame, textvariable=self.fixed_cell_size, width=8)
        self.fixed_cell_entry.pack(side=tk.LEFT, padx=5)
        self.fixed_cell_entry.bind('<Return>', self.callbacks['update_grid'])
        self.fixed_cell_entry.bind('<FocusOut>', self.callbacks['update_grid'])
        
        self.fixed_unit_combo = Combobox(controls_frame, textvariable=self.fixed_cell_unit, 
                                        values=['px', 'cm', 'mm', 'inch'], 
                                        state='readonly', width=6)
        self.fixed_unit_combo.pack(side=tk.LEFT, padx=5)
        self.fixed_unit_combo.bind('<<ComboboxSelected>>', self.callbacks['update_grid'])

    def create_slider_frame(self, parent_frame):
        self.slider_frame = Frame(parent_frame)
        self.slider_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.create_square_grid_controls(self.slider_frame)
        self.create_rectangular_grid_controls(self.slider_frame)
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

    def create_rectangular_grid_controls(self, parent_frame):
        self.rect_grid_frame = Frame(parent_frame)

        # Unit selection for rectangular grid
        unit_frame_rect = Frame(self.rect_grid_frame)
        unit_frame_rect.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        Label(unit_frame_rect, text="Unit:").pack(side=tk.LEFT)
        self.unit_combo_rect = Combobox(unit_frame_rect, textvariable=self.grid_unit, 
                                       values=['px', 'cm', 'mm', 'inch'], 
                                       state='readonly', width=8)
        self.unit_combo_rect.pack(side=tk.LEFT, padx=5)
        self.unit_combo_rect.bind('<<ComboboxSelected>>', self.callbacks['update_grid'])

        width_frame = Frame(self.rect_grid_frame)
        width_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        Label(width_frame, text="Grid Width:").pack(side=tk.TOP)

        width_control_frame = Frame(width_frame)
        width_control_frame.pack(side=tk.TOP, fill=tk.X)

        Button(width_control_frame, text="-",
            command=lambda: self.callbacks['adjust_grid_width'](-1)).pack(side=tk.LEFT)
        self.grid_width_scale = Scale(width_control_frame, from_=0.1, to=50, orient=tk.HORIZONTAL,
                                    length=150, command=self.callbacks['update_grid'], resolution=0.1)
        self.grid_width_scale.set(1.0)
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
        self.grid_height_scale = Scale(height_control_frame, from_=0.1, to=50, orient=tk.HORIZONTAL,
                                    length=150, command=self.callbacks['update_grid'], resolution=0.1)
        self.grid_height_scale.set(1.0)
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
