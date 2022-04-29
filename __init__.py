bl_info = {
    # required обязательный
    "name": "Add Fast Panel Button",
    "blender": (3, 1, 2),
    "location": "View3D > Sidebar > Item",
    "category": "Object",
    # optional дополнительный
    "version": (1, 6, 2),
    "author": "Constantyn6487",
    "description": "Adds acces panel to buttons. Giving speeds job on modificators.",
}

import bpy
from bpy.types import Panel, Operator, AddonPreferences, Mesh
from bpy.props import StringProperty, FloatProperty
from bpy.utils import register_class, unregister_class
    
    ### Weight ### OPERATORS ###
class BUTTON_OT_BevelWeight0(Operator):
    ### buttom left = weith 0 ###
    bl_idname = "button.bevel_weight_0"
    bl_label = "Edge Bevel Weight 0.00"
    bl_description = "Clear the Bevel Weight 0.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=-1)
        return {'FINISHED'}

class BUTTON_OT_BevelWeight1(Operator):
    ### buttom right = weith 1 ###
    bl_idname = "button.bevel_weight_1"
    bl_label = "Edge Bevel Weight 1.00"
    bl_description = "Sets the Bevel Weight 1.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=1)
        return {'FINISHED'}
    
    ### Crease ### OPERATORS ###
class BUTTON_OT_Crease0(Operator):
    ### buttom left = Crease 0 ###
    bl_idname = "button.crease_0"
    bl_label = "Edge Crease 0.00"
    bl_description = "Sets the Crease 0.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_crease(value=-1)
        return {'FINISHED'}
    
class BUTTON_OT_Crease1(Operator):
    ### buttom right = Crease 1 ###
    bl_idname = "button.crease_1"
    bl_label = "Edge Crease 1.00"
    bl_description = "Sets the Crease 1.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_crease(value=1)
        return {'FINISHED'}
    
    ### Sharpness ### OPERATOR ###
class BUTTON_OT_TargetSharpWeight(Operator):
    bl_idname = "button.target_sharp_weight"
    bl_label = "Target Sharp set Weight"
    bl_description = "Select Eage Sargness set Weight 1.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
            bpy.context.tool_settings.mesh_select_mode = (False, True, False)
            bpy.ops.mesh.select_similar(type='SHARP', threshold=0.01)
            bpy.ops.transform.edge_bevelweight(value=1)   
            return {'FINISHED'}
    
    ### Bevel Subdivision EDIT_MESH ### OPERATOR ###
class BUTTON_OT_SpeedOperationBevelSubserfEdit(Operator):
    bl_idname = "button.speed_operation_bev_sub"
    bl_label = "Bevel and Subsurf"
    bl_description = "Adds BEVEL(Weight,Amount=0.005,Shape=1.00), Subdivision(lvl2), and Shade Smooth"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
    ### The current mode is remembered: ###
        mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if mode == 'EDIT_MESH':
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.005
            bpy.context.object.modifiers["Bevel"].segments = 2
            bpy.context.object.modifiers["Bevel"].limit_method = 'WEIGHT'
            bpy.context.object.modifiers["Bevel"].profile = 1
            bpy.ops.object.subdivision_set(level=2, relative=False)
            bpy.context.object.modifiers["Subdivision"].render_levels = 2
            bpy.ops.object.shade_smooth()
            bpy.ops.object.mode_set(mode='EDIT')
            return {'FINISHED'}
    
    ### Bevel Subdivision OBJECT ### OPERATOR ###
class BUTTON_OT_SpeedOperationBevelSubserfObject(Operator):
    bl_idname = "button.speed_operation_bev_sub_object"
    bl_label = "Bevel and Subsurf"
    bl_description = "Adds BEVEL(Weight,Amount=0.005,Segments=2,Shape=1.00), Subdivision(lvl2), and Shade Smooth"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'OBJECT'
    
    def execute(self, context):
    ### The current mode is remembered: ###
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].width = 0.005
        bpy.context.object.modifiers["Bevel"].segments = 2
        bpy.context.object.modifiers["Bevel"].limit_method = 'WEIGHT'
        bpy.context.object.modifiers["Bevel"].profile = 1
        bpy.ops.object.subdivision_set(level=2, relative=False)
        bpy.context.object.modifiers["Subdivision"].render_levels = 2
        bpy.ops.object.shade_smooth()
        return {'FINISHED'}

    ### Panel ### Panel ### Panel ###
