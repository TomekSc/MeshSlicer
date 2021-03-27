import bpy
import math
bl_info = {
    "name": "Mesh Slicer",
    "author": "Tomasz Schelenz",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tools panel 'T' > Mesh Slicer",
    "description": "Slice a mesh with multiple planes at once. Planes can intersect with each other. Will not work correctly with other types of meshes as slicers",
    "warning": "",
    "wiki_url": "",
    "category": "",
    }
class SlicerContainer:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

class My_settings(bpy.types.PropertyGroup):

    bool_deleteChunks: bpy.props.BoolProperty(
        name='Delete chunks',
        description="Deletes the partial results after completed. This almost always should be TRUE",
        default=True,
        options={'HIDDEN'}
    )
    bool_keepOriginal: bpy.props.BoolProperty(
        name='Keep original',
        description="Keeps the original object that is being sliced in the scene, but hides it. False - it will be deleted",
        default=False,
        options={'HIDDEN'}
    )
    bool_resetOrigin: bpy.props.BoolProperty(
        name='Reset origins',
        description="If TRUE, each indivudual result of slice operation will have origin set to center of its bounds",
        default=True,
        options={'HIDDEN'}
    )       
    slicersAction : bpy.props.EnumProperty(
        name="Slicing objects action",
        description="Slicing objects will be",
        items = [('Delete','Delete','Deletes the objects used for slicing','',0), 
             ('Hide','Hide','Hides the objects used for slicing','',1),
             ('Keep','Keep','Keeps the objects used for slicing','',2)]
    )
     
    slicerSize: bpy.props.FloatProperty(
        name="Size of slicers",
        options= {'HIDDEN'},
        description="Size of the generated slicing planes",
        default = 4
    )
        
class GENERATE_SLICERS_OT(bpy.types.Operator):
    bl_idname = 'generate.operator'
    bl_label = 'Generate slicers'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = 'Generate slicing planes'
    variant: bpy.props.IntProperty(name="Generation variant",options={'HIDDEN'})
    slicerContainers = []
        
    def execute(self, context):
        slicers = []
        slicerSize = context.scene.my_tool.slicerSize
        bpy.ops.object.select_all(action='DESELECT')
        if(self.variant == 0):
            bpy.ops.mesh.primitive_plane_add(size=1)
            ob = bpy.context.active_object 
            ob.scale = (slicerSize,slicerSize,slicerSize)
            ob.name = "Slicer"  
            slicers.append(ob)

        if(self.variant == 1):
            bpy.ops.mesh.primitive_plane_add(size=1)
            ob = bpy.context.active_object
            ob.scale = (slicerSize,slicerSize,slicerSize)
            ob.name = "Slicer"  
            slicers.append(ob)
          
            bpy.ops.mesh.primitive_plane_add(size=1)
            ob = bpy.context.active_object
            ob.scale = (slicerSize,slicerSize,slicerSize)  
            ob.name = "Slicer"  
            slicers.append(ob)
            ob.rotation_euler[1] = math.radians(90)
        
        if(self.variant == 2):
            bpy.ops.mesh.primitive_plane_add(size=1)
            ob = bpy.context.active_object
            ob.scale = (slicerSize,slicerSize,slicerSize)  
            ob.name = "Slicer"  
            slicers.append(ob)
            
            bpy.ops.mesh.primitive_plane_add(size=1)
            ob = bpy.context.active_object
            ob.scale = (slicerSize,slicerSize,slicerSize)  
            ob.name = "Slicer"  
            slicers.append(ob)
            ob.rotation_euler[1] = math.radians(90)
            
            bpy.ops.mesh.primitive_plane_add(size=1)
            ob = bpy.context.active_object
            ob.scale = (slicerSize,slicerSize,slicerSize)  
            ob.name = "Slicer"  
            slicers.append(ob)
            ob.rotation_euler[0] = math.radians(90)
           
        for obj in slicers:
            obj.select_set(True)
        return {'FINISHED'}

