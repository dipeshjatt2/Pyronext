from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class RichMessage(Object):
    """Rich formatted message.

    This object represents the new rich text revolution: a full structured document
    (headings, lists, tables, quotes, embedded media and buttons) delivered as a message.

    Parameters:
        blocks (List of :obj:`~pyrogram.types.RichBlock`):
            Content of the message.

        is_rtl (``bool``, *optional*):
            True, if the rich message must be shown right-to-left.
    """

    def __init__(
        self,
        *,
        blocks: list[types.RichBlock],
        is_rtl: bool | None = None,
    ):
        super().__init__()

        self.blocks = blocks
        self.is_rtl = is_rtl

    @staticmethod
    async def _parse(
        client: pyrogram.Client,
        rich_message: raw.base.RichMessage,
        users: dict[int, raw.base.User] | None = None,
        chats: dict[int, raw.base.Chat] | None = None,
    ) -> RichMessage:
        if chats is None:
            chats = {}
        if users is None:
            users = {}
        photos = {photo.id: photo for photo in rich_message.photos}
        documents = {document.id: document for document in rich_message.documents}

        return RichMessage(
            blocks=types.List(
                [
                    await types.RichBlock._parse(
                        client,
                        block,
                        photos,
                        documents,
                        users,
                        chats,
                    )
                    for block in rich_message.blocks
                ]
            ),
            is_rtl=rich_message.rtl,
        )
