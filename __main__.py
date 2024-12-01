from portablemc.standard import (
    DownloadCompleteEvent,
    DownloadProgressEvent,
    DownloadStartEvent,
    JarFoundEvent,
    Version,
    Watcher,
)
from progress.bar import Bar
import pytermgui as ptg

from versions import VersionList, VersionProvider

version_provider = VersionProvider()
selected_version = None


class ProgressWatcher(Watcher):
    def __init__(self, version_id: str):
        self.version_id = version_id

    def handle(self, event) -> None:
        if isinstance(event, DownloadStartEvent) and event.size is not None:
            self.bar = Bar(
                "Downloading",
                max=event.size // 1_000,
                suffix=f"0/{event.size // 1_000} kb",
            )
        elif (
            isinstance(event, DownloadProgressEvent)
            and event.entry.size is not None
            and hasattr(self, "bar")
        ):
            self.bar.message = f"Downloading {event.entry.name}"
            self.bar.suffix = f"{event.size // 1_000}/{event.entry.size // 1_000} kb"
            self.bar.max = event.entry.size // 1_000
            self.bar.goto(event.size // 1_000)
        elif isinstance(event, DownloadCompleteEvent) and hasattr(self, "bar"):
            self.bar.finish()
        elif isinstance(event, JarFoundEvent):
            print(f"Jar file for {self.version_id} found")


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
    Version(selected_version).install(watcher=ProgressWatcher(selected_version)).run()
    print("\r\nThanks for using Cozycraft. Goodbye!")
else:
    print(f"\r\nNo version selected. Exiting...")
