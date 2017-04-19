import bpy
import math

bl_info = {
    "name": "Snap2ortho",
    "author": "Martin Durhuus",
    "version": (1,0),
    "blender": (2,77,0),
    "location": "3d view",
    "description": "Align view with a specific angled view and press ALT+MMB to snap into ortho mode for that view",
    "warning": "Enable 'auto-perspective' in user preferences for the addon to work as intended.",
    "category": "3D View",
}

def main(context):
    for area in context.screen.areas:
        if area.type == 'VIEW_3D':
            r3d = area.spaces.active.region_3d
            view_matrix = r3d.view_matrix   
            view_orientation = get_view_orientation_from_matrix(view_matrix).upper()
    return view_orientation    
        
def get_view_orientation_from_matrix(view_matrix):
    r = lambda x: round(x, 2)
    view_rot = view_matrix.to_euler()
    
    orientation_dict = {
    (0.0,0.0,0.0) : 'TOP',
    (r(math.pi), 0.0, 0.0) : 'BOTTOM',
    (r(-math.pi/2), 0.0,0.0): 'FRONT',
    (r(math.pi/2), 0.0, r(-math.pi)) : 'BACK',
    (r(-math.pi/2), r(math.pi/2), 0.0) : 'LEFT',
    (r(-math.pi/2), r(-math.pi/2), 0.0) : 'RIGHT'}
    
    return orientation_dict.get(tuple(map(r, view_rot)), 'USER')

class superAutoPerspective(bpy.types.Operator):
    """
    Enable 'auto-perspective' to work properly. The AddOn does not make much sense without, anyways.
    """
    bl_idname="object.view3d"
    bl_label="Orient view"
    
    def __init__(self):
        print("Start")

    def __del__(self):
        print("End")
    
    def execute(self, context):
        print("\n".join(main(context)))
        view = main(context)
        if view != 'USER':
            bpy.ops.view3d.viewnumpad(type=view)
        return {'FINISHED'}

keymaps = []

def register():
    bpy.utils.register_class(superAutoPerspective)
    #Handle keymapping
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new(superAutoPerspective.bl_idname, 'MIDDLEMOUSE', 'PRESS', alt=True)
    keymaps.append(km)
    
def unregister():
    bpy.utils.unregister_class(superAutoPerspective)
    #Unhandle keymapping
    wm = bpy.context.window_manager
    for km in keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    #clear list
    del keymaps[:]
    
if __name__ == '__main__':
    register()