# Art Grid Generator

A Windows application that creates customizable grid overlays on images for artists and designers.

## Features

- Upload and display images
- Adjustable grid with square or rectangular cells
- Customizable grid color
- Adjustable line thickness
- Coordinates displayed along grid edges (letters for columns, numbers for rows)
- Pan and zoom functionality
- Export images with grid overlay

## Requirements

- Python 3.6+
- Tkinter (included with standard Python installation)
- PIL/Pillow (`pip install pillow`)

## Installation

1. Ensure Python is installed on your system
2. Install required dependencies: `pip install pillow`
3. Download the script
4. Run the application: `python main.py`

## Creating an Executable File

To create a standalone `.exe` file that doesn't require Python to be installed:

1. Install PyInstaller: `pip install pyinstaller`
2. Navigate to the project directory
3. Create the executable: `pyinstaller --onefile --windowed main.py`
4. The executable will be created in the `dist` folder

### Advanced PyInstaller Options

For a more optimized executable with custom icon:

```bash
pyinstaller --onefile --windowed --name "ArtGridTool" --icon=icon.ico main.py
```

- `--onefile`: Creates a single executable file
- `--windowed`: Removes the console window (GUI only)
- `--name`: Sets the executable name
- `--icon`: Adds a custom icon (optional)

## Usage

1. Click "Load Image" to select an image file
2. Use the controls to customize your grid:
  - Toggle between square or rectangular grid
  - Adjust grid size(s) with sliders or +/- buttons
  - Set line thickness
  - Change grid color
3. Pan by clicking and dragging the image
4. Zoom with mouse wheel or zoom slider
5. Click "Export" to save the image with grid overlay

## Controls

- **Load Image**: Open an image file
- **Reset View**: Return to default zoom and position
- **Export**: Save image with grid overlay
- **Grid Color**: Change the color of grid lines
- **Square/Rectangular Grid**: Toggle between equal or custom cell dimensions
- **Grid Size/Width/Height**: Adjust cell dimensions
- **Line Thickness**: Adjust grid line width
- **Zoom**: Scale the image and grid

## Tips

- Use rectangular grid for specialized drawing references
- Change grid color if it's difficult to see against your image
- Exported images include coordinate labels for reference
- Use +/- buttons for fine-tuning grid dimensions

## License

Free to use and modify for personal and commercial projects.