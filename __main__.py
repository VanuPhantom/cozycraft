from portablemc.standard import Version
import pytermgui as ptg

from versions import VersionList, VersionProvider

version_provider = VersionProvider()
selected_version = None


class FixedWindowManager(ptg.WindowManager):
    def __init__(self, **args):
        super().__init__(**args)

    def on_resize(self, size):
        if self._is_running:
            super().on_resize(size)


with FixedWindowManager(autorun=False) as manager:
    selector_window = ptg.Window()

    def on_select(version_id: str) -> None:
        global manager, selected_version, selector_window

        selected_version = version_id
        manager.stop()

    manager.layout.add_slot("Body")

    selector_window.set_widgets([VersionList(version_provider, on_select)])
    manager.add(selector_window)
    manager.run()

if selected_version is not None:
    print(f"\r\nLaunching {selected_version}")
    Version(selected_version).install().run()
    print("\r\nThanks for using Cozycraft. Goodbye!")
else:
    print(f"\r\nNo version selected. Exiting...")
