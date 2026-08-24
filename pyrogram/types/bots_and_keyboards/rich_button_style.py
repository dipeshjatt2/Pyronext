from __future__ import annotations

from pyrogram import enums, raw, types
from pyrogram.types.object import Object


class RichButtonStyle(Object):
    """Style of a button embedded in rich text or page blocks.

    Parameters:
        bg_primary (``bool``, *optional*):
            Whether the button should be primary.

        bg_danger (``bool``, *optional*):
            Whether the button should be danger.

        bg_success (``bool``, *optional*):
            Whether the button should be success.

        link (``bool``, *optional*):
            Whether the button should be styled as a link.
    """

    def __init__(
        self,
        *,
        bg_primary: bool | None = None,
        bg_danger: bool | None = None,
        bg_success: bool | None = None,
        link: bool | None = None,
    ) -> None:
        super().__init__()

        self.bg_primary = bg_primary
        self.bg_danger = bg_danger
        self.bg_success = bg_success
        self.link = link

    @staticmethod
    def read(b: raw.base.RichButtonStyle | None) -> RichButtonStyle | None:
        if not b:
            return None

        return RichButtonStyle(
            bg_primary=b.bg_primary,
            bg_danger=b.bg_danger,
            bg_success=b.bg_success,
            link=b.link,
        )

    def write(self) -> raw.types.RichButtonStyle:
        return raw.types.RichButtonStyle(
            bg_primary=self.bg_primary,
            bg_danger=self.bg_danger,
            bg_success=self.bg_success,
            link=self.link,
        )

    @staticmethod
    def _parse(
        style: RichButtonStyle | enums.ButtonStyle | None,
    ) -> RichButtonStyle | None:
        if style is None:
            return None

        if isinstance(style, enums.ButtonStyle):
            return RichButtonStyle(
                bg_primary=style == enums.ButtonStyle.PRIMARY,
                bg_danger=style == enums.ButtonStyle.DANGER,
                bg_success=style == enums.ButtonStyle.SUCCESS,
                link=style == enums.ButtonStyle.LINK,
            )

        return style

    @staticmethod
    def write_from(
        style: RichButtonStyle
        | enums.ButtonStyle
        | types.KeyboardButtonStyle
        | None,
    ) -> raw.types.RichButtonStyle | None:
        """Convert any supported style object into a raw RichButtonStyle."""
        if style is None:
            return None

        if isinstance(style, enums.ButtonStyle):
            normalized = RichButtonStyle._parse(style)

            return normalized.write() if normalized else None

        if isinstance(style, RichButtonStyle):
            return style.write()

        if isinstance(style, types.KeyboardButtonStyle):
            return raw.types.RichButtonStyle(
                bg_primary=style.bg_primary,
                bg_danger=style.bg_danger,
                bg_success=style.bg_success,
                link=None,
            )

        return None
