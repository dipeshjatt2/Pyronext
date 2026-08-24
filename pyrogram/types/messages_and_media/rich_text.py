from __future__ import annotations

from datetime import datetime
from typing import TypeAlias, Union

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object

RichTextContent: TypeAlias = Union[str, list["RichText"], "RichText"]


class RichText(Object):
    """This object represents a rich formatted text.

    It can be one of:

    - ``str``
    - List of :obj:`~pyrogram.types.RichText`
    - :obj:`~pyrogram.types.RichTextBold`
    - :obj:`~pyrogram.types.RichTextItalic`
    - :obj:`~pyrogram.types.RichTextUnderline`
    - :obj:`~pyrogram.types.RichTextStrikethrough`
    - :obj:`~pyrogram.types.RichTextSpoiler`
    - :obj:`~pyrogram.types.RichTextDateTime`
    - :obj:`~pyrogram.types.RichTextTextMention`
    - :obj:`~pyrogram.types.RichTextSubscript`
    - :obj:`~pyrogram.types.RichTextSuperscript`
    - :obj:`~pyrogram.types.RichTextMarked`
    - :obj:`~pyrogram.types.RichTextCode`
    - :obj:`~pyrogram.types.RichTextCustomEmoji`
    - :obj:`~pyrogram.types.RichTextMathematicalExpression`
    - :obj:`~pyrogram.types.RichTextUrl`
    - :obj:`~pyrogram.types.RichTextEmailAddress`
    - :obj:`~pyrogram.types.RichTextPhoneNumber`
    - :obj:`~pyrogram.types.RichTextBankCardNumber`
    - :obj:`~pyrogram.types.RichTextMention`
    - :obj:`~pyrogram.types.RichTextHashtag`
    - :obj:`~pyrogram.types.RichTextCashtag`
    - :obj:`~pyrogram.types.RichTextBotCommand`
    - :obj:`~pyrogram.types.RichTextAnchor`
    - :obj:`~pyrogram.types.RichTextAnchorLink`
    - :obj:`~pyrogram.types.RichTextReference`
    - :obj:`~pyrogram.types.RichTextImage`
    - :obj:`~pyrogram.types.RichTextButton`
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def _parse_button_type(
        button_type: raw.base.InlineButtonType,
        text: str,
    ) -> types.InlineKeyboardButton | None:
        """Convert a raw inline button type into a high-level InlineKeyboardButton."""
        if isinstance(button_type, raw.types.InlineButtonTypeCallback):
            try:
                data = button_type.data.decode()
            except UnicodeDecodeError:
                data = button_type.data

            return types.InlineKeyboardButton(
                text=text,
                callback_data=data,
                requires_password=button_type.requires_password,
            )

        if isinstance(button_type, raw.types.InlineButtonTypeUrl):
            return types.InlineKeyboardButton(text=text, url=button_type.url)

        if isinstance(
            button_type,
            raw.types.InlineButtonTypeUrlAuth
            | raw.types.InputInlineButtonTypeUrlAuth,
        ):
            return types.InlineKeyboardButton(
                text=text,
                login_url=types.LoginUrl.read(button_type),
            )

        if isinstance(
            button_type,
            raw.types.InlineButtonTypeUserProfile
            | raw.types.InputInlineButtonTypeUserProfile,
        ):
            user_id = button_type.user_id

            return types.InlineKeyboardButton(
                text=text,
                user_id=user_id if isinstance(user_id, int) else None,
            )

        if isinstance(button_type, raw.types.InlineButtonTypeSwitchInline):
            if button_type.same_peer:
                return types.InlineKeyboardButton(
                    text=text,
                    switch_inline_query_current_chat=button_type.query,
                )
            return types.InlineKeyboardButton(
                text=text, switch_inline_query=button_type.query
            )

        if isinstance(button_type, raw.types.InlineButtonTypeGame):
            return types.InlineKeyboardButton(
                text=text, callback_game=types.CallbackGame()
            )

        if isinstance(button_type, raw.types.InlineButtonTypeWebView):
            return types.InlineKeyboardButton(
                text=text,
                web_app=types.WebAppInfo(url=button_type.url),
            )

        if isinstance(button_type, raw.types.InlineButtonTypeCopy):
            return types.InlineKeyboardButton(
                text=text, copy_text=button_type.copy_text
            )

        return None

    @staticmethod
    async def _parse(
        client: pyrogram.Client,
        rich_text: raw.base.RichText,
        users: dict[int, raw.base.User] | None = None,
        chats: dict[int, raw.base.Chat] | None = None,
    ) -> RichTextContent | None:
        if chats is None:
            chats = {}
        if users is None:
            users = {}
        if isinstance(rich_text, raw.types.TextPlain):
            return rich_text.text

        if isinstance(rich_text, raw.types.TextConcat):
            return types.List(
                [await RichText._parse(client, t) for t in rich_text.texts]
            )

        if isinstance(rich_text, raw.types.TextBold):
            return RichTextBold(text=await RichText._parse(client, rich_text.text))

        if isinstance(rich_text, raw.types.TextItalic):
            return RichTextItalic(text=await RichText._parse(client, rich_text.text))

        if isinstance(rich_text, raw.types.TextUnderline):
            return RichTextUnderline(
                text=await RichText._parse(client, rich_text.text)
            )

        if isinstance(rich_text, raw.types.TextStrike):
            return RichTextStrikethrough(
                text=await RichText._parse(client, rich_text.text)
            )

        if isinstance(rich_text, raw.types.TextSpoiler):
            return RichTextSpoiler(
                text=await RichText._parse(client, rich_text.text)
            )

        if isinstance(rich_text, raw.types.TextDate):
            if rich_text.relative:
                date_time_format = "r"
            else:
                date_time_format = ""

                if rich_text.day_of_week:
                    date_time_format += "w"

                if rich_text.short_date:
                    date_time_format += "d"
                elif rich_text.long_date:
                    date_time_format += "D"

                if rich_text.short_time:
                    date_time_format += "t"
                elif rich_text.long_time:
                    date_time_format += "T"

            return RichTextDateTime(
                text=await RichText._parse(client, rich_text.text),
                date=utils.timestamp_to_datetime(rich_text.date),
                date_time_format=date_time_format or None,
            )

        if isinstance(rich_text, raw.types.TextMentionName):
            return RichTextTextMention(
                text=await RichText._parse(client, rich_text.text),
                user=types.User._parse(client, users.get(rich_text.user_id)),
            )

        if isinstance(rich_text, raw.types.TextSubscript):
            return RichTextSubscript(
                text=await RichText._parse(client, rich_text.text)
            )

        if isinstance(rich_text, raw.types.TextSuperscript):
            return RichTextSuperscript(
                text=await RichText._parse(client, rich_text.text)
            )

        if isinstance(rich_text, raw.types.TextMarked):
            return RichTextMarked(text=await RichText._parse(client, rich_text.text))

        if isinstance(rich_text, raw.types.TextFixed):
            return RichTextCode(text=await RichText._parse(client, rich_text.text))

        if isinstance(rich_text, raw.types.TextCustomEmoji):
            return RichTextCustomEmoji(
                custom_emoji_id=str(rich_text.document_id),
                alternative_text=rich_text.alt,
            )

        if isinstance(rich_text, raw.types.TextMath):
            return RichTextMathematicalExpression(expression=rich_text.source)

        if isinstance(rich_text, raw.types.TextUrl):
            content = await RichText._parse(client, rich_text.text)

            if rich_text.url.startswith("#"):
                anchor = rich_text.url[1:]

                return RichTextAnchorLink(text=content, anchor_name=anchor)

            return RichTextUrl(text=content, url=rich_text.url)

        if isinstance(rich_text, raw.types.TextAutoUrl):
            content = await RichText._parse(client, rich_text.text)

            return RichTextUrl(
                text=content,
                url="".join(_flatten_plain(content)),
            )

        if isinstance(rich_text, raw.types.TextEmail):
            return RichTextEmailAddress(
                text=await RichText._parse(client, rich_text.text),
                email_address=rich_text.email,
            )

        if isinstance(rich_text, raw.types.TextAutoEmail):
            content = await RichText._parse(client, rich_text.text)

            return RichTextEmailAddress(
                text=content,
                email_address="".join(_flatten_plain(content)),
            )

        if isinstance(rich_text, raw.types.TextPhone):
            return RichTextPhoneNumber(
                text=await RichText._parse(client, rich_text.text),
                phone_number=rich_text.phone,
            )

        if isinstance(rich_text, raw.types.TextAutoPhone):
            content = await RichText._parse(client, rich_text.text)

            return RichTextPhoneNumber(
                text=content,
                phone_number="".join(_flatten_plain(content)),
            )

        if isinstance(rich_text, raw.types.TextBankCard):
            content = await RichText._parse(client, rich_text.text)

            return RichTextBankCardNumber(
                text=content,
                bank_card_number="".join(_flatten_plain(content)),
            )

        if isinstance(rich_text, raw.types.TextMention):
            content = await RichText._parse(client, rich_text.text)

            return RichTextMention(
                text=content,
                username="".join(_flatten_plain(content)).lstrip("@"),
            )

        if isinstance(rich_text, raw.types.TextHashtag):
            content = await RichText._parse(client, rich_text.text)

            return RichTextHashtag(
                text=content,
                hashtag="".join(_flatten_plain(content)).lstrip("#"),
            )

        if isinstance(rich_text, raw.types.TextCashtag):
            content = await RichText._parse(client, rich_text.text)

            return RichTextCashtag(
                text=content,
                cashtag="".join(_flatten_plain(content)).lstrip("$"),
            )

        if isinstance(rich_text, raw.types.TextBotCommand):
            content = await RichText._parse(client, rich_text.text)

            return RichTextBotCommand(
                text=content,
                bot_command="".join(_flatten_plain(content)).lstrip("/"),
            )

        if isinstance(rich_text, raw.types.TextAnchor):
            if isinstance(rich_text.text, raw.types.TextEmpty):
                return RichTextAnchor(
                    text=await RichText._parse(client, rich_text.text),
                    name=rich_text.name,
                )

            return RichTextReference(
                text=await RichText._parse(client, rich_text.text),
                name=rich_text.name,
            )

        if isinstance(rich_text, raw.types.TextImage):
            return RichTextImage(
                document_id=rich_text.document_id,
                width=rich_text.w,
                height=rich_text.h,
            )

        if isinstance(rich_text, raw.types.TextDiff):
            return RichTextDiff(
                text=await RichText._parse(client, rich_text.text),
                old_text=await RichText._parse(client, rich_text.old_text),
            )

        if isinstance(rich_text, raw.types.TextButton):
            content = await RichText._parse(client, rich_text.text)
            plain = "".join(_flatten_plain(content))
            button = RichText._parse_button_type(rich_text.type, plain)

            return RichTextButton(
                text=content,
                button=button,
                style=types.RichButtonStyle.read(rich_text.style),
            )
        return None


class RichTextBold(RichText):
    """A bold text.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextItalic(RichText):
    """A italicized text.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextUnderline(RichText):
    """A underlined text.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextStrikethrough(RichText):
    """A strikethrough text.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextSpoiler(RichText):
    """A text covered by a spoiler.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextDateTime(RichText):
    """Formatted date and time.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        date (:py:obj:`datetime.datetime`):
            The date associated with the entity.

        date_time_format (``str``, *optional*):
            The string that defines the formatting of the date and time.
    """

    def __init__(
        self,
        text: RichTextContent | None,
        date: datetime,
        date_time_format: str | None = None,
    ):
        super().__init__()

        self.text = text
        self.date = date
        self.date_time_format = date_time_format


