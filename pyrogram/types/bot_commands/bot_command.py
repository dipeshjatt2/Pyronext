from __future__ import annotations

from pyrogram import raw
from pyrogram.types.object import Object


class BotCommand(Object):
    """A bot command with the standard slash "/" prefix.

    Parameters:
        command (``str``):
            Text of the command; 1-32 characters.
            Can contain only lowercase English letters, digits and underscores.

        description (``str``):
            Description of the command; 1-256 characters.

        is_ephemeral (``bool``, *optional*):
            Pass True to make this command execute ephemerally.
    """

    def __init__(self, command: str, description: str, is_ephemeral: bool = False) -> None:
        super().__init__()

        self.command = command
        self.description = description
        self.is_ephemeral = is_ephemeral

    def write(self) -> raw.types.BotCommand:
        return raw.types.BotCommand(
            command=self.command,
            description=self.description,
            ephemeral=self.is_ephemeral or None,
        )

    @staticmethod
    def read(c: raw.types.BotCommand) -> BotCommand:
        return BotCommand(
            command=c.command,
            description=c.description,
            is_ephemeral=bool(c.ephemeral)
        )
