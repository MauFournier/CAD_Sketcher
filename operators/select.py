from bpy.types import Operator, Context
from bpy.props import IntProperty, BoolProperty
from bpy.utils import register_classes_factory

from .utilities import select_extend, select_invert
from ..utilities.select import select_all, deselect_all
from .. import global_data
from ..declarations import Operators
from ..utilities.highlighting import HighlightElement
from ..utilities.select import mode_property


class View3D_OT_slvs_select(Operator, HighlightElement):
    """
    Select an entity

    Either the entity specified by the index property or the hovered index
    if the index property is not set

    """

    bl_idname = Operators.Select
    bl_label = "Select Sketch Entities"

    index: IntProperty(name="Index", default=-1)
    mode: mode_property

    def execute(self, context: Context):
        indices = (
            [self.index]
            if self.properties.is_property_set("index")
            else global_data.hover
        )
        mode = self.mode
        selected = global_data.selected

        if mode == "SET" and not indices:
            deselect_all(context)

        else:
            if mode == "SET":
                for index in indices:
                    if index in selected:
                        index = indices[
                            (indices.index(index) + 1) % len(indices)
                        ]
                        break

                else:
                    index = indices[0]

                deselect_all(context)
                entity = context.scene.sketcher.entities.get(index)
                entity.selected = True

            elif mode == "ADD":
                for index in indices:
                    if index not in selected:
                        entity = context.scene.sketcher.entities.get(index)
                        entity.selected = True
                        break

            elif mode == "SUBTRACT":
                for index in indices:
                    if index in selected:
                        entity = context.scene.sketcher.entities.get(index)
                        entity.selected = False
                        break

            elif mode == "TOGGLE":
                for index in indices:
                    entity = context.scene.sketcher.entities.get(index)
                    entity.selected = not entity.selected

        context.area.tag_redraw()
        return {"FINISHED"}


class View3D_OT_slvs_select_all(Operator):
    """Select / Deselect all entities"""

    bl_idname = Operators.SelectAll
    bl_label = "Select / Deselect Entities"

    deselect: BoolProperty(name="Deselect")

    def execute(self, context: Context):
        if self.deselect:
            deselect_all(context)
        else:
            select_all(context)
        context.area.tag_redraw()
        return {"FINISHED"}


class View3D_OT_slvs_select_invert(Operator):
    """Invert entities selection"""

    bl_idname = Operators.SelectInvert
    bl_label = "Invert entities selection"

    def execute(self, context: Context):
        select_invert(context)
        context.area.tag_redraw()
        return {"FINISHED"}


class View3D_OT_slvs_select_extend(Operator):
    """Select neighbour entities"""

    bl_idname = Operators.SelectExtend
    bl_label = "Select neighbour entities"

    def execute(self, context: Context):
        select_extend(context)
        context.area.tag_redraw()
        return {"FINISHED"}


class View3D_OT_slvs_select_extend_all(Operator):
    """Select neighbour entities"""

    bl_idname = Operators.SelectExtendAll
    bl_label = "Select neighbour entities"

    def execute(self, context: Context):
        while select_extend(context):
            pass
        context.area.tag_redraw()
        return {"FINISHED"}


register, unregister = register_classes_factory(
    (
        View3D_OT_slvs_select,
        View3D_OT_slvs_select_all,
        View3D_OT_slvs_select_invert,
        View3D_OT_slvs_select_extend,
        View3D_OT_slvs_select_extend_all,
    )
)
