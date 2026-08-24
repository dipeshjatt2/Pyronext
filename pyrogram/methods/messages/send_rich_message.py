from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import enums, raw, types, utils

if TYPE_CHECKING:
    from datetime import datetime


class SendRichMessage:
    async def send_rich_message(
        self: pyrogram.Client,
        chat_id: int | str,
        rich_text: str | types.InputRichMessage,
        parse_mode: enums.ParseMode | None = None,
        media: list[types.InputRichMessageMedia] | None = None,
        disable_web_page_preview: bool | None = None,
        disable_notification: bool | None = None,
        message_thread_id: int | None = None,
        reply_to_message_id: int | None = None,
        reply_to_chat_id: int | str | None = None,
        quote_text: str | None = None,
        quote_entities: list[types.MessageEntity] | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        invert_media: bool | None = None,
        message_effect_id: int | None = None,
        send_as: int | str | None = None,
        background: bool | None = None,
        clear_draft: bool | None = None,
        reply_markup: types.InlineKeyboardMarkup
        | types.ReplyKeyboardMarkup
        | types.ReplyKeyboardRemove
        | types.ForceReply
        | None = None,
        business_connection_id: str | None = None,
    ) -> types.Message | None:
        """Send a rich formatted message.

        Rich messages support structured content — headings, paragraphs, lists, tables,
        quotations, collapsible details, embedded media and even buttons inside the
        message body itself.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

            rich_text (``str`` | :obj:`~pyrogram.types.InputRichMessage`):
                Rich text (HTML or Markdown) describing the message, or a whole
                :obj:`~pyrogram.types.InputRichMessage` built from
                :obj:`~pyrogram.types.InputRichBlock` blocks for full control.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                Parse mode for *rich_text*. Defaults to HTML.
                Ignored when *rich_text* is an :obj:`~pyrogram.types.InputRichMessage`.

            media (List of :obj:`~pyrogram.types.InputRichMessageMedia`, *optional*):
                Media referenced by the rich text through ``tg://photo?id=``,
                ``tg://video?id=`` or ``tg://audio?id=`` links.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_to_chat_id (``int`` | ``str``, *optional*):
                Unique identifier for the origin chat.

            quote_text (``str``, *optional*):
                Text to quote.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message.

            send_as (``int`` | ``str``, *optional*):
                Unique identifier of the chat or user to send the message on behalf of.

            background (``bool``, *optional*):
                Pass True to send the message in the background.

            clear_draft (``bool``, *optional*):
                Pass True to clear the draft.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options.

            business_connection_id (``str``, *optional*):
                Business connection identifier.
                for business bots only.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent rich message is returned.

        Example:
            .. code-block:: python

                # Send a rich formatted message from HTML
                await app.send_rich_message(
                    "me",
                    "<h1>Hello</h1><p>This is a <b>rich</b> message.</p>"
                )

                # Send a rich message built from blocks with an embedded button row
                from pyrogram.types import (
                    InputRichMessage, InputRichBlockParagraph, InputRichBlockButtonRow,
                    InlineKeyboardButton,
                )

                await app.send_rich_message(
                    "me",
                    InputRichMessage(
                        blocks=[
                            InputRichBlockParagraph("Pick one:"),
                            InputRichBlockButtonRow(
                                [InlineKeyboardButton("Go", url="https://example.com")]
                            ),
                        ]
                    ),
                )
        """
        if isinstance(rich_text, types.InputRichMessage):
            rich_message_rpc = rich_text.write()
        else:
            files = (
                types.InputRichMessage(html="_", media=media).write_files()
                if media
                else None
            )

            if parse_mode == enums.ParseMode.MARKDOWN:
                rich_message_rpc = raw.types.InputRichMessageMarkdown(
                    markdown=rich_text,
                    files=files,
                )
            else:
                rich_message_rpc = raw.types.InputRichMessageHTML(
                    html=rich_text,
                    files=files,
                )

        rpc = raw.functions.messages.SendMessage(
            peer=utils.get_input_peer(await self.resolve_peer(chat_id)),
            no_webpage=disable_web_page_preview or None,
            silent=disable_notification or None,
            random_id=self.rnd_id(),
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            message="",
            rich_message=rich_message_rpc,
            noforwards=protect_content,
            invert_media=invert_media,
            effect=message_effect_id,
            background=background,
            clear_draft=clear_draft,
            send_as=utils.get_input_peer(await self.resolve_peer(send_as))
            if send_as
            else None,
            reply_to=await utils.get_reply_to(
                client=self,
                chat_id=chat_id,
                reply_to_message_id=reply_to_message_id,
                message_thread_id=message_thread_id,
                reply_to_chat_id=reply_to_chat_id,
                quote_text=quote_text,
                quote_entities=quote_entities,
            ),
        )
        if business_connection_id is not None:
            r = await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    connection_id=business_connection_id,
                    query=rpc,
                ),
            )
        else:
            r = await self.invoke(rpc)

        if isinstance(r, raw.types.UpdateShortSentMessage):
            peer = await self.resolve_peer(chat_id)

            peer_id = (
                peer.user_id
                if isinstance(peer, raw.types.InputPeerUser)
                else -peer.chat_id
            )

            return types.Message(
                id=r.id,
                chat=types.Chat(
                    id=peer_id,
                    type=enums.ChatType.PRIVATE,
                    client=self,
                ),
                date=utils.timestamp_to_datetime(r.date),
                outgoing=r.out,
                client=self,
            )

        for i in r.updates:
            if isinstance(
                i,
                raw.types.UpdateNewMessage
                | raw.types.UpdateNewChannelMessage
                | raw.types.UpdateNewScheduledMessage,
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {u.id: u for u in r.users},
                    {c.id: c for c in r.chats},
                )
        return None
