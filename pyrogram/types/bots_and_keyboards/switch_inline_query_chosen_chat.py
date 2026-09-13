from __future__ import annotations

from pyrogram import raw
from pyrogram.types.object import Object


class SwitchInlineQueryChosenChat(Object):
    """This object represents an inline button that switches the current user to inline mode in a chosen chat, with an optional default inline query.

    Parameters:
        query (``str``, *optional*):
            The default inline query to be inserted in the input field. If left empty, only the bot's username will be inserted.

        allow_user_chats (``bool``, *optional*):
            True, if private chats with users can be chosen.

        allow_bot_chats (``bool``, *optional*):
            True, if private chats with bots can be chosen.

        allow_group_chats (``bool``, *optional*):
            True, if group and supergroup chats can be chosen.

        allow_channel_chats (``bool``, *optional*):
            True, if channel chats can be chosen.
    """

    def __init__(
        self,
        *,
        query: str | None = None,
        allow_user_chats: bool | None = None,
        allow_bot_chats: bool | None = None,
        allow_group_chats: bool | None = None,
        allow_channel_chats: bool | None = None,
    ):
        super().__init__()

        self.query = query
        self.allow_user_chats = allow_user_chats
        self.allow_bot_chats = allow_bot_chats
        self.allow_group_chats = allow_group_chats
        self.allow_channel_chats = allow_channel_chats

    @staticmethod
    def read(
        button_type: raw.types.InlineButtonTypeSwitchInline,
    ) -> SwitchInlineQueryChosenChat:
        peer_types = button_type.peer_types or []

        allow_user_chats = any(
            isinstance(p, raw.types.InlineQueryPeerTypePM) for p in peer_types
        )
        allow_bot_chats = any(
            isinstance(p, raw.types.InlineQueryPeerTypeBotPM) for p in peer_types
        )
        allow_group_chats = any(
            isinstance(
                p,
                (
                    raw.types.InlineQueryPeerTypeChat,
                    raw.types.InlineQueryPeerTypeMegagroup,
                ),
            )
            for p in peer_types
        )
        allow_channel_chats = any(
            isinstance(p, raw.types.InlineQueryPeerTypeBroadcast) for p in peer_types
        )

        return SwitchInlineQueryChosenChat(
            query=button_type.query,
            allow_user_chats=allow_user_chats or None,
            allow_bot_chats=allow_bot_chats or None,
            allow_group_chats=allow_group_chats or None,
            allow_channel_chats=allow_channel_chats or None,
        )

    async def write(self) -> raw.types.InlineButtonTypeSwitchInline:
        peer_types = []

        if self.allow_user_chats:
            peer_types.append(raw.types.InlineQueryPeerTypePM())

        if self.allow_bot_chats:
            peer_types.append(raw.types.InlineQueryPeerTypeBotPM())

        if self.allow_group_chats:
            peer_types.append(raw.types.InlineQueryPeerTypeChat())

        if self.allow_channel_chats:
            peer_types.append(raw.types.InlineQueryPeerTypeBroadcast())

        return raw.types.InlineButtonTypeSwitchInline(
            query=self.query or "",
            peer_types=peer_types,
        )
