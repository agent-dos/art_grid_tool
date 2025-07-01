from PIL import Image, ImageTk
import os


class ImageProcessor:
    def __init__(self):
        self.original_image = None
        self.displayed_image = None
        self.image_path = None
    
    def load_image(self, file_path):
        if not file_path:
            return False
        
        try:
            self.original_image = Image.open(file_path)
            self.image_path = file_path
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            return False
    
    def get_image_info(self):
        if self.original_image:
            return {
                'size': self.original_image.size,
                'filename': os.path.basename(self.image_path) if self.image_path else 'None'
            }
        return None
    
    def resize_image(self, resize_factor):
        if self.original_image is None:
            return None
        
        img_width, img_height = self.original_image.size
        scaled_width = int(img_width * resize_factor)
        scaled_height = int(img_height * resize_factor)
        
        resized_image = self.original_image.resize(
            (scaled_width, scaled_height), Image.LANCZOS)
        self.displayed_image = ImageTk.PhotoImage(resized_image)
        
        return self.displayed_image, scaled_width, scaled_height