class BAR_PT_Panel(Panel):
    bl_idname = 'VIEW3D_PT_example_panel'
    bl_label = 'Button Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
    ### Window, actives object ### 
        obj = context.object
        if obj is not None:
            row = layout.row()
            row.label(text="Active object is: ", icon='OBJECT_DATA')
            box = layout.box()
            box.label(text=obj.name, icon='EDITMODE_HLT')
            
    ### Buttom visibility in edit mode ###
        if context.object is not None and context.mode == 'EDIT_MESH':
            layout.label(text="Speed Crease:")
            col = layout.column()
            spl = col.split(align = True)
            op = spl.operator("button.crease_0", text="c0.00")
            op = spl.operator("button.crease_1", text="c1.00")
            layout.label(text="Speed Edge Bevel Weight:")
            col = layout.column()
            #box = layout.box()
            spl = col.split(align = True)
            #buttom left
            op = spl.operator("button.bevel_weight_0", text="w0.00")
            #buttom right
            op = spl.operator("button.bevel_weight_1", text="w1.00")
            col = layout.column()
            #buttom target sharp set bevel weight 1
            op = col.operator("button.target_sharp_weight", text="Sharp set Weight ")
            
    ### Buttom visibility in edit mode ### Bevel Subdivision ###
        if context.object is not None and context.mode == 'EDIT_MESH':
            layout.label(text="Set Mesh Bevel and Subserf:")
            col = layout.column()
            op = col.operator("button.speed_operation_bev_sub")
            
            ### Auto Smooth ###
            mesh = context.object.data
            layout.use_property_split = True
            col = layout.column(heading="Auto Smooth")
            col.use_property_decorate = False
            row = col.row(align=True)
            sub = row.row(align=True)
            sub.prop(mesh, "use_auto_smooth", text="")
            sub = sub.row(align=True)
            sub.active = mesh.use_auto_smooth and not mesh.has_custom_normals
            sub.prop(mesh, "auto_smooth_angle", text="")
        if context.object is None or context.object.type != "MESH":
            layout.label(icon="ERROR", text = "No mesh selected")
        
        ### Buttom visibility in object and edit mode ### Bevel Subdivision ###
        if context.object is not None and context.mode == 'OBJECT':
            layout.label(text="Set Mesh Bevel and Subserf:")
            col = layout.column()
            op = col.operator("button.speed_operation_bev_sub_object")
            
            ### Auto Smooth ###
            mesh = context.object.data
            layout.use_property_split = True
            col = layout.column(heading="Auto Smooth")
            col.use_property_decorate = False
            row = col.row(align=True)
            sub = row.row(align=True)
            sub.prop(mesh, "use_auto_smooth", text="")
            sub = sub.row(align=True)
            sub.active = mesh.use_auto_smooth and not mesh.has_custom_normals
            sub.prop(mesh, "auto_smooth_angle", text="")
        
        
    ### Category Update Panel ###
panels = (
        BAR_PT_Panel,
        )

def update_panel(self, context):
    message = "Align Tools: Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[__name__].preferences.category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass


class EditCategoryAddonUI(AddonPreferences):
    bl_idname = __name__

    category: StringProperty(
            name="Tab Category",
            description="Choose a name for the category of the panel",
            default="Item",
            update=update_panel
            )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="Tab Category:")
        col.prop(self, "category", text="")
        
CLASSES = [
    BUTTON_OT_BevelWeight0,
    BUTTON_OT_BevelWeight1,
    BUTTON_OT_Crease0,
    BUTTON_OT_Crease1,
    BUTTON_OT_TargetSharpWeight,
    BUTTON_OT_SpeedOperationBevelSubserfEdit,
    BUTTON_OT_SpeedOperationBevelSubserfObject,
    BAR_PT_Panel,
    EditCategoryAddonUI,
]

def register():
    print('registered') # just for debug
    for klass in CLASSES:
        register_class(klass)

def unregister():
    print('unregistered') # just for debug
    for klass in reversed(CLASSES):
        unregister_class(klass)

if __name__ == '__main__':
    register()
    
    #my_msg = "Test Message"
    #bpy.ops.object.warning('INVOKE_DEFAULT', msg = my_msg, type="ERROR") # type может быть "ERROR", "INFO" или "WARNING" 
    
"""
No skills
configure single race settings
add already saved parameters to the object by clicking on the.
activate radio_check_box and menu 
select-> 
-bevel
--width
--segments
--limit_method
--profile
activate radio_check_box and menu
-subsurf
--levels
--render_levels
activate radio_check_box
-shade smooth
activate radio_check_box
-use_auto_smooth
and menu
-auto_smooth_angle
"""