class SLICE_OT(bpy.types.Operator):
    bl_idname = "slice.operator"
    bl_label = "Slice"
    bl_options = {"REGISTER", "UNDO"}
    bl_description = 'Slice selected object'
    slicerContainers = []
    
    #GENERETES TEMPORAL OBJECTS USED FOR BOOL OPERATION
    def makeSlicers(self, size, srcObject):
        
        #CREATE ACTUAL OBJECTS THAT WILL BE USED FOR BOOL OPERANDS ON BOTH SIDES OF THE PLANE 
        #LEFT 
        container = SlicerContainer()
        bpy.ops.mesh.primitive_cube_add(size=1, location= srcObject.location)
        ob = bpy.context.active_object 
        ob.parent = srcObject
        ob.location = (0,0,0.5)
        container.left = ob;
        #RIGHT
        bpy.ops.mesh.primitive_cube_add(size=1, location= srcObject.location)
        ob = bpy.context.active_object 
        ob.parent = srcObject
        ob.location = (0,0,-0.5)
        container.right = ob;
        self.slicerContainers.append(container)
    
    #CLONES SOURCE OBJECT 
    def cloneObject(self, objectToClone):
        
        ob = objectToClone.copy()
        ob.data = objectToClone.data.copy()
        bpy.data.collections["Collection"].objects.link(ob)
        bpy.ops.object.select_all(action='DESELECT')
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        
        ob.name = "Clone"
        return ob
    
    #PERFORMS THE BOOL OPERATION
    def doBool(self, src, object, operation):
        
        boolmod = src.modifiers.new("Bool", 'BOOLEAN')
        boolmod.object = object
        boolmod.solver = 'EXACT'
        boolmod.operation = operation
        bpy.ops.object.modifier_apply(modifier='Bool')
    
    #BUTTON CALLBACK 
    def execute(self, context):
        
        self.slicerContainers.clear()
  
        selectedObjects = bpy.context.selected_objects
        
        if(len(selectedObjects) < 2):
             self.report({"ERROR"}, "You need to select at least two objects!")
             return {"CANCELLED"}
        
        activeObjects = []
        objectsToRemove = []
        activeObjects.append(bpy.context.active_object)
        
        #REMOVE ACTIVE FROM SLICERS
        selectedObjects.remove(activeObjects[0])
        
        #CREATE THE DUMMY OBJECTS TO USE FOR BOOL
        for src in selectedObjects:
            self.makeSlicers(context.scene.my_tool.slicerSize, src)
        
        loopCount = len(selectedObjects)-1
        

        #MAIN LOOP 
        for index in range(len(selectedObjects)):
            newActiveObjects = []
      
            for active in activeObjects:
                newObj = self.cloneObject(active)
                self.doBool(newObj,self.slicerContainers[index].left,'DIFFERENCE')
   
                if(len(newObj.data.vertices) == 0):
                    bpy.ops.object.delete()
                else:
                    newActiveObjects.append(newObj)
                    #USE INDEX TO AVOID REMOVING THE RESULT OF LAST SLICING LOOP
                    if newObj not in objectsToRemove and index < loopCount:
                        objectsToRemove.append(newObj)
                
                newObj = self.cloneObject(active)
                self.doBool(newObj,self.slicerContainers[index].right,'DIFFERENCE')

                
                if(len(newObj.data.vertices) == 0):
                    bpy.ops.object.delete()
                else:
                    newActiveObjects.append(newObj)
                    
                    if newObj not in objectsToRemove and index < loopCount:
                        objectsToRemove.append(newObj)

                #HIDE ACTIVE OBJECT 
                if(context.scene.my_tool.bool_keepOriginal == False):
                    if active not in objectsToRemove:
                        objectsToRemove.append(active)
                else:
                    active.hide_set(True)
                #UPDATE THE LIST OF OBJECT TO SLICE WITH RESULTS OF RECENT SLICING
                activeObjects = newActiveObjects
            
        
        #CLEANUP

        #DELETE BOOL CONTAINERS
        for container in self.slicerContainers:
            bpy.data.objects.remove(container.left, do_unlink=True)
            bpy.data.objects.remove(container.right, do_unlink=True)
        self.slicerContainers.clear()
        
        #CLEANUP SLICER PLANES
        for src in selectedObjects:
            if(context.scene.my_tool.slicersAction == "Hide"):
                src.hide_set(True)
            else: 
                if(context.scene.my_tool.slicersAction == "Delete"):
                    bpy.data.objects.remove(src, do_unlink=True)
        
        #RENAME
        for i in range(len(activeObjects)):
            activeObjects[i].name = "Bool result " + str(i)
            if(context.scene.my_tool.bool_resetOrigin == True):
                activeObjects[i].select_set(True)
                bpy.context.view_layer.objects.active = activeObjects[i]
                bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
                
        #REMOVE TEMP OBJECTS
        if(context.scene.my_tool.bool_deleteChunks == True):
            for obj in objectsToRemove:
                bpy.data.objects.remove(obj, do_unlink=True)
            
            objectsToRemove.clear()
        return {'FINISHED'}
    
    
class SLICE_PT_Panel(bpy.types.Panel):
    bl_label = "Mesh Slicer"
    bl_idname = "SLICE_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        
        my_tool = context.scene.my_tool

        #SLICER GENERATION
        layout.label(text="Create slicers:")
        box = layout.box()
        box.prop(my_tool, "slicerSize")
        sub = box.row()
        sub.scale_y = 2.0
        sub.operator(GENERATE_SLICERS_OT.bl_idname, text= "Single").variant = 0
        sub.operator(GENERATE_SLICERS_OT.bl_idname, text= "Double").variant = 1
        sub.operator(GENERATE_SLICERS_OT.bl_idname, text= "Triple").variant = 2
       
        #SLICING OPTIONS
        layout.label(text="Perform slicing:")
        box = layout.box()
        row = box.row()
        row.prop(my_tool, "bool_deleteChunks")
        row = box.row()
        row.prop(my_tool, "bool_keepOriginal")
        row = box.row()
        row.prop(my_tool, "bool_resetOrigin")
        row = box.row()
        row.label(text= "What to do with slicers?", icon= 'SELECT_INTERSECT')
        row = box.row()
        row.prop(my_tool, "slicersAction", text= "")
        layout.separator()
     
        row = box.row(align=True)
        sub = row.row()
        sub.scale_y = 2.0
        
        #SLICE BUTTON
        objName = "Slice"
        if(len(bpy.context.selected_objects) > 0):
            objName = "Slice: " + str(bpy.context.active_object.name)
        
        sub.operator(SLICE_OT.bl_idname, icon= 'MOD_BOOLEAN', text= objName)
        if(len(bpy.context.selected_objects) > 1):
            sub.enabled = True
        else:
            sub.enabled = False
            
def register():
    bpy.utils.register_class(SLICE_PT_Panel)
    bpy.utils.register_class(SLICE_OT)
    bpy.utils.register_class(GENERATE_SLICERS_OT)
    bpy.utils.register_class(My_settings)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=My_settings)
def unregister():
    del bpy.types.Scene.my_tool
    bpy.utils.unregister_class(SLICE_PT_Panel)
    bpy.utils.unregister_class(SLICE_OT)
    bpy.utils.unregister_class(GENERATE_SLICERS_OT)
    bpy.utils.unregister_class(My_settings)    

if __name__ == "__main__":
    register()
