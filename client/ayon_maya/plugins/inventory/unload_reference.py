from maya import cmds

from ayon_core.pipeline import InventoryAction
from ayon_maya.api.lib import get_reference_node


class UnloadReference(InventoryAction):
    """Unload selected references from the scene."""

    label = "Unload Reference"
    icon = "pause"
    color = "#d8d8d8"

    supported_loaders = {"ReferenceLoader", "MayaUSDReferenceLoader"}

    def process(self, containers):
        for container in containers:
            if container["loader"] not in self.supported_loaders:
                print("Not a reference, skipping")
                continue

            node = container["objectName"]
            members = cmds.sets(node, query=True, nodesOnly=True)
            ref_node = get_reference_node(members)

            if not cmds.referenceQuery(ref_node, isLoaded=True):
                print("Reference already unloaded: {}".format(ref_node))
                continue

            ref_file = cmds.referenceQuery(ref_node, f=True)
            cmds.file(ref_file, unloadReference=True)

        return True

    @classmethod
    def is_compatible(cls, container):
        return container.get("loader") in cls.supported_loaders
