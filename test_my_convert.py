import trimesh
import struct
import numpy as np
from gltflib import (
    GLTF, GLTFModel, Asset, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor, AccessorType,
    BufferTarget, ComponentType, GLBResource, FileResource
)
mesh = trimesh.load_mesh('public/save_mesh.obj')

vertices = mesh.vertices
faces = mesh.faces
normals = mesh.vertex_normals

colors = mesh.visual.vertex_colors
colors = colors / 255.0

def calculate_min_max(data):
    min_val = np.min(data, axis=0).tolist()
    max_val = np.max(data, axis=0).tolist()
    return min_val, max_val

vertex_bytearray = bytearray()
for vertex in vertices:
    for value in vertex:
        vertex_bytearray.extend(struct.pack('f', value))

normal_bytearray = bytearray()
for normal in normals:
    for value in normal:
        normal_bytearray.extend(struct.pack('f', value))

color_bytearray = bytearray()
if colors is not None:
    for color in colors:
        for c in color[:4]:
            color_bytearray.extend(struct.pack('f', c))

indices_bytearray = bytearray()
for face in faces:
    for index in face:
        indices_bytearray.extend(struct.pack('I', index))

vertex_buffer = Buffer(byteLength=len(vertex_bytearray), uri="vertices.bin")
normal_buffer = Buffer(byteLength=len(normal_bytearray), uri="normals.bin")
color_buffer = Buffer(byteLength=len(color_bytearray), uri="colors.bin") if colors is not None else None
indices_buffer = Buffer(byteLength=len(indices_bytearray), uri="indices.bin")

vertex_view = BufferView(buffer=0, byteOffset=0, byteLength=len(vertex_bytearray), target=BufferTarget.ARRAY_BUFFER.value)
normal_view = BufferView(buffer=1, byteOffset=0, byteLength=len(normal_bytearray), target=BufferTarget.ARRAY_BUFFER.value)
color_view = BufferView(buffer=2, byteOffset=0, byteLength=len(color_bytearray), target=BufferTarget.ARRAY_BUFFER.value) if colors is not None else None
indices_view = BufferView(buffer=3, byteOffset=0, byteLength=len(indices_bytearray), target=BufferTarget.ELEMENT_ARRAY_BUFFER.value)

position_min, position_max = calculate_min_max(vertices)
normal_min, normal_max = calculate_min_max(normals)
color_min, color_max = calculate_min_max(colors) if colors is not None else (None, None)

position_accessor = Accessor(
    bufferView=0, componentType=ComponentType.FLOAT.value, count=len(vertices),
    type=AccessorType.VEC3.value, min=position_min, max=position_max
)

normal_accessor = Accessor(
    bufferView=1, componentType=ComponentType.FLOAT.value, count=len(normals),
    type=AccessorType.VEC3.value, min=normal_min, max=normal_max
)

color_accessor = Accessor(
    bufferView=2, componentType=ComponentType.FLOAT.value, count=len(colors),
    type=AccessorType.VEC4.value, min=color_min, max=color_max
) if colors is not None else None

indices_accessor = Accessor(
    bufferView=3, componentType=ComponentType.UNSIGNED_INT.value, count=len(faces.flatten()),
    type=AccessorType.SCALAR.value
)

primitive = Primitive(
    attributes={
        "POSITION": 0,
        "NORMAL": 1,
        "COLOR_0": 2 if colors is not None else None
    },
    indices=3,
    mode=4  # TRIANGLES
)

mesh = Mesh(primitives=[primitive])
node = Node(mesh=0)
scene = Scene(nodes=[0])

model = GLTFModel(
    asset=Asset(version='2.0'),
    scenes=[scene],
    nodes=[node],
    meshes=[mesh],
    buffers=[vertex_buffer, normal_buffer, color_buffer, indices_buffer] if colors is not None else [vertex_buffer, normal_buffer, indices_buffer],
    bufferViews=[vertex_view, normal_view, color_view, indices_view] if colors is not None else [vertex_view, normal_view, indices_view],
    accessors=[position_accessor, normal_accessor, color_accessor, indices_accessor] if colors is not None else [position_accessor, normal_accessor, indices_accessor]
)

resources = []
resources.append(FileResource('vertices.bin', data=vertex_bytearray))
resources.append(FileResource('normals.bin', data=normal_bytearray))
if colors is not None:
    resources.append(FileResource('colors.bin', data=color_bytearray))
resources.append(FileResource('indices.bin', data=indices_bytearray))

gltf = GLTF(model=model, resources=resources)
gltf.export('public/my_handcrafted_gltf/model.gltf')

print("GLTF model has been exported successfully.")