from maya import cmds

from ayon_core.pipeline import InventoryAction
from ayon_maya.api.lib import get_reference_node


class ReloadReference(InventoryAction):
    """Reload previously unloaded references."""

    label = "Reload Reference"
    icon = "play"
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

            if cmds.referenceQuery(ref_node, isLoaded=True):
                print("Reference already loaded: {}".format(ref_node))
                continue

            ref_file = cmds.referenceQuery(
                ref_node, f=True, withoutCopyNumber=True
            )
            cmds.file(ref_file, loadReference=ref_node)

        return True

    @classmethod
    def is_compatible(cls, container):
        return container.get("loader") in cls.supported_loaders