class RichTextTextMention(RichText):
    """A mention of a Telegram user by their identifier.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        user (:obj:`~pyrogram.types.User`):
            The mentioned user.
    """

    def __init__(self, text: RichTextContent | None, user: types.User | None):
        super().__init__()

        self.text = text
        self.user = user


class RichTextSubscript(RichText):
    """A subscript text.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextSuperscript(RichText):
    """A superscript text.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextMarked(RichText):
    """A marked text.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextCode(RichText):
    """A monowidth text.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.
    """

    def __init__(self, text: RichTextContent | None):
        super().__init__()

        self.text = text


class RichTextCustomEmoji(RichText):
    """A custom emoji.

    Parameters:
        custom_emoji_id (``str``):
            Unique identifier of the custom emoji.
            Use :meth:`~pyrogram.Client.get_custom_emoji_stickers` to get full information about the sticker.

        alternative_text (``str``):
            Alternative emoji for the custom emoji.
    """

    def __init__(self, custom_emoji_id: str, alternative_text: str):
        super().__init__()

        self.custom_emoji_id = custom_emoji_id
        self.alternative_text = alternative_text


class RichTextMathematicalExpression(RichText):
    """A mathematical expression.

    Parameters:
        expression (``str``):
            The expression in LaTeX format.
    """

    def __init__(self, expression: str):
        super().__init__()

        self.expression = expression


class RichTextUrl(RichText):
    """A text with a link.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        url (``str``):
            URL of the link.
    """

    def __init__(self, text: RichTextContent | None, url: str):
        super().__init__()

        self.text = text
        self.url = url


class RichTextEmailAddress(RichText):
    """A text with an email address.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        email_address (``str``):
            The email address.
    """

    def __init__(self, text: RichTextContent | None, email_address: str):
        super().__init__()

        self.text = text
        self.email_address = email_address


class RichTextPhoneNumber(RichText):
    """A text with a phone number.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        phone_number (``str``):
            The phone number.
    """

    def __init__(self, text: RichTextContent | None, phone_number: str):
        super().__init__()

        self.text = text
        self.phone_number = phone_number


class RichTextBankCardNumber(RichText):
    """A text with a bank card number.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        bank_card_number (``str``):
            The bank card number.
    """

    def __init__(self, text: RichTextContent | None, bank_card_number: str):
        super().__init__()

        self.text = text
        self.bank_card_number = bank_card_number


class RichTextMention(RichText):
    """A mention by a username.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        username (``str``):
            The username.
    """

    def __init__(self, text: RichTextContent | None, username: str):
        super().__init__()

        self.text = text
        self.username = username


class RichTextHashtag(RichText):
    """A hashtag.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        hashtag (``str``):
            The hashtag.
    """

    def __init__(self, text: RichTextContent | None, hashtag: str):
        super().__init__()

        self.text = text
        self.hashtag = hashtag


class RichTextCashtag(RichText):
    """A cashtag.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        cashtag (``str``):
            The cashtag.
    """

    def __init__(self, text: RichTextContent | None, cashtag: str):
        super().__init__()

        self.text = text
        self.cashtag = cashtag


class RichTextBotCommand(RichText):
    """A bot command.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        bot_command (``str``):
            The bot command.
    """

    def __init__(self, text: RichTextContent | None, bot_command: str):
        super().__init__()

        self.text = text
        self.bot_command = bot_command


class RichTextAnchor(RichText):
    """An anchor.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        name (``str``):
            The name of the anchor.
    """

    def __init__(self, text: RichTextContent | None, name: str):
        super().__init__()

        self.text = text
        self.name = name


class RichTextAnchorLink(RichText):
    """A link to an anchor.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        anchor_name (``str``):
            The name of the anchor.
            If the name is empty, then the link brings back to the top of the message.
    """

    def __init__(self, text: RichTextContent | None, anchor_name: str):
        super().__init__()

        self.text = text
        self.anchor_name = anchor_name


class RichTextReference(RichText):
    """A reference.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        name (``str``):
            The name of the reference.
    """

    def __init__(self, text: RichTextContent | None, name: str):
        super().__init__()

        self.text = text
        self.name = name


class RichTextReferenceLink(RichText):
    """A link to a reference.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The text.

        reference_name (``str``):
            The name of the reference.
    """

    def __init__(self, text: RichTextContent | None, reference_name: str):
        super().__init__()

        self.text = text
        self.reference_name = reference_name


class RichTextImage(RichText):
    """An inline image.

    Parameters:
        document_id (``int``):
            Unique identifier of the photo document.

        width (``int``):
            Width of the image.

        height (``int``):
            Height of the image.
    """

    def __init__(self, document_id: int, width: int, height: int):
        super().__init__()

        self.document_id = document_id
        self.width = width
        self.height = height


class RichTextDiff(RichText):
    """A diff text, representing the difference between a text and its previous version.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The new text.

        old_text (:obj:`~pyrogram.types.RichText`):
            The previous version of the text.
    """

    def __init__(
        self, text: RichTextContent | None, old_text: RichTextContent | None
    ):
        super().__init__()

        self.text = text
        self.old_text = old_text


class RichTextButton(RichText):
    """A button embedded in rich text.

    This is the revolutionary way to attach buttons directly inside formatted message text,
    instead of only via reply markup.

    Parameters:
        text (:obj:`~pyrogram.types.RichText`):
            The button label text.

        button (:obj:`~pyrogram.types.InlineKeyboardButton`, *optional*):
            The embedded inline keyboard button.

        style (:obj:`~pyrogram.types.RichButtonStyle`, *optional*):
            Style of the embedded button.
    """

    def __init__(
        self,
        text: RichTextContent | None,
        button: types.InlineKeyboardButton | None = None,
        style: types.RichButtonStyle | None = None,
    ):
        super().__init__()

        self.text = text
        self.button = button
        self.style = style

    @staticmethod
    async def write_from(
        client: pyrogram.Client,
        button: types.InlineKeyboardButton,
    ) -> raw.types.TextButton:
        """Build a raw TextButton from a high-level InlineKeyboardButton."""
        label = raw.types.TextPlain(text=str(button.text))

        if button.callback_data is not None:
            data = (
                button.callback_data.encode()
                if isinstance(button.callback_data, str)
                else button.callback_data
            )
            button_type = raw.types.InlineButtonTypeCallback(data=data)
        elif button.url is not None:
            button_type = raw.types.InlineButtonTypeUrl(url=button.url)
        elif button.login_url is not None:
            button_type = raw.types.InputInlineButtonTypeUrlAuth(
                url=button.login_url.url,
                fwd_text=button.login_url.forward_text,
                bot=utils.get_input_user(
                    await client.resolve_peer(
                        button.login_url.bot_username or "self"
                    )
                ),
            )
        elif button.switch_inline_query_current_chat is not None:
            button_type = raw.types.InlineButtonTypeSwitchInline(
                query=button.switch_inline_query_current_chat,
                same_peer=True,
            )
        elif button.switch_inline_query is not None:
            button_type = raw.types.InlineButtonTypeSwitchInline(
                query=button.switch_inline_query,
            )
        elif button.copy_text is not None:
            button_type = raw.types.InlineButtonTypeCopy(copy_text=button.copy_text)
        else:
            raise ValueError(
                "Rich text buttons support url/callback/switch_inline/copy only"
            )

        return raw.types.TextButton(
            text=label,
            type=button_type,
            style=types.RichButtonStyle.write_from(button.style),
        )


def _flatten_plain(rich_text) -> list[str]:
    """Extract all plain strings from parsed rich text for button labels."""
    if rich_text is None:
        return []
    if isinstance(rich_text, str):
        return [rich_text]
    if isinstance(rich_text, list):
        return [s for item in rich_text for s in _flatten_plain(item)]
    text = getattr(rich_text, "text", None)
    if text is not None and not isinstance(text, (int, datetime)):
        return _flatten_plain(text)
    return []
