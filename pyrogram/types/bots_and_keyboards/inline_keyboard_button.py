from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.types.object import Object


class InlineKeyboardButton(Object):
    """One button of an inline keyboard.

    You must use exactly one of the optional fields.

    Parameters:
        text (``str``):
            Label text on the button.

        callback_data (``str`` | ``bytes``, *optional*):
            Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes.

        url (``str``, *optional*):
            HTTP url to be opened when button is pressed.

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            Description of the `Web App <https://core.telegram.org/bots/webapps>`_ that will be launched when the user
            presses the button. The Web App will be able to send an arbitrary message on behalf of the user using the
            method :meth:`~pyrogram.Client.answer_web_app_query`. Available only in private chats between a user and the
            bot.

        login_url (:obj:`~pyrogram.types.LoginUrl`, *optional*):
             An HTTP URL used to automatically authorize the user. Can be used as a replacement for
             the `Telegram Login Widget <https://core.telegram.org/widgets/login>`_.

        user_id (``int``, *optional*):
            User id, for links to the user profile.

        switch_inline_query (``str``, *optional*):
            If set, pressing the button will prompt the user to select one of their chats, open that chat and insert
            the bot's username and the specified inline query in the input field. Can be empty, in which case just
            the bot's username will be inserted.Note: This offers an easy way for users to start using your bot in
            inline mode when they are currently in a private chat with it. Especially useful when combined with
            switch_pm… actions – in this case the user will be automatically returned to the chat they switched from,
            skipping the chat selection screen.

        switch_inline_query_current_chat (``str``, *optional*):
            If set, pressing the button will insert the bot's username and the specified inline query in the current
            chat's input field. Can be empty, in which case only the bot's username will be inserted.This offers a
            quick way for the user to open your bot in inline mode in the same chat – good for selecting something
            from multiple options.

        callback_game (:obj:`~pyrogram.types.CallbackGame`, *optional*):
            Description of the game that will be launched when the user presses the button.
            **NOTE**: This type of button **must** always be the first button in the first row.

        requires_password (``bool``, *optional*):
            A button that asks for the 2-step verification password of the current user and then sends a callback
            query to a bot. Data to be sent to the bot via a callback query.

        copy_text (``str``, *optional*):
            A button that copies the text to the clipboard.

        disabled (``bool``, *optional*):
            True, if the button is disabled and cannot be pressed.

        style (:obj:`~pyrogram.types.KeyboardButtonStyle` | :obj:`~pyrogram.enums.ButtonStyle`, *optional*):
            Button style.

        icon (``int``, *optional*):
            Custom icon for the button.
    """

    def __init__(
        self,
        text: str,
        callback_data: str | bytes | None = None,
        url: str | None = None,
        web_app: types.WebAppInfo | None = None,
        login_url: types.LoginUrl | None = None,
        user_id: int | None = None,
        switch_inline_query: str | None = None,
        switch_inline_query_current_chat: str | None = None,
        switch_inline_query_chosen_chat: types.SwitchInlineQueryChosenChat
        | None = None,
        callback_game: types.CallbackGame | None = None,
        requires_password: bool | None = None,
        copy_text: str | None = None,
        disabled: bool | None = None,
        style: types.KeyboardButtonStyle | enums.ButtonStyle | None = None,
        icon: int | None = None,
    ) -> None:
        super().__init__()

        self.text = str(text)
        self.callback_data = callback_data
        self.url = url
        self.web_app = web_app
        self.login_url = login_url
        self.user_id = user_id
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.switch_inline_query_chosen_chat = switch_inline_query_chosen_chat
        self.callback_game = callback_game
        self.requires_password = requires_password
        self.copy_text = copy_text
        self.disabled = disabled
        self.style = types.KeyboardButtonStyle._parse(style)

        if icon is not None:
            if self.style is None:
                self.style = types.KeyboardButtonStyle(icon=icon)
            else:
                self.style.icon = icon

    @staticmethod
    def read(
        b: raw.base.KeyboardInlineButton,
    ) -> types.InlineKeyboardButton | types.InlineKeyboardButtonBuy | None:
        style = types.KeyboardButtonStyle.read(getattr(b, "style", None))
        button_type = getattr(b, "type", None)

        if isinstance(button_type, raw.types.InlineButtonTypeCallback):
            # Try decode data to keep it as string, but if fails, fallback to bytes so we don't lose any information,
            # instead of decoding by ignoring/replacing errors.
            try:
                data = button_type.data.decode()
            except UnicodeDecodeError:
                data = button_type.data

            return InlineKeyboardButton(
                text=b.text,
                callback_data=data,
                requires_password=button_type.requires_password,
                style=style,
            )

        if isinstance(button_type, raw.types.InlineButtonTypeUrl):
            return InlineKeyboardButton(
                text=b.text, url=button_type.url, style=style
            )

        if isinstance(
            button_type,
            raw.types.InlineButtonTypeUrlAuth
            | raw.types.InputInlineButtonTypeUrlAuth,
        ):
            return InlineKeyboardButton(
                text=b.text,
                login_url=types.LoginUrl.read(button_type),
                style=style,
            )

        if isinstance(
            button_type,
            raw.types.InlineButtonTypeUserProfile
            | raw.types.InputInlineButtonTypeUserProfile,
        ):
            return InlineKeyboardButton(
                text=b.text, user_id=button_type.user_id, style=style
            )

        if isinstance(button_type, raw.types.InlineButtonTypeSwitchInline):
            if button_type.peer_types:
                return InlineKeyboardButton(
                    text=b.text,
                    switch_inline_query_chosen_chat=types.SwitchInlineQueryChosenChat.read(
                        button_type
                    ),
                    style=style,
                )
            if button_type.same_peer:
                return InlineKeyboardButton(
                    text=b.text,
                    switch_inline_query_current_chat=button_type.query,
                    style=style,
                )
            return InlineKeyboardButton(
                text=b.text,
                switch_inline_query=button_type.query,
                style=style,
            )

        if isinstance(button_type, raw.types.InlineButtonTypeGame):
            return InlineKeyboardButton(
                text=b.text,
                callback_game=types.CallbackGame(),
                style=style,
            )

        if isinstance(button_type, raw.types.InlineButtonTypeWebView):
            return InlineKeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(url=button_type.url),
                style=style,
            )

        if isinstance(button_type, raw.types.InlineButtonTypeCopy):
            return InlineKeyboardButton(
                text=b.text,
                copy_text=button_type.copy_text,
                style=style,
            )

        if isinstance(button_type, raw.types.InlineButtonTypeBuy):
            return types.InlineKeyboardButtonBuy.read(b)

        if isinstance(button_type, raw.types.InlineButtonTypeDisabled):
            return InlineKeyboardButton(text=b.text, disabled=True, style=style)

        return None

    async def write(
        self, client: pyrogram.Client
    ) -> raw.types.KeyboardInlineButton | None:
        style = self.style.write() if self.style else None

        if self.callback_data is not None:
            # Telegram only wants bytes, but we are allowed to pass strings too, for convenience.
            data = (
                bytes(self.callback_data, "utf-8")
                if isinstance(self.callback_data, str)
                else self.callback_data
            )

            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InlineButtonTypeCallback(
                    data=data,
                    requires_password=self.requires_password or None,
                ),
                style=style,
            )

        if self.url is not None:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InlineButtonTypeUrl(url=self.url),
                style=style,
            )

        if self.login_url is not None:
            button_type = await self.login_url.write(
                bot=utils.get_input_user(
                    await client.resolve_peer(self.login_url.bot_username or "self")
                ),
            )

            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=button_type,
                style=style,
            )

        if self.user_id is not None:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InputInlineButtonTypeUserProfile(
                    user_id=utils.get_input_user(
                        await client.resolve_peer(self.user_id)
                    ),
                ),
                style=style,
            )

        if self.switch_inline_query_chosen_chat is not None:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=await self.switch_inline_query_chosen_chat.write(),
                style=style,
            )

        if self.switch_inline_query is not None:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InlineButtonTypeSwitchInline(
                    query=self.switch_inline_query
                ),
                style=style,
            )

        if self.switch_inline_query_current_chat is not None:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InlineButtonTypeSwitchInline(
                    query=self.switch_inline_query_current_chat,
                    same_peer=True,
                ),
                style=style,
            )

        if self.callback_game is not None:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InlineButtonTypeGame(),
                style=style,
            )

        if self.web_app is not None:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InlineButtonTypeWebView(url=self.web_app.url),
                style=style,
            )

        if self.copy_text is not None:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InlineButtonTypeCopy(copy_text=self.copy_text),
                style=style,
            )

        if self.disabled:
            return raw.types.KeyboardInlineButton(
                text=self.text,
                type=raw.types.InlineButtonTypeDisabled(),
                style=style,
            )

        return None
