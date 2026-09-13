from __future__ import annotations

import pyrogram
from pyrogram import raw, utils


class DeleteEphemeralMessage:
    async def delete_ephemeral_message(
        self: pyrogram.Client,
        chat_id: int | str,
        receiver_user_id: int | str,
        ephemeral_message_id: int,
    ) -> bool:
        """Use this method to delete an ephemeral message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            receiver_user_id (``int`` | ``str``):
                Identifier (int) or username (str) of the user who received the message.

            ephemeral_message_id (``int``):
                Identifier of the ephemeral message to delete.

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self.invoke(
            raw.functions.ephemeral.DeleteMessage(
                peer=utils.get_input_peer(await self.resolve_peer(chat_id)),
                receiver_id=utils.get_input_user(
                    await self.resolve_peer(receiver_user_id)
                ),
                id=ephemeral_message_id,
            )
        )
