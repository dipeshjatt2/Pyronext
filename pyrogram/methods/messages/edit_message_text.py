from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types, utils


class EditMessageText:
    async def edit_message_text(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        text: str,
        parse_mode: enums.ParseMode | None = None,
        entities: list[types.MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        invert_media: bool | None = None,
        reply_markup: types.InlineKeyboardMarkup | None = None,
        business_connection_id: str | None = None,
        rich_message: str | types.InputRichMessage | None = None,
        rich_message_media: types.InputRichMessageMedia
        | list[types.InputRichMessageMedia]
        | None = None,
    ) -> types.Message | None:
        """Edit the text of messages.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            text (``str``):
                New text of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.
                for business bots only.

            rich_message (``str`` | :obj:`~pyrogram.types.InputRichMessage`, *optional*):
                Edit the message into a rich formatted message.
                Pass a string with HTML or Markdown content, or an
                :obj:`~pyrogram.types.InputRichMessage` for full control.

            rich_message_media (:obj:`~pyrogram.types.InputRichMessageMedia` | List of :obj:`~pyrogram.types.InputRichMessageMedia`, *optional*):
                Media referenced by the rich message.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the edited message is returned.

        Example:
            .. code-block:: python

                # Simple edit text
                await app.edit_message_text(chat_id, message_id, "new text")

                # Take the same text message, remove the web page preview only
                await app.edit_message_text(
                    chat_id, message_id, message.text,
                    disable_web_page_preview=True)
        """

        text_params = await utils.parse_text_entities(
            self, text, parse_mode, entities
        )

        rich_message_rpc = None

        if rich_message is not None:
            if isinstance(rich_message, types.InputRichMessage):
                rich_message_rpc = rich_message.write()
            else:
                files = (
                    types.InputRichMessage(
                        html="_", media=rich_message_media
                    ).write_files()
                    if rich_message_media
                    else None
                )

                if parse_mode == enums.ParseMode.HTML:
                    rich_message_rpc = raw.types.InputRichMessageHTML(
                        html=rich_message,
                        files=files,
                    )
                else:
                    rich_message_rpc = raw.types.InputRichMessageMarkdown(
                        markdown=rich_message,
                        files=files,
                    )

        rpc = raw.functions.messages.EditMessage(
            peer=utils.get_input_peer(await self.resolve_peer(chat_id)),
            id=message_id,
            no_webpage=disable_web_page_preview or None,
            invert_media=invert_media,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            rich_message=rich_message_rpc,
            **text_params,
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

        for i in r.updates:
            if isinstance(
                i,
                raw.types.UpdateEditMessage | raw.types.UpdateEditChannelMessage,
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                )
        return None
