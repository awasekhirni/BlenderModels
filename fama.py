##Copyright 2025 β ORI Inc.Canada All Rights Reserved.
## Author: Awase Khirni Syed

import bpy
import math

# ==========================================
# 1. UTILITY & MATERIAL CLASSES
# ==========================================

class MaterialManager:
    """Manages the creation and storage of materials."""

    def __init__(self):
        self.materials = {}
        self._create_all_materials()

    def _create_material(self, name, color, metallic=0.0, roughness=0.5):
        """Helper to create a single PBR material."""
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (*color, 1.0)
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
        self.materials[name] = mat
        return mat

    def _create_all_materials(self):
        """Initialize all required materials for Fama."""
        self._create_material("Skin", (0.4, 0.25, 0.18), metallic=0.0, roughness=0.7)
        self._create_material("Turban", (0.92, 0.88, 0.82), metallic=0.0, roughness=0.8)
        self._create_material("Veil", (0.95, 0.93, 0.90), metallic=0.0, roughness=0.9)
        self._create_material("Armor", (0.55, 0.35, 0.20), metallic=0.3, roughness=0.4)
        self._create_material("ArmGuard", (0.35, 0.50, 0.35), metallic=0.2, roughness=0.5)
        self._create_material("Clothing", (0.75, 0.65, 0.50), metallic=0.0, roughness=0.7)
        self._create_material("Blade", (0.85, 0.85, 0.88), metallic=0.9, roughness=0.2)
        self._create_material("Handle", (0.35, 0.20, 0.10), metallic=0.1, roughness=0.6)

    def get(self, name):
        return self.materials.get(name)


# ==========================================
# 2. SCENE ENVIRONMENT CLASS
# ==========================================

class SceneEnvironment:
    """Handles scene setup, lighting, and camera."""

    @staticmethod
    def clear_scene():
        """Removes all objects from the current scene."""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

    @staticmethod
    def setup_lighting():
        """Creates a basic three-point lighting setup."""
        # Key Light
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        key_light = bpy.context.active_object
        key_light.name = "Key_Light"
        key_light.data.energy = 1.5

        # Fill Light
        bpy.ops.object.light_add(type='AREA', location=(-5, -3, 5))
        fill_light = bpy.context.active_object
        fill_light.name = "Fill_Light"
        fill_light.data.energy = 0.5
        fill_light.data.size = 5

        # Rim Light
        bpy.ops.object.light_add(type='POINT', location=(0, -5, 3))
        rim_light = bpy.context.active_object
        rim_light.name = "Rim_Light"
        rim_light.data.energy = 0.8

    @staticmethod
    def setup_camera():
        """Creates and positions the camera."""
        bpy.ops.object.camera_add(location=(3, -4, 2))
        camera = bpy.context.active_object
        camera.name = "Main_Camera"
        camera.rotation_euler = (math.radians(70), 0, math.radians(45))
        bpy.context.scene.camera = camera


# ==========================================
# 3. CHARACTER COMPONENT CLASSES
# ==========================================

class HeadComponent:
    """Models the head, turban, and face veil."""

    def __init__(self, mat_manager):
        self.mat_manager = mat_manager
        self.objects = []

    def build(self):
        # Head
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.3, location=(0, 0, 1.7))
        head = bpy.context.active_object
        head.name = "Head"
        head.data.materials.append(self.mat_manager.get("Skin"))
        self.objects.append(head)

        # Turban Base
        bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.12,
                                         major_segments=48, minor_segments=16, location=(0, 0, 1.75))
        turban = bpy.context.active_object
        turban.name = "Turban"
        turban.rotation_euler = (math.radians(90), 0, 0)
        turban.data.materials.append(self.mat_manager.get("Turban"))
        self.objects.append(turban)

        # Turban Wrap 2
        bpy.ops.mesh.primitive_torus_add(major_radius=0.38, minor_radius=0.08,
                                         major_segments=48, minor_segments=16, location=(0, 0, 1.85))
        turban2 = bpy.context.active_object
        turban2.name = "Turban_Wrap2"
        turban2.rotation_euler = (math.radians(90), 0, 0)
        turban2.data.materials.append(self.mat_manager.get("Turban"))
        self.objects.append(turban2)

        # Face Veil
        bpy.ops.mesh.primitive_plane_add(size=0.6, location=(0, 0.25, 1.65))
        veil = bpy.context.active_object
        veil.name = "Face_Veil"
        veil.scale = (1.0, 0.5, 1.5)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        veil.data.materials.append(self.mat_manager.get("Veil"))
        self.objects.append(veil)


