"""
This is NOT for running standalone. You must use it as a blender script
"""
import sys
import bpy
# required for import TODO that only works for windows x(
sys.path.append('\\'.join(bpy.data.filepath.split('\\')[:-2]))
from electromagnetism import ChargeSystem, Charge, process_coordinates


def electron_animation_from_coords(name, coords, initial_location=(0, 0, 0), frames_per_keyframe=7):
    """Animate an electron from a list of coordinates"""
    electron_mesh = bpy.ops.mesh.primitive_uv_sphere_add(
        location=initial_location
    )
    electron_object = bpy.context.object
    electron_object.name = name

    for f, coord in enumerate(coords):
        electron_object.location = tuple(coord)
        electron_object.keyframe_insert("location", frame=f * frames_per_keyframe)


v = ChargeSystem(3)
c1 = Charge(-5 * 10 ** -5, v, position=[0, 0, 0])
c2 = Charge(5 * 10 ** -5, v, position=[10, 10, 10])
anim = process_coordinates(v, 60)

for ind, charge_coords in enumerate(anim):
    electron_animation_from_coords('electron{}'.format(ind), charge_coords, frames_per_keyframe=4)
