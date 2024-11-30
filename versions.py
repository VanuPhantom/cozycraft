from typing import Callable, Union, cast

import portablemc.standard
from pytermgui import Button, Container, Splitter, Widget, keys, tim


class VersionProvider:
    def __init__(self):
        version_manifest = portablemc.standard.VersionManifest()
        self.versions: list[str] = [
            version["id"] for version in version_manifest.all_versions()
        ]
        self.page_index: int = 0
        self.highlight_index: int = 0

    def get_page(self, n: int) -> list[str]:
        return self.versions[n * 20 : (n + 1) * 20]

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

    def scroll_down(self) -> None:
        if self.highlight_index < len(self.page) - 1:
            self.highlight_index += 1

    def scroll_up(self) -> None:
        if self.highlight_index > 0:
            self.highlight_index -= 1


class VersionListItem(Widget):
    def __init__(self, value: str, on_click: Callable[[str], None], **args):
        super().__init__(**args)
        self.value = value
        self.on_click = on_click
        self._selected = False

    @property
    def selectables_length(self) -> int:
        if len(self.value) > 0:
            return 1
        else:
            return 0

    def select(self, index: Union[int, None] = None) -> None:
        self._selected = index is not None

    def get_lines(self) -> list[str]:
        if self._selected:
            return [tim.parse(f"[bold]{self.value}")]
        else:
            return [self.value]

    def handle_key(self, key: str) -> bool:
        if key == keys.ENTER:
            self.on_click(self.value)
            return True
        else:
            return False


class VersionList(Container):
    def __init__(
        self, version_provider: VersionProvider, on_select: Callable[[str], None]
    ) -> None:
        super().__init__()

        # Set up state management
        self.version_provider = version_provider

        # Initialise the sub-widgets
        self.labels: list[VersionListItem] = [
            VersionListItem(version, on_select, parent_align=0)
            for version in self.version_provider.page
        ]

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
                self.labels[i]._selectables_length = 1
            else:
                self.labels[i]._selectables_length = 0
                self.labels[i].value = ""

    def previous(self) -> None:
        self.version_provider.previous_page()
        self._update_content()

    def next(self) -> None:
        self.version_provider.next_page()
        self._update_content()
