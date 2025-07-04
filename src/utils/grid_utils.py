import string
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont


class GridRenderer:
    def __init__(self):
        pass
    

    
    def draw_grid_on_canvas(self, canvas, img_x, img_y, scaled_width, scaled_height, 
                           scaled_grid_width, scaled_grid_height, line_thickness, grid_color, canvas_zoom_factor):
        # Draw vertical lines
        for x_unzoomed in range(0, scaled_width + 1, scaled_grid_width):
            x_pos = img_x + (x_unzoomed * canvas_zoom_factor)
            y_start = img_y
            y_end = img_y + (scaled_height * canvas_zoom_factor)
            canvas.create_line(x_pos, y_start, x_pos, y_end,
                              width=line_thickness, fill=grid_color, tags="grid_tag")

        # Draw horizontal lines
        for y_unzoomed in range(0, scaled_height + 1, scaled_grid_height):
            y_pos = img_y + (y_unzoomed * canvas_zoom_factor)
            x_start = img_x
            x_end = img_x + (scaled_width * canvas_zoom_factor)
            canvas.create_line(x_start, y_pos, x_end, y_pos,
                              width=line_thickness, fill=grid_color, tags="grid_tag")
    
    def draw_coordinates_on_canvas(self, canvas, img_x, img_y, scaled_width, scaled_height,
                                  scaled_grid_width, scaled_grid_height, canvas_zoom_factor):
        font_size = max(8, min(12, min(scaled_grid_width, scaled_grid_height) // 4))

        # Draw column numbers
        for x_unzoomed in range(0, scaled_width, scaled_grid_width):
            col_num = x_unzoomed // scaled_grid_width + 1
            cell_center_x = img_x + (x_unzoomed + scaled_grid_width // 2) * canvas_zoom_factor
            canvas.create_text(cell_center_x, img_y - 15, # -15 offset for text position
                              text=str(col_num), fill="blue",
                              font=("Arial", font_size), tags="coordinate_tag")

        # Draw row numbers
        for y_unzoomed in range(0, scaled_height, scaled_grid_height):
            row_num = y_unzoomed // scaled_grid_height + 1
            cell_center_y = img_y + (y_unzoomed + scaled_grid_height // 2) * canvas_zoom_factor
            canvas.create_text(img_x - 15, cell_center_y, # -15 offset for text position
                              text=str(row_num), fill="blue",
                              font=("Arial", font_size), tags="coordinate_tag")


class GridExporter:
    def __init__(self):
        pass
    

    
    def export_image_with_grid(self, original_image, file_path, grid_width, grid_height, 
                              line_thickness, grid_color, resize_factor, dpi=96):
        margin = max(30, min(grid_width, grid_height) // 2)
        
        img_width, img_height = original_image.size
        
        export_width = int(img_width * resize_factor)
        export_height = int(img_height * resize_factor)
        
        # Use NEAREST neighbor for crisp pixel-perfect scaling
        resized_image = original_image.resize((export_width, export_height), Image.NEAREST)
        
        export_image = Image.new('RGBA', (export_width + margin * 2, export_height + margin * 2), (255, 255, 255, 255))
        export_image.paste(resized_image, (margin, margin))
        
        draw = ImageDraw.Draw(export_image)
        
        # Scale grid dimensions by resize factor for crisp rendering
        scaled_grid_width = int(grid_width * resize_factor)
        scaled_grid_height = int(grid_height * resize_factor)
        scaled_line_thickness = max(1, int(line_thickness * resize_factor))
        
        try:
            # Scale font size based on grid dimensions and zoom factor
            font_size = max(10, min(16, min(scaled_grid_width, scaled_grid_height) // 3))
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # Draw vertical grid lines (crisp, pixel-aligned)
        for x in range(0, export_width + 1, scaled_grid_width):
            x_pos = x + margin
            draw.line([(x_pos, margin), (x_pos, export_height + margin)],
                     fill=grid_color, width=scaled_line_thickness)
        
        # Draw horizontal grid lines (crisp, pixel-aligned)
        for y in range(0, export_height + 1, scaled_grid_height):
            y_pos = y + margin
            draw.line([(margin, y_pos), (export_width + margin, y_pos)],
                     fill=grid_color, width=scaled_line_thickness)
        
        # Draw column numbers using scaled grid dimensions
        for x in range(0, export_width, scaled_grid_width):
            col_num = x // scaled_grid_width + 1
            cell_center_x = x + margin + scaled_grid_width // 2
            
            text_width, text_height = draw.textsize(str(col_num), font=font) if hasattr(
                draw, 'textsize') else (scaled_grid_width // 3, scaled_grid_height // 3)
            
            draw.text(
                (cell_center_x - text_width // 2, margin // 2 - text_height // 2),
                str(col_num),
                fill="blue",
                font=font
            )
        
        # Draw row numbers using scaled grid dimensions
        for y in range(0, export_height, scaled_grid_height):
            row_num = str(y // scaled_grid_height + 1)
            cell_center_y = y + margin + scaled_grid_height // 2
            
            text_width, text_height = draw.textsize(row_num, font=font) if hasattr(
                draw, 'textsize') else (scaled_grid_width // 3, scaled_grid_height // 3)
            
            draw.text(
                (margin // 2 - text_width // 2, cell_center_y - text_height // 2),
                row_num,
                fill="blue",
                font=font
            )
        
        # Save with correct DPI for accurate measurements
        try:
            export_image.save(file_path, dpi=(dpi, dpi))
        except Exception as e:
            # Fallback: save without DPI if there's an error
            export_image.save(file_path)
        return True