# blender_lithoplane
Blender python script to automatically generate lithoplane STL files for 3D Printing.
Tested on Creatlity Ender 3 printer in PLA 
## Requirements
1. Blender (2.79 tested, probably works on 2.8.x)
2. Blender added to PATH environment variable
3. Probably only works on Windows, you're welcome to try other OS' let me know if it fails

## Usage
1. Clone the repo `git clone https://github.com/HCAWN/blender_lithoplane.git`
2. Duplicate `configuration/config-template.json` and rename it to `configuration/config.json`
3. Edit the variable of your newely created `configuration/config.json` file, see Variables section below
4. Open terminal in the root of the directory
5. Run the following command `blender -b --python main.py` OR open `_EXECUTE_FUNCTION.bat`
6. If your variables set the resolution of the file high then it may take up to a few second depending on the speed of your machine.

## DEMO + EXTRA
- Open `interactive.blend` (in Blender) to have a more interactive version of the script
- The demo file is very low resolution to reduce the size for git. re-run it while changing `pixelsPerGrid` from `20` to `2`
- Run the script in Blender (button at the bottom, or press `ALT + p`)

## Variables
| Variable | Example | Description |
| --- | ---: | --- |
| imagePath | "C:\\Path\\to\\input\\image\\fileName.jpg" | full path to input image, \\ for delimiting directories, jpg, jpeg, png |
| stlOutputPath | "C:\\Path\\to\\output\\stl\\fileName.stl" | full path to output stl, \\ for delimiting directories, ensure .stl file ending |
| printImageWidth | 60 | mm width of the image path of lithoplane (height determined by the aspect ratio of input image) |
| printBorderWidth | 3 | mm width of border added beyond image part of mesh, 0 invalid |
| fileWidth | 1200 | width in pixels of source image |
| fileHeight | 1600 | height in pixels of source image |
| pixelsPerGrid | 10 | each cell will average thisxthis grid. Lower numbers are higher detail. |
| minLithoplaneThickness | 0.5 | minimum thickness in mm of lithoplane (0.5 for pla allows almost all light through) |
| maxLithoplaneThickness | 2.5 | maximum thickness in mm of lithoplane (2.5 seems to just block out all light) |
| frameThickness | 2.5 | frame can be thicker than thickest part of image, in mm |

## Print settings
1. Set infill to 100 percent
2. Layer height as low as possible
3. Print the file horizontal as you will never really need more than 20 levels of greyscale (range of lithoplane divided by layer height, 2mm/0.1mm layer height)

## Known issues
Non yet, please open an issue if you have questions