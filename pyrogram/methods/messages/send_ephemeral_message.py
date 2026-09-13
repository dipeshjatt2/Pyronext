from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types, utils


class SendEphemeralMessage:
    async def send_ephemeral_message(
        self: pyrogram.Client,
        chat_id: int | str,
        text: str,
        user_id: int | str | None = None,
        parse_mode: enums.ParseMode | None = None,
        entities: list[types.MessageEntity] | None = None,
        reply_to_message_id: int | None = None,
        reply_markup: types.ReplyMarkup = None,
    ) -> types.Message | None:
        """Send an ephemeral message to a chat/user (visible only to them)."""

        parsed_text = await utils.parse_text_entities(self, text, parse_mode, entities)
        message = parsed_text["message"]
        entities = parsed_text["entities"]

        if user_id is None:
            user_id = chat_id

        receiver = await self.resolve_peer(user_id)
        if not isinstance(receiver, raw.types.InputPeerUser):
            # Try to cast/convert, but typically ephemeral messages target a user
            pass

        peer = utils.get_input_peer(await self.resolve_peer(chat_id))
        receiver_user = utils.get_input_user(receiver)

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
        )

        rpc = raw.functions.ephemeral.SendMessage(
            receiver_id=receiver_user,
            peer=peer,
            message=message,
            random_id=self.rnd_id(),
            entities=entities,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            reply_to=reply_to
        )

        r = await self.invoke(rpc)

        for i in getattr(r, "updates", []):
            if isinstance(i, raw.types.UpdateNewEphemeralMessage):
                return await types.Message._parse(
                    self,
                    i.message,
                    {u.id: u for u in r.users},
                    {c.id: c for c in r.chats},
                )
        return None
