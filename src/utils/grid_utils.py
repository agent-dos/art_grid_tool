import string
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont


class GridRenderer:
    def __init__(self):
        pass
    

    
    def draw_grid_on_canvas(self, canvas, img_x, img_y, scaled_width, scaled_height, 
                           scaled_grid_width, scaled_grid_height, line_thickness, grid_color, canvas_zoom_factor):
        # Ensure line thickness remains constant in pixels regardless of zoom
        pixel_line_thickness = max(1, int(line_thickness))
        
        # Draw vertical lines - snap to integer pixels to avoid anti-aliasing
        for x_unzoomed in range(0, scaled_width + 1, scaled_grid_width):
            x_pos = int(img_x + (x_unzoomed * canvas_zoom_factor))
            y_start = int(img_y)
            y_end = int(img_y + (scaled_height * canvas_zoom_factor))
            canvas.create_line(x_pos, y_start, x_pos, y_end,
                              width=pixel_line_thickness, fill=grid_color, tags="grid_tag")

        # Draw horizontal lines - snap to integer pixels to avoid anti-aliasing
        for y_unzoomed in range(0, scaled_height + 1, scaled_grid_height):
            y_pos = int(img_y + (y_unzoomed * canvas_zoom_factor))
            x_start = int(img_x)
            x_end = int(img_x + (scaled_width * canvas_zoom_factor))
            canvas.create_line(x_start, y_pos, x_end, y_pos,
                              width=pixel_line_thickness, fill=grid_color, tags="grid_tag")
    
    def draw_coordinates_on_canvas(self, canvas, img_x, img_y, scaled_width, scaled_height,
                                  scaled_grid_width, scaled_grid_height, canvas_zoom_factor):
        font_size = max(8, min(12, min(scaled_grid_width, scaled_grid_height) // 4))

        # Draw column numbers - snap to integer pixels to avoid anti-aliasing
        for x_unzoomed in range(0, scaled_width, scaled_grid_width):
            col_num = x_unzoomed // scaled_grid_width + 1
            cell_center_x = int(img_x + (x_unzoomed + scaled_grid_width // 2) * canvas_zoom_factor)
            canvas.create_text(cell_center_x, int(img_y - 15), # -15 offset for text position
                              text=str(col_num), fill="blue",
                              font=("Arial", font_size), tags="coordinate_tag")

        # Draw row numbers - snap to integer pixels to avoid anti-aliasing
        for y_unzoomed in range(0, scaled_height, scaled_grid_height):
            row_num = y_unzoomed // scaled_grid_height + 1
            cell_center_y = int(img_y + (y_unzoomed + scaled_grid_height // 2) * canvas_zoom_factor)
            canvas.create_text(int(img_x - 15), cell_center_y, # -15 offset for text position
                              text=str(row_num), fill="blue",
                              font=("Arial", font_size), tags="coordinate_tag")


class GridExporter:
    def __init__(self):
        pass
    

    
    def export_image_with_grid(self, original_image, file_path, grid_width, grid_height, 
                              line_thickness, grid_color, resize_factor, dpi=96):
        img_width, img_height = original_image.size
        
        export_width = int(img_width * resize_factor)
        export_height = int(img_height * resize_factor)
        
        # Grid dimensions should remain constant in actual units
        scaled_grid_width = grid_width
        scaled_grid_height = grid_height
        # Ensure line thickness is integer pixels
        scaled_line_thickness = max(1, int(line_thickness))
        
        # Calculate number of cells to determine margin requirements
        num_cols = export_width // scaled_grid_width
        num_rows = export_height // scaled_grid_height
        
        try:
            # Scale font size based on grid dimensions and zoom factor
            font_size = max(10, min(16, min(scaled_grid_width, scaled_grid_height) // 3))
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # Calculate required margins based on actual text dimensions
        draw_temp = ImageDraw.Draw(Image.new('RGB', (100, 100)))
        
        # Test longest column number (highest number)
        max_col_text = str(num_cols)
        col_text_width, col_text_height = draw_temp.textsize(max_col_text, font=font) if hasattr(
            draw_temp, 'textsize') else (len(max_col_text) * font_size // 2, font_size)
        
        # Test longest row number
        max_row_text = str(num_rows)
        row_text_width, row_text_height = draw_temp.textsize(max_row_text, font=font) if hasattr(
            draw_temp, 'textsize') else (len(max_row_text) * font_size // 2, font_size)
        
        # Calculate margins with padding
        top_margin = col_text_height + 10  # 10px padding
        left_margin = row_text_width + 10  # 10px padding
        
        # Use LANCZOS for consistent scaling with canvas display
        resized_image = original_image.resize((export_width, export_height), Image.LANCZOS)
        
        export_image = Image.new('RGBA', (export_width + left_margin + 10, export_height + top_margin + 10), (255, 255, 255, 255))
        export_image.paste(resized_image, (left_margin, top_margin))
        
        draw = ImageDraw.Draw(export_image)
        
        # Draw vertical grid lines (crisp, pixel-aligned)
        for x in range(0, export_width + 1, scaled_grid_width):
            x_pos = int(x + left_margin)
            draw.line([(x_pos, int(top_margin)), (x_pos, int(export_height + top_margin))],
                     fill=grid_color, width=scaled_line_thickness)
        
        # Draw horizontal grid lines (crisp, pixel-aligned)
        for y in range(0, export_height + 1, scaled_grid_height):
            y_pos = int(y + top_margin)
            draw.line([(int(left_margin), y_pos), (int(export_width + left_margin), y_pos)],
                     fill=grid_color, width=scaled_line_thickness)
        
        # Draw column numbers using scaled grid dimensions - snap to integer pixels
        for x in range(0, export_width, scaled_grid_width):
            col_num = x // scaled_grid_width + 1
            cell_center_x = int(x + left_margin + scaled_grid_width // 2)
            
            text_width, text_height = draw.textsize(str(col_num), font=font) if hasattr(
                draw, 'textsize') else (len(str(col_num)) * font_size // 2, font_size)
            
            # Position column numbers above the grid - snap to integer pixels
            draw.text(
                (int(cell_center_x - text_width // 2), int(top_margin // 2 - text_height // 2)),
                str(col_num),
                fill="blue",
                font=font
            )
        
        # Draw row numbers using scaled grid dimensions - snap to integer pixels
        for y in range(0, export_height, scaled_grid_height):
            row_num = str(y // scaled_grid_height + 1)
            cell_center_y = int(y + top_margin + scaled_grid_height // 2)
            
            text_width, text_height = draw.textsize(row_num, font=font) if hasattr(
                draw, 'textsize') else (len(row_num) * font_size // 2, font_size)
            
            # Position row numbers to the left of the grid - snap to integer pixels
            draw.text(
                (int(left_margin // 2 - text_width // 2), int(cell_center_y - text_height // 2)),
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