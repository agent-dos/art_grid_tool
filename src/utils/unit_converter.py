class UnitConverter:
    """Handles conversion between different units (px, cm, mm, inch) for grid sizing"""
    
    # Default DPI for conversion (dots per inch)
    DEFAULT_DPI = 96
    
    # Conversion factors to pixels
    CONVERSIONS = {
        'px': 1.0,
        'cm': DEFAULT_DPI / 2.54,  # 1 cm = 2.54 inches
        'mm': DEFAULT_DPI / 25.4,  # 1 mm = 0.1 cm  
        'inch': DEFAULT_DPI  # 1 inch = 96 pixels at default DPI
    }
    
    @classmethod
    def to_pixels(cls, value, unit):
        """Convert value from given unit to pixels"""
        if unit not in cls.CONVERSIONS:
            raise ValueError(f"Unsupported unit: {unit}")
        return value * cls.CONVERSIONS[unit]
    
    @classmethod
    def from_pixels(cls, pixels, unit):
        """Convert pixels to given unit"""
        if unit not in cls.CONVERSIONS:
            raise ValueError(f"Unsupported unit: {unit}")
        return pixels / cls.CONVERSIONS[unit]
    
    @classmethod
    def convert(cls, value, from_unit, to_unit):
        """Convert value from one unit to another"""
        pixels = cls.to_pixels(value, from_unit)
        return cls.from_pixels(pixels, to_unit)
    
    @classmethod
    def get_available_units(cls):
        """Get list of available units"""
        return list(cls.CONVERSIONS.keys())
    
    @classmethod
    def get_unit_display_name(cls, unit):
        """Get display name for unit"""
        names = {
            'px': 'Pixels',
            'cm': 'Centimeters',
            'mm': 'Millimeters',
            'inch': 'Inches'
        }
        return names.get(unit, unit)