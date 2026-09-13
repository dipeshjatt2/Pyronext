from __future__ import annotations

import pyrogram
from pyrogram import raw, types, utils


class EditEphemeralMessageReplyMarkup:
    async def edit_ephemeral_message_reply_markup(
        self: pyrogram.Client,
        chat_id: int | str,
        receiver_user_id: int | str,
        ephemeral_message_id: int,
        reply_markup: types.InlineKeyboardMarkup | None = None,
    ) -> types.Message | None:
        """Use this method to edit only the reply markup of an ephemeral message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            receiver_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to edit.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`~pyrogram.types.Message` | ``None``: On success, the edited message is returned.
        """
        r = await self.invoke(
            raw.functions.ephemeral.EditMessage(
                peer=utils.get_input_peer(await self.resolve_peer(chat_id)),
                receiver_id=utils.get_input_user(
                    await self.resolve_peer(receiver_user_id)
                ),
                id=ephemeral_message_id,
                reply_markup=await reply_markup.write(self)
                if reply_markup
                else None,
            )
        )

        messages = await utils.parse_messages(client=self, messages=r)

        return messages[0] if messages else None
