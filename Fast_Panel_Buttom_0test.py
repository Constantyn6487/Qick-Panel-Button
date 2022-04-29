bl_info = {
    # required обязательный
    "name": "ADD BUTTON BAR",
    "blender": (3, 1, 2),
    "location": "View3D > Sidebar > Item",
    "category": "Object",
    # optional дополнительный
    "version": (1, 1, 0),
    "author": "Constantyn6487",
    "description": "Adds acces panel to buttoms. Giving speeds job on modificators.",
}

import bpy
from bpy.types import Panel, Operator, AddonPreferences, Mesh
from bpy.props import StringProperty, FloatProperty
from bpy.utils import register_class, unregister_class

class MY_OT_Warning(Operator):
    bl_idname = "object.warning"
    bl_label = "Warning!"
    type: StringProperty(default="ERROR")
    msg : StringProperty(default="")
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        return {'FINISHED'}
    
    def modal(self, context, event):
        if event:
            self.report({self.type}, self.msg)
        return {'FINISHED'}
        
    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    
    ### Weight ### OPERATORS ###
class BUTTOM_OT_BevelWeight0(Operator):
    ### buttom left = weith 0 ###
    bl_idname = "buttom.bevel_weight_0"
    bl_label = "Edge Bevel Weight 0.00"
    bl_description = "Clear the Bevel Weight 0.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=-1)
        return {'FINISHED'}

class BUTTOM_OT_BevelWeight1(Operator):
    ### buttom right = weith 1 ###
    bl_idname = "buttom.bevel_weight_1"
    bl_label = "Edge Bevel Weight 1.00"
    bl_description = "Sets the Bevel Weight 1.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=1)
        return {'FINISHED'}
    
    ### Sharpness ### OPERATOR ###
class BUTTOM_OT_TargetSharpWeight(Operator):
    bl_idname = "buttom.target_sharp_weight"
    bl_label = "Target Sharp set Weight"
    bl_description = "Select Eage Sargness set Weight 1.00"
    
    @classmethod
    def poll(self, context):
        return context.object is not None and context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        bpy.context.tool_settings.mesh_select_mode = (False, True, False)
        if context.tool_settings.mesh_select_mode == (False, True, False):
            my_msg = "!!! No edges selected !!!"
            bpy.ops.object.warning('INVOKE_DEFAULT', msg = my_msg, type="ERROR", icon="ERROR")
        bpy.ops.mesh.select_similar(type='SHARP', threshold=0.01)
        bpy.ops.transform.edge_bevelweight(value=1)
        
        return {'FINISHED'}
    
    ### Bevel Subdivision ### OPERATOR ###
class BUTTOM_OT_SpeedOperationBevelSubserf(Operator):
    bl_idname = "buttom.speed_operation_bev_sub"
    bl_label = "Bevel and Subsurf"
    bl_description = "Adds BEVEL(Weight,Amount=0.005,Shape=1.00), Subdivision(lvl2), and Shade Smooth"
    
    #@classmethod
    #def poll(self, context):
    #    return context.object is not None and context.mode == 'OBJECT'
    
    def execute(self, context):
    ### The current mode is remembered: ###
        mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        if mode == 'EDIT_MESH':
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].width = 0.005
            bpy.context.object.modifiers["Bevel"].limit_method = 'WEIGHT'
            bpy.context.object.modifiers["Bevel"].profile = 1
            bpy.ops.object.subdivision_set(level=3, relative=False)
            bpy.ops.object.shade_smooth()
            bpy.ops.object.mode_set(mode='EDIT')
        #bpy.context.object.data.use_auto_smooth = True
        #bpy.context.object.data.auto_smooth_angle = 0.698132
        return {'FINISHED'}

    ### Panel ###
class BAR_PT_Panel(Panel):
    bl_idname = 'VIEW3D_PT_example_panel'
    bl_label = 'Buttom Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
    
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
            layout.label(text="Speed Edge Bevel Weight:")
            col = layout.column()
            #box = layout.box()
            spl = col.split(align = True)
                #buttom left
            op = spl.operator("buttom.bevel_weight_0", text="0.00")
                #buttom right
            op = spl.operator("buttom.bevel_weight_1", text="1.00")
            col = layout.column()
                #buttom target sharp set bevel weight 1
            op = col.operator("buttom.target_sharp_weight", text="Sharp set Weight ")
            
    ### Buttom visibility in object and edit mode ### Bevel Subdivision ###
        if context.object is not None and context.mode:
            layout.label(text="Set Mesh Bevel and Subserf:")
            col = layout.column()
            op = col.operator("buttom.speed_operation_bev_sub")
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
        else:
            layout.label(icon="ERROR", text = "No mesh selected")
        
        
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
    BUTTOM_OT_BevelWeight0,
    BUTTOM_OT_BevelWeight1,
    BUTTOM_OT_TargetSharpWeight,
    BUTTOM_OT_SpeedOperationBevelSubserf,
    BAR_PT_Panel,
    EditCategoryAddonUI,
    MY_OT_Warning
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