# obj2gltf

Convert the **obj with vertex color** to gltf

For `.obj` with vertex color, many apps can not preview the "unofficial" obj directly or convert to other 3D format with color.(For example, Blender, Spline, MeshLab).
Scripts and online tools also can not deal with objs with vertex color (Including [CesiumGS/obj2gltf](https://github.com/CesiumGS/obj2gltf), the [issue](https://github.com/CesiumGS/obj2gltf/issues/102) haven't been solved yet)

The script is based on [trimesh](https://github.com/mikedh/trimesh/tree/main), [gltflib](https://github.com/lukas-shawford/gltflib) APIs.
