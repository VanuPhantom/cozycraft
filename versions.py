from typing import Callable, Tuple

import portablemc.standard
from pytermgui import HorizontalAlignment, Widget, keys, tim


class VersionProvider:
    def __init__(self):
        version_manifest = portablemc.standard.VersionManifest()
        self.versions: list[str] = [
            version["id"] for version in version_manifest.all_versions()
        ]
        self.highlight_index = 0
        self.index_within_view = 0
        self.query = ""

    def select(self, index: int) -> None:
        start, end = self.visible_range

        self.highlight_index = index

        if index < start:
            if index >= 5:
                self.index_within_view = 5
            else:
                self.index_within_view = index
        elif index > end:
            if index <= len(self.versions) - 6:
                self.index_within_view = 14
            else:
                self.index_within_view = 14 + len(self.filtered_versions) - 1 - index
        else:
            self.index_within_view = index - start

    def scroll_down(self) -> None:
        if self.highlight_index < len(self.filtered_versions):
            self.highlight_index += 1

            if (
                self.index_within_view < 14
                or self.highlight_index >= len(self.filtered_versions) - 6
            ):
                self.index_within_view += 1

    def scroll_up(self) -> None:
        if self.highlight_index > 0:
            self.highlight_index -= 1

            if self.index_within_view > 5 or self.highlight_index < 5:
                self.index_within_view -= 1

    @property
    def visible_versions(self) -> list[str]:
        start, end = self.visible_range

        return self.filtered_versions[start:end]

    @property
    def visible_range(self) -> Tuple[int, int]:
        start = self.highlight_index - self.index_within_view
        end = (
            start + 20
            if len(self.filtered_versions) >= 20
            else len(self.filtered_versions)
        )

        return (start, end)

    @property
    def selected_version(self) -> str | None:
        if len(self.filtered_versions) > 0:
            return self.filtered_versions[self.highlight_index]
        else:
            return None

    @property
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, query: str) -> None:
        self._query = query
        self.filtered_versions = [
            version for version in self.versions if query in version
        ]
        self.highlight_index = 0
        self.index_within_view = 0


class VersionList(Widget):
    def __init__(
        self, version_provider: VersionProvider, on_select: Callable[[str], None]
    ) -> None:
        super().__init__(parent_align=HorizontalAlignment.LEFT)

        self.version_provider = version_provider

        self.on_select = on_select

    def get_lines(self) -> list[str]:
        versions = self.version_provider.visible_versions

        return [
            (
                tim.parse(f"[bold]{version}")
                if version == self.version_provider.selected_version
                else version
            )
            for version in versions
        ] + [self.version_provider.query]

    def handle_key(self, key: str) -> bool:
        if super().handle_key(key):
            return True

        if key in "abcdefghijklmnopqrstuvwxyz1234567890.-_()/":
            self.version_provider.query += key
        elif key == keys.BACKSPACE:
            self.version_provider.query = self.version_provider.query[
                : (
                    len(self.version_provider.query) - 1
                    if len(self.version_provider.query) > 0
                    else 0
                )
            ]
        elif key == keys.UP:
            self.version_provider.scroll_up()
            return False
        elif key == keys.DOWN:
            self.version_provider.scroll_down()
            return False
        elif key == keys.ENTER:
            selected_version = self.version_provider.selected_version

            if selected_version is not None:
                self.on_select(selected_version)
                return False
            else:
                return True

        return True

    @property
    def selectables_length(self) -> int:
        return len(self.version_provider.versions)

    def select(self, index: int | None = None) -> None:
        if index is not None:
            self.version_provider.highlight_index = index