class BodyComponent:
    """Models the torso and underlying clothing."""

    def __init__(self, mat_manager):
        self.mat_manager = mat_manager
        self.objects = []

    def build(self):
        # Torso
        bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=0.8, location=(0, 0, 1.0))
        torso = bpy.context.active_object
        torso.name = "Torso"
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(1.2, 1.2, 1.0))
        bpy.ops.object.mode_set(mode='OBJECT')
        torso.data.materials.append(self.mat_manager.get("Skin"))
        self.objects.append(torso)

        # Tunic
        bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=0.9, location=(0, 0, 0.85))
        tunic = bpy.context.active_object
        tunic.name = "Tunic"
        tunic.scale = (1.1, 1.1, 1.0)
        tunic.data.materials.append(self.mat_manager.get("Clothing"))
        self.objects.append(tunic)


class ArmorComponent:
    """Models the chest armor and arm guards."""

    def __init__(self, mat_manager):
        self.mat_manager = mat_manager
        self.objects = []

    def build(self):
        # Chest Armor
        bpy.ops.mesh.primitive_cylinder_add(radius=0.38, depth=0.5, location=(0, 0, 1.1))
        chest = bpy.context.active_object
        chest.name = "Chest_Armor"
        chest.scale = (1.0, 1.0, 0.8)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        chest.data.materials.append(self.mat_manager.get("Armor"))
        self.objects.append(chest)

        # Left Arm Guard
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.5, location=(0.4, 0, 0.9))
        left_arm = bpy.context.active_object
        left_arm.name = "Left_Arm_Guard"
        left_arm.rotation_euler = (0, 0, math.radians(-20))
        left_arm.data.materials.append(self.mat_manager.get("ArmGuard"))
        self.objects.append(left_arm)

        # Right Arm Guard
        bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.5, location=(-0.4, 0, 0.9))
        right_arm = bpy.context.active_object
        right_arm.name = "Right_Arm_Guard"
        right_arm.rotation_euler = (0, 0, math.radians(20))
        right_arm.data.materials.append(self.mat_manager.get("ArmGuard"))
        self.objects.append(right_arm)


class WeaponComponent:
    """Models the curved scimitar sword."""

    def __init__(self, mat_manager):
        self.mat_manager = mat_manager
        self.objects = []

    def build(self):
        # Blade
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=1.2, location=(0.6, 0.3, 1.4))
        blade = bpy.context.active_object
        blade.name = "Sword_Blade"
        blade.rotation_euler = (0, 0, math.radians(-45))
        blade.scale = (1.0, 0.2, 1.5)
        blade.data.materials.append(self.mat_manager.get("Blade"))
        self.objects.append(blade)

        # Handle
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.25, location=(0.75, 0.2, 1.25))
        handle = bpy.context.active_object
        handle.name = "Sword_Handle"
        handle.rotation_euler = (0, 0, math.radians(-45))
        handle.data.materials.append(self.mat_manager.get("Handle"))
        self.objects.append(handle)

        # Guard
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.05, location=(0.7, 0.25, 1.3))
        guard = bpy.context.active_object
        guard.name = "Sword_Guard"
        guard.rotation_euler = (0, 0, math.radians(-45))
        guard.data.materials.append(self.mat_manager.get("Armor"))
        self.objects.append(guard)


# ==========================================
# 4. MAIN CHARACTER CONTROLLER
# ==========================================

class FamaCharacter:
    """Main orchestrator class that builds the complete character."""

    def __init__(self):
        self.mat_manager = MaterialManager()
        self.components = [
            HeadComponent(self.mat_manager),
            BodyComponent(self.mat_manager),
            ArmorComponent(self.mat_manager),
            WeaponComponent(self.mat_manager)
        ]
        self.all_objects = []

    def build(self):
        """Executes the full build pipeline."""
        print("Initializing Fama Character Build...")

        # 1. Setup Environment
        SceneEnvironment.clear_scene()
        SceneEnvironment.setup_lighting()
        SceneEnvironment.setup_camera()

        # 2. Build Components
        for component in self.components:
            component.build()
            self.all_objects.extend(component.objects)

        # 3. Parent all to a root empty for clean outliner
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        root = bpy.context.active_object
        root.name = "Fama_Root"
        for obj in self.all_objects:
            obj.parent = root

        print("Fama Character build complete!")


# ==========================================
# 5. EXECUTION
# ==========================================

if __name__ == "__main__":
    # Instantiate and build the character
    fama = FamaCharacter()
    fama.build()
