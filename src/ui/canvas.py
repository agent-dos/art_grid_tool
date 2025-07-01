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
        
        self.bind_events()
    
    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.callbacks['start_drag'])
        self.canvas.bind("<B1-Motion>", self.callbacks['drag'])
        self.canvas.bind("<ButtonRelease-1>", self.callbacks['end_drag'])
        self.canvas.bind("<MouseWheel>", self.callbacks['mouse_resize'])
        self.canvas.bind("<Button-4>", self.callbacks['mouse_resize'])
        self.canvas.bind("<Button-5>", self.callbacks['mouse_resize'])