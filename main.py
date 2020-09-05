############### variables ###############
############### variables ###############
############### variables ###############
imagePath = "C:\\Path\\to\\input\\image\\jpeg\\png\\jpg\\maybe\\others\\accepted\\fileName.jpg" # full path to input image, \\ for delimiting directories
stlOutputPath = "C:\\Path\\to\\output\\stl\\file.stl" # # full path to output stl, \\ for delimiting directories, ensure .stl file ending

printImageWidth = 60            # mm width of the image path of lithoplane (height determined by the aspect ratio of input image)
printBorderWidth = 3            # mm width of border added beyond image part of mesh, 0 invalid

fileWidth = 1200                # width pixels of source image
fileHeight = 1600               # height pixels of srouce image
pixelsPerGrid = 10              # each cell will average thisxthis grid. Lower numbers are higher detail.

minLithoplaneThickness = 0.5    # minimum thickness in mm of lithoplane (0.5 for pla allows almost all light through)
maxLithoplaneThickness = 2.5    # maximum thickness in mm of lithoplane (2.5 seems to just block out all light)
frameThickness = 2.5            # frame can be thicker than thickest part of image, in mm
############### variables ###############
############### variables ###############
############### variables ###############

import bpy
# some maths
gridWidth = fileWidth/pixelsPerGrid
gridHeight = fileHeight/pixelsPerGrid
borderXScale = ((2*printBorderWidth)+printImageWidth)/printImageWidth
borderYScale = ((2*printBorderWidth)+(printImageWidth * fileHeight / fileWidth))/(printImageWidth * fileHeight / fileWidth)
# clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
# create grid
bpy.ops.mesh.primitive_grid_add(x_subdivisions=gridWidth,y_subdivisions=gridHeight, enter_editmode=False, location=(0,0,0))
lithoplane = bpy.data.objects['Grid']
lithoplane.name = 'lithoplane'
# set resolution of lithoplane
lithoplane.dimensions = [printImageWidth, printImageWidth * fileHeight / fileWidth, 1]
# import image
bpy.ops.object.mode_set(mode='OBJECT')
# add displace modifier
try:
    img = bpy.data.images.load(imagePath)
except:
    raise NameError("Cannot load image %s" % imagePath)
# create texture
tex = bpy.data.textures.new("litho", 'IMAGE')
tex.image = img
# apply texture as displacement
modifier = lithoplane.modifiers.new(name="Displace", type='DISPLACE')
modifier.texture = bpy.data.textures['litho']
modifier.strength = minLithoplaneThickness-maxLithoplaneThickness
bpy.ops.object.modifier_apply(apply_as='DATA',modifier='Displace')
# select border
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_non_manifold()
# unify edge of image
# flatten vertices
bpy.ops.transform.resize(value=(1, 1, 0))
# find average of edges and subteact from offset
bpy.ops.object.mode_set(mode='OBJECT')
zoffset = [v.co[2] for v in lithoplane.data.vertices if v.select][0]
bpy.ops.object.mode_set(mode='EDIT')
zmove = frameThickness-minLithoplaneThickness+((minLithoplaneThickness-maxLithoplaneThickness)/2)-zoffset
# move up 
bpy.ops.transform.translate(value=(0, 0, zmove))
# add border
bpy.ops.mesh.extrude_region_move()
bpy.ops.transform.resize(value=(borderXScale, borderYScale, 1))
# add side walls
bpy.ops.mesh.extrude_region_move()
bpy.ops.transform.translate(value=(0, 0, -frameThickness))
# close base
bpy.ops.mesh.edge_face_add()
# exit edit mode
bpy.ops.object.mode_set(mode='OBJECT')
# export mesh
bpy.ops.export_mesh.stl(filepath=stlOutputPath)