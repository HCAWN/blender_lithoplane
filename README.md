# blender_lithoplane
Blender python script to generate lithoplane STL files for 3D printing 
## Requirements
1. Blender (2.79 tested, probably works on 2.8.x)
2. Blender added to PATH environment variable
## Usage
1. Clone the repo `git clone https://github.com/HCAWN/blender_lithoplane.git`
2. Open and edit the variable as the top of `main.py` inside `############### variables ###############`
3. save and close `main.py`
4. Open terminal in the root of the directory
5. run the following command `blender -b --python main.py`
6. if your variables set the resolution of the file high then it make take up to a few second depending on the speed of your machine.
## Print settings
1. Set infill to 100 percent
2. Layer height as low as possible
3. Print the file horizontal as you will never really need more than 20 levels of greyscale (range of lithoplane divided by layer height, 2mm/0.1mm layer height)
## Known issues
Non yet, please open an issue if you have questions