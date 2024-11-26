import pytermgui as ptg

from versions import VersionList, VersionProvider

version_provider = VersionProvider()

with ptg.WindowManager() as manager:
    selector_window = ptg.Window()

    def on_select(version_id: str) -> None:
        global selector_window, manager

        selector_window.close()
        manager.add(ptg.Window(version_id))

    manager.layout.add_slot("Body")

    selector_window.set_widgets([VersionList(version_provider, on_select)])
    manager.add(
            selector_window
    )

