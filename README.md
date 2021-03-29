# MeshSlicer
Blender Add-On for slicing meshes with multiple overlapping planes at once. 

![cubeSlice](https://user-images.githubusercontent.com/52789554/112713791-7415de80-8f09-11eb-885c-58abb62bf2bc.gif)

![sliceSphere](https://user-images.githubusercontent.com/52789554/112713793-7841fc00-8f09-11eb-8b9a-6991308d52ef.gif)

This is a simple Blender addon to slice a silmple mesh
with multiple planes at once. Unlike other existing add-ons, this tool performs correct slicing while the plances are intersecting with each other. This has similar slicing functionality to 3D Max's Pro Cutter. 



**Perform Slicing**
Select at least two meshes and press the Slice button. 
The last selected object will be sliced, while all previous ones will be used as planes to cut it with. 
The Slice button will display the name of the object that will be sliced. 

Options:

_Delete chunks_ - the algorithm is cloning the objects during the process. If Selected, this partial results will be deleted. This should be selected for most cases.

_Keep original_ - retains the original object that was sliced in the scene. If Selected the object will be kept bud hidden in the hierarchy, otherwise it will be deleted.

_Reset origins_ - if selected, result meshes will get the origin set to their center. Otherwise they will have the same origin as source mesh to slice. 

_What to do with slicers_ - decides what happen to slicing planes after the operation is completed. Keep, Hide and Delete options are available. 

**Create Slicers:**
Allows to create 1,2 or 3 perpendicular plane templates at world (0,0,0) position, they can be quickly used to slice an object. This step is not required to perform the slicing, you are free to generate the planes any other way. 

_Size of slicers_ - size of Blender units of generated slicers. 

**How to use:**
1) Clone or Download the MeshSlicer.py file.
2) In Blender go to Edit>Preferences>Add-ons install and point to the file.
3) Enable the toggle in top left corner. 
4) Mesh Slicer panel will appear avaialble in 3D view - Tools panel.

**Notes:**
- Created and tested with Blender 2.92
- **This version will only work for objects linked to default scene collection (named "Collection")**
- You need to be in object mode for this tool to work. 
- While the material and other data will be transferred from the the source object to results of slicing, the uvs will not. This is a limitation of build int Blender Boolean modifier, after applying it the uvs get reset. 
- This tool uses recursion-like algorithm, execution time increases exponentially with the count of slicing objects. In other words it gets quite slow with plenty of slicers. 
- This tool executes build in Blender Boolean modifier, for some complex meshes the Boolean result might be broken, and so will be the result of this tool.
- This tool is designed to sliced with planes, you can use different shape as source which will probably work, but those object will be treated as planes located at the object origin, and oriented towards its up vector. Slicing with complex shapes won't work.
- This plugin was created for one of personal projects, it was not fully tested and thus might contain bugs and not be production ready. 
- Any feedback regarding the plugin features/bugs as well as Python will be greatly appreciated. Please also report any missing functionality. 

![suzanneSlice](https://user-images.githubusercontent.com/52789554/112714778-a1b15680-8f0e-11eb-925f-81194d238bc0.gif)
