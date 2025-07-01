import tkinter as tk
from tkinter import Frame


class ImageCanvas:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        
        self.canvas_frame = Frame(root)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.current_line = None
        self.bind_events()
    
    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.callbacks['start_drag'])
        self.canvas.bind("<B1-Motion>", self.callbacks['drag'])
        self.canvas.bind("<ButtonRelease-1>", self.callbacks['end_drag'])

    def draw_line(self, x1, y1, x2, y2, color="black", width=1):
        return self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    def delete_line(self, line_id):
        self.canvas.delete(line_id)

    def draw_bezier_curve(self, points, color="black", width=1):
        if len(points) < 2:
            return
        return self.canvas.create_line(points, smooth=True, fill=color, width=width)

    def draw_line_control_points(self, line_id):
        coords = self.canvas.coords(line_id)
        control_points = []
        for i in range(0, len(coords), 2):
            x, y = coords[i], coords[i+1]
            cp_id = self.canvas.create_rectangle(x-3, y-3, x+3, y+3, fill="blue", outline="white")
            control_points.append(cp_id)
        return control_points

    def clear_control_points(self, control_points_dict):
        for line_id, cp_ids in control_points_dict.items():
            for cp_id in cp_ids:
                self.canvas.delete(cp_id)
        control_points_dict.clear()