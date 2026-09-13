from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types, utils


class EditEphemeralMessageText:
    async def edit_ephemeral_message_text(
        self: pyrogram.Client,
        chat_id: int | str,
        receiver_user_id: int | str,
        ephemeral_message_id: int,
        text: str | None = None,
        parse_mode: enums.ParseMode | None = None,
        entities: list[types.MessageEntity] | None = None,
        rich_message: types.InputRichMessage | None = None,
        link_preview_options: types.LinkPreviewOptions | None = None,
        reply_markup: types.InlineKeyboardMarkup | None = None,
    ) -> types.Message | None:
        """Use this method to edit an ephemeral text message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            receiver_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to edit.

            text (``str``):
                New text of the message, 1-4096 characters after entity parsing.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.

            entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in message text.

            rich_message (:obj:`~pyrogram.types.InputRichMessage`, *optional*):
                New rich content of the message.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Options used for link preview generation for the message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~pyrogram.types.Message` | ``None``: On success, the edited message is returned.
        """
        link_preview_options = link_preview_options or getattr(
            self, "link_preview_options", None
        )

        parsed_text = await utils.parse_text_entities(
            self, text, parse_mode, entities
        )
        message = parsed_text["message"]
        entities = parsed_text["entities"]

        media = None
        if link_preview_options and link_preview_options.url:
            media = raw.types.InputMediaWebPage(
                url=link_preview_options.url,
                force_large_media=link_preview_options.prefer_large_media,
                force_small_media=link_preview_options.prefer_small_media,
                optional=True,
            )

        r = await self.invoke(
            raw.functions.ephemeral.EditMessage(
                peer=utils.get_input_peer(await self.resolve_peer(chat_id)),
                receiver_id=utils.get_input_user(
                    await self.resolve_peer(receiver_user_id)
                ),
                id=ephemeral_message_id,
                invert_media=getattr(link_preview_options, "show_above_text", None),
                reply_markup=await reply_markup.write(self)
                if reply_markup
                else None,
                message=message,
                rich_message=rich_message.write() if rich_message else None,
                media=media,
                entities=entities,
            )
        )

        messages = await utils.parse_messages(client=self, messages=r)

        return messages[0] if messages else None
