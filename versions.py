from typing import cast
import portablemc.standard
from pytermgui import Button, Container, Label, Splitter, Widget, keys
from pytermgui.widgets import keys

class VersionProvider:
    def __init__(self):
        version_manifest = portablemc.standard.VersionManifest()
        self.versions: list[str] = [version["id"] for version in version_manifest.all_versions()]
        self.page_index: int = 0

    def get_page(self, n: int) -> list[str]:
        return self.versions[n*20:(n+1)*20]

    @property
    def page(self) -> list[str]:
        return self.get_page(self.page_index)

    @property
    def page_count(self) -> int:
        version_count = len(self.versions)

        if version_count % 20 == 0:
            return version_count // 20
        else:
            return version_count // 20 + 1

    def next_page(self) -> None:
        if self.page_index < self.page_count - 1:
            self.page_index += 1

    def previous_page(self) -> None:
        if self.page_index > 0:
            self.page_index -= 1

class VersionList(Container):
    def __init__(self, version_provider: VersionProvider) -> None:
        super().__init__()

        # Set up state management
        self.version_provider = version_provider

        # Initialise the sub-widgets
        self.labels: list[Label] = [Label(version, parent_align=0) for version in self.version_provider.page]

        previous_button: Widget = Button("<", onclick=lambda _: self.previous())
        next_button: Widget = Button(">", onclick=lambda _: self.next())

        self.button_wrapper: Widget = Splitter(previous_button, next_button)

        # Populate the sub-widgets with content
        self._update_content()

        # Insert the sub-widgets
        self.set_widgets(cast(list[Widget], self.labels) + [self.button_wrapper])

    def _update_content(self) -> None:
        page = self.version_provider.page

        for i in range(len(self.labels)):
            if i < len(page):
                self.labels[i].value = page[i]
            else:
                self.labels[i].value = ""

    def previous(self) -> None:
        self.version_provider.previous_page()
        self._update_content()

    def next(self) -> None:
        self.version_provider.next_page()
        self._update_content()

