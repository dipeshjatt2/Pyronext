from __future__ import annotations

import pyrogram
from pyrogram import enums, types


class EditEphemeralMessageCaption:
    async def edit_ephemeral_message_caption(
        self: pyrogram.Client,
        chat_id: int | str,
        receiver_user_id: int | str,
        ephemeral_message_id: int,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        reply_markup: types.InlineKeyboardMarkup | None = None,
    ) -> types.Message | None:
        """Use this method to edit the caption of an ephemeral message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            receiver_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to edit.

            caption (``str``, *optional*):
                New caption of the message, 0-1024 characters after entities parsing.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in the caption.

            show_caption_above_media (``bool``, *optional*):
                Pass True if the caption must be shown above the message media.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~pyrogram.types.Message` | ``None``: On success, the edited message is returned.
        """
        link_preview = None
        if show_caption_above_media is not None and hasattr(
            types, "LinkPreviewOptions"
        ):
            link_preview = types.LinkPreviewOptions(
                show_above_text=show_caption_above_media
            )

        return await self.edit_ephemeral_message_text(
            chat_id=chat_id,
            receiver_user_id=receiver_user_id,
            ephemeral_message_id=ephemeral_message_id,
            text=caption,
            parse_mode=parse_mode,
            entities=caption_entities,
            link_preview_options=link_preview,
            reply_markup=reply_markup,
        )
