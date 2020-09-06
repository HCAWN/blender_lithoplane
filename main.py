import bpy                          # bpy module (built into blender)
import json                         # json to read config variables

# import config values
with open('configuration/config.json') as configFile:
    config = json.load(configFile)
# some maths
gridWidth = config["fileWidth"]/config["pixelsPerGrid"]
gridHeight = config["fileHeight"]/config["pixelsPerGrid"]
borderXScale = ((2*config["printBorderWidth"])+config["printImageWidth"])/config["printImageWidth"]
borderYScale = ((2*config["printBorderWidth"])+(config["printImageWidth"] * config["fileHeight"] / config["fileWidth"]))/(config["printImageWidth"] * config["fileHeight"] / config["fileWidth"])
# clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
# create grid
bpy.ops.mesh.primitive_grid_add(x_subdivisions=gridWidth,y_subdivisions=gridHeight, enter_editmode=False, location=(0,0,0))
lithoplane = bpy.data.objects['Grid']
lithoplane.name = 'lithoplane'
# set resolution of lithoplane
lithoplane.dimensions = [config["printImageWidth"], config["printImageWidth"] * config["fileHeight"] / config["fileWidth"], 1]
# import image
bpy.ops.object.mode_set(mode='OBJECT')
# add displace modifier
try:
    img = bpy.data.images.load(config["imagePath"])
except:
    raise NameError("Cannot load image %s" % config["imagePath"])
# create texture
tex = bpy.data.textures.new("litho", 'IMAGE')
tex.image = img
# apply texture as displacement
modifier = lithoplane.modifiers.new(name="Displace", type='DISPLACE')
modifier.texture = bpy.data.textures['litho']
modifier.strength = config["minLithoplaneThickness"]-config["maxLithoplaneThickness"]
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
zmove = config["frameThickness"]-config["minLithoplaneThickness"]+((config["minLithoplaneThickness"]-config["maxLithoplaneThickness"])/2)-zoffset
# move up 
bpy.ops.transform.translate(value=(0, 0, zmove))
# add border
bpy.ops.mesh.extrude_region_move()
bpy.ops.transform.resize(value=(borderXScale, borderYScale, 1))
# add side walls
bpy.ops.mesh.extrude_region_move()
bpy.ops.transform.translate(value=(0, 0, -config["frameThickness"]))
# close base
bpy.ops.mesh.edge_face_add()
# exit edit mode
bpy.ops.object.mode_set(mode='OBJECT')
# export mesh
bpy.ops.export_mesh.stl(filepath=config["stlOutputPath"])
print('DONE')