import string
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont


class GridRenderer:
    def __init__(self):
        pass
    

    
    def draw_grid_on_canvas(self, canvas, img_x, img_y, scaled_width, scaled_height, 
                           scaled_grid_width, scaled_grid_height, line_thickness, grid_color):
        for x in range(0, scaled_width + 1, scaled_grid_width):
            x_pos = img_x + x
            canvas.create_line(x_pos, img_y, x_pos, img_y + scaled_height,
                              width=line_thickness, fill=grid_color)
        
        for y in range(0, scaled_height + 1, scaled_grid_height):
            y_pos = img_y + y
            canvas.create_line(img_x, y_pos, img_x + scaled_width, y_pos,
                              width=line_thickness, fill=grid_color)
    
    def draw_coordinates_on_canvas(self, canvas, img_x, img_y, scaled_width, scaled_height,
                                  scaled_grid_width, scaled_grid_height):
        font_size = max(8, min(12, min(scaled_grid_width, scaled_grid_height) // 4))
        
        for x in range(0, scaled_width, scaled_grid_width):
            col_num = x // scaled_grid_width + 1
            cell_center_x = img_x + x + scaled_grid_width // 2
            canvas.create_text(cell_center_x, img_y - 15,
                              text=str(col_num), fill="blue",
                              font=("Arial", font_size))
        
        for y in range(0, scaled_height, scaled_grid_height):
            row_num = y // scaled_grid_height + 1
            cell_center_y = img_y + y + scaled_grid_height // 2
            canvas.create_text(img_x - 15, cell_center_y,
                              text=str(row_num), fill="blue",
                              font=("Arial", font_size))


class GridExporter:
    def __init__(self):
        pass
    

    
    def export_image_with_grid(self, original_image, file_path, grid_width, grid_height, 
                              line_thickness, grid_color, resize_factor):
        margin = max(30, min(grid_width, grid_height) // 2)
        
        img_width, img_height = original_image.size
        
        export_width = int(img_width * resize_factor)
        export_height = int(img_height * resize_factor)
        
        resized_image = original_image.resize((export_width, export_height), Image.LANCZOS)
        
        export_image = Image.new('RGBA', (export_width + margin * 2, export_height + margin * 2), (255, 255, 255, 255))
        export_image.paste(resized_image, (margin, margin))
        
        draw = ImageDraw.Draw(export_image)
        
        try:
            font = ImageFont.truetype("arial.ttf", max(10, min(16, min(grid_width, grid_height) // 3)))
        except IOError:
            font = ImageFont.load_default()
        
        for x in range(0, export_width + 1, grid_width):
            draw.line([(x + margin, margin), (x + margin, export_height + margin)],
                     fill=grid_color, width=line_thickness)
        
        for y in range(0, export_height + 1, grid_height):
            draw.line([(margin, y + margin), (export_width + margin, y + margin)],
                     fill=grid_color, width=line_thickness)
        
        for x in range(0, export_width, grid_width):
            col_num = x // grid_width + 1
            cell_center_x = x + margin + grid_width // 2
            
            text_width, text_height = draw.textsize(str(col_num), font=font) if hasattr(
                draw, 'textsize') else (grid_width // 3, grid_height // 3)
            
            draw.text(
                (cell_center_x - text_width // 2, margin // 2 - text_height // 2),
                str(col_num),
                fill="blue",
                font=font
            )
        
        for y in range(0, export_height, grid_height):
            row_num = str(y // grid_height + 1)
            cell_center_y = y + margin + grid_height // 2
            
            text_width, text_height = draw.textsize(row_num, font=font) if hasattr(
                draw, 'textsize') else (grid_width // 3, grid_height // 3)
            
            draw.text(
                (margin // 2 - text_width // 2, cell_center_y - text_height // 2),
                row_num,
                fill="blue",
                font=font
            )
        
        export_image.save(file_path)
        return True