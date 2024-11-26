import pytermgui as ptg
from versions import VersionProvider, VersionList

version_provider = VersionProvider()

with ptg.WindowManager() as manager:
    manager.layout.add_slot("Body")
    manager.add(
            ptg.Window(VersionList(version_provider))
    )

