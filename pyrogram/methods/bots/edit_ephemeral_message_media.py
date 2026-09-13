from __future__ import annotations

import pyrogram
from pyrogram import raw, types, utils


class EditEphemeralMessageMedia:
    async def edit_ephemeral_message_media(
        self: pyrogram.Client,
        chat_id: int | str,
        receiver_user_id: int | str,
        ephemeral_message_id: int,
        media: types.InputMedia,
        reply_markup: types.InlineKeyboardMarkup | None = None,
    ) -> types.Message | None:
        """Use this method to edit the media of an ephemeral message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            receiver_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to edit.

            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~pyrogram.types.Message` | ``None``: On success, the edited message is returned.
        """
        caption = getattr(media, "caption", None)
        parse_mode = getattr(media, "parse_mode", None)
        caption_entities = getattr(media, "caption_entities", None)

        message, entities = None, None

        if caption is not None:
            parsed = await utils.parse_text_entities(
                self, caption, parse_mode, caption_entities
            )
            message = parsed["message"]
            entities = parsed["entities"]

        if not isinstance(
            media,
            (
                types.InputMediaPhoto,
                types.InputMediaVideo,
                types.InputMediaAudio,
                types.InputMediaAnimation,
                types.InputMediaDocument,
            ),
        ):
            raise ValueError(f"Unsupported media type {type(media)}")

        r = await self.invoke(
            raw.functions.ephemeral.EditMessage(
                peer=utils.get_input_peer(await self.resolve_peer(chat_id)),
                receiver_id=utils.get_input_user(
                    await self.resolve_peer(receiver_user_id)
                ),
                id=ephemeral_message_id,
                media=await media.write(client=self),
                reply_markup=await reply_markup.write(self)
                if reply_markup
                else None,
                message=message,
                entities=entities,
            )
        )

        messages = await utils.parse_messages(client=self, messages=r)

        return messages[0] if messages else None
