# Mesh

Meshes are collections of verticies, edges, and faces in 3D space.
In `templux`, meshes are represented as a collection of faces only.
Each face contains a list of `(x, y, z)` vertex locations.

## templux.Mesh

Initialize a mesh with a list of faces:

``` python
import templux

my_mesh = templux.Mesh(
    templux.Face(((0, 0, 0), (0, 0, 1), (0, 1, 0))),
    templux.Face(((1, 0, 0), (1, 0, 1), (1, 1, 0))),
)
```

It can be hard manually typing in locations, so `templux` contains STL parsing algorithms.

STL files are representations of a triangulated 3D mesh.

To initialize a mesh with an STL file, use the classmethods `from_stl_ascii`, and `from_stl_bin`.
Your STL file will most likely be a binary file, so you should use `from_stl_bin`.
If that doesn't work, try `from_stl_ascii` instead.

``` python
import templux

my_mesh = templux.Mesh.from_stl_ascii("path/to/file.stl")
my_mesh2 = templux.Mesh.from_stl_bin("path/to/binfile.stl")
```


[Back to documentation home][dochome]

[dochome]: https://medilocus.github.io/templux/
