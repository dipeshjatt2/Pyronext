from __future__ import annotations

from typing import Literal

from pyrogram import raw
from pyrogram.types.object import Object


def _to_rich_text(text: str | raw.base.RichText) -> raw.base.RichText:
    if isinstance(text, str):
        return raw.types.TextConcat(texts=[raw.types.TextPlain(text=text)])
    return text


def _to_page_caption(
    text: str | raw.base.RichText | None = None,
    credit: str | raw.base.RichText | None = None,
) -> raw.types.PageCaption:
    return raw.types.PageCaption(
        text=_to_rich_text(text or ""),
        credit=_to_rich_text(credit or ""),
    )


class InputRichBlock(Object):
    """Base class for all input rich message blocks.

    Subclasses define specific block types that can be used to compose
    the content of a rich message. Each subclass implements a ``write()``
    method that produces the corresponding raw Telegram type.
    """

    def __init__(self):
        super().__init__()

    def write(self) -> raw.base.PageBlock:
        raise NotImplementedError


class InputRichBlockParagraph(InputRichBlock):
    """A paragraph block, corresponding to the HTML tag ``<p>``.

    Parameters:
        text (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Text of the block.
    """

    def __init__(
        self,
        text: str | raw.base.RichText,
    ):
        super().__init__()

        self.text = text

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockParagraph(text=_to_rich_text(self.text))


class InputRichBlockSectionHeading(InputRichBlock):
    """A section heading block, corresponding to the HTML tags ``<h1>`` through ``<h6>``.

    Parameters:
        text (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Text of the block.

        size (``int``):
            Relative size of the text font, 1-6.
            1 is the largest, 6 is the smallest.
    """

    def __init__(
        self,
        text: str | raw.base.RichText,
        size: int,
    ):
        super().__init__()

        self.text = text
        self.size = size

    def write(self) -> raw.base.PageBlock:
        mapping = {
            1: raw.types.PageBlockHeading1,
            2: raw.types.PageBlockHeading2,
            3: raw.types.PageBlockHeading3,
            4: raw.types.PageBlockHeading4,
            5: raw.types.PageBlockHeading5,
            6: raw.types.PageBlockHeading6,
        }
        cls = mapping.get(self.size)
        if cls is None:
            raise ValueError(f"Invalid heading size: {self.size}. Must be 1-6.")
        return cls(text=_to_rich_text(self.text))


class InputRichBlockPreformatted(InputRichBlock):
    """A preformatted text block, corresponding to the HTML tag ``<pre>``.

    Parameters:
        text (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Text of the block.

        language (``str``, *optional*):
            Language of the code block (e.g. ``python``, ``javascript``).
    """

    def __init__(
        self,
        text: str | raw.base.RichText,
        language: str | None = None,
    ):
        super().__init__()

        self.text = text
        self.language = language

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockPreformatted(
            text=_to_rich_text(self.text),
            language=self.language or "",
        )


class InputRichBlockFooter(InputRichBlock):
    """A footer block, corresponding to the HTML tag ``<footer>``.

    Parameters:
        text (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Text of the block.
    """

    def __init__(
        self,
        text: str | raw.base.RichText,
    ):
        super().__init__()

        self.text = text

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockFooter(text=_to_rich_text(self.text))


class InputRichBlockDivider(InputRichBlock):
    """A thematic break block, corresponding to the HTML tag ``<hr>``.

    This block has no content and simply draws a horizontal line.
    """

    def __init__(self):
        super().__init__()

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockDivider()


class InputRichBlockMathematicalExpression(InputRichBlock):
    """A mathematical expression block, corresponding to the HTML tag ``<math>``.

    Parameters:
        expression (``str``):
            The mathematical expression in TeX source format.
    """

    def __init__(
        self,
        expression: str,
    ):
        super().__init__()

        self.expression = expression

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockMath(source=self.expression)


class InputRichBlockAnchor(InputRichBlock):
    """An anchor block, corresponding to the HTML tag ``<a>`` with a ``name`` attribute.

    This block creates a named anchor point in the message that can be
    linked to from other parts of the message.

    Parameters:
        name (``str``):
            The anchor name.
    """

    def __init__(
        self,
        name: str,
    ):
        super().__init__()

        self.name = name

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockAnchor(name=self.name)


class InputRichBlockListItem(Object):
    """An item in a :class:`~pyrogram.types.InputRichBlockList`.

    A list item either contains a single text line or a collection of nested blocks.

    Parameters:
        blocks (List of :obj:`~pyrogram.types.InputRichBlock`, *optional*):
            Nested blocks that make up the list item content.
            Mutually exclusive with *text*.

        text (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Simple text content of the list item.
            Mutually exclusive with *blocks*.

        has_checkbox (``bool``, *optional*):
            Pass True if the item has a checkbox.

        is_checked (``bool``, *optional*):
            Pass True if the item has a checked checkbox.

        value (``int``, *optional*):
            For ordered lists, the numeric value of the item.
    """

    def __init__(
        self,
        blocks: list[InputRichBlock] | None = None,
        text: str | raw.base.RichText | None = None,
        has_checkbox: bool | None = None,
        is_checked: bool | None = None,
        value: int | None = None,
    ):
        super().__init__()

        if isinstance(blocks, str):
            blocks, text = None, blocks

        self.blocks = blocks
        self.text = text
        self.has_checkbox = has_checkbox
        self.is_checked = is_checked
        self.value = value

    def write_ordered(self) -> raw.types.PageListOrderedItem:
        if self.blocks:
            return raw.types.PageListOrderedItemBlocks(
                blocks=[b.write() for b in self.blocks],
                checkbox=self.has_checkbox,
                checked=self.is_checked,
                value=self.value,
            )
        return raw.types.PageListOrderedItemText(
            text=_to_rich_text(self.text or ""),
            checkbox=self.has_checkbox,
            checked=self.is_checked,
            value=self.value,
        )

    def write(self) -> raw.base.PageListItem:
        if self.blocks:
            return raw.types.PageListItemBlocks(
                blocks=[b.write() for b in self.blocks],
                checkbox=self.has_checkbox,
                checked=self.is_checked,
            )
        return raw.types.PageListItemText(
            text=_to_rich_text(self.text or ""),
            checkbox=self.has_checkbox,
            checked=self.is_checked,
        )


class InputRichBlockList(InputRichBlock):
    """A list block, corresponding to the HTML tags ``<ul>`` (unordered) or ``<ol>`` (ordered).

    Parameters:
        items (List of :obj:`~pyrogram.types.InputRichBlockListItem`):
            The items in the list.

        ordered (``bool``, *optional*):
            Pass *True* for an ordered (numbered) list, *False* or omit for an unordered list.

        reversed_ (``bool``, *optional*):
            For ordered lists, pass *True* to reverse the numbering.

        start (``int``, *optional*):
            For ordered lists, the starting value of the numbering.

        list_type (``str``, *optional*):
            For ordered lists, the label type: "a", "A", "i", "I" or "1".
    """

    def __init__(
        self,
        items: list[InputRichBlockListItem],
        ordered: bool | None = None,
        reversed_: bool | None = None,
        start: int | None = None,
        list_type: Literal["a", "A", "i", "I", "1"] | None = None,
    ):
        super().__init__()

        self.items = items
        self.ordered = ordered
        self.reversed_ = reversed_
        self.start = start
        self.list_type = list_type

    def write(self) -> raw.base.PageBlock:
        if self.ordered:
            return raw.types.PageBlockOrderedList(
                items=[item.write_ordered() for item in self.items],
                reversed=self.reversed_,
                start=self.start,
                type=self.list_type,
            )
        return raw.types.PageBlockList(items=[item.write() for item in self.items])


class InputRichBlockBlockQuotation(InputRichBlock):
    """A block quotation, corresponding to the HTML tag ``<blockquote>``.

    Parameters:
        blocks (List of :obj:`~pyrogram.types.InputRichBlock`):
            Blocks inside the block quotation.

        credit (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Credit or citation source of the block quotation,
            corresponding to the HTML tag ``<cite>``.

        collapsed (``bool``, *optional*):
            Pass *True* to collapse the quotation by default.
            Only used when a single paragraph-like *text* block is provided via
            :class:`~pyrogram.types.InputRichBlockPullQuotation` instead.
    """

    def __init__(
        self,
        blocks: list[InputRichBlock],
        credit: str | raw.base.RichText | None = None,
        collapsed: bool | None = None,
    ):
        super().__init__()

        self.blocks = blocks
        self.credit = credit
        self.collapsed = collapsed

    def write(self) -> raw.base.PageBlock:
        if (
            len(self.blocks) == 1
            and isinstance(self.blocks[0], InputRichBlockParagraph)
            and not self.credit
        ):
            paragraph = self.blocks[0].write()

            if isinstance(paragraph, raw.types.PageBlockParagraph):
                return raw.types.PageBlockBlockquote(
                    text=paragraph.text,
                    caption=raw.types.TextEmpty(),
                    collapsed=self.collapsed,
                )

        return raw.types.PageBlockBlockquoteBlocks(
            blocks=[b.write() for b in self.blocks],
            caption=_to_rich_text(self.credit or ""),
        )


class InputRichBlockPullQuotation(InputRichBlock):
    """A pull quotation block, corresponding to the HTML tag ``<pullquote>``.

    Parameters:
        text (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Text of the pull quotation.

        credit (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Credit or citation source of the pull quotation,
            corresponding to the HTML tag ``<cite>``.
    """

    def __init__(
        self,
        text: str | raw.base.RichText,
        credit: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.text = text
        self.credit = credit

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockPullquote(
            text=_to_rich_text(self.text),
            caption=_to_rich_text(self.credit or ""),
        )


class InputRichBlockCollage(InputRichBlock):
    """A collage block, corresponding to the HTML tag ``<collage>``.

    Displays a set of media blocks in a grid layout.

    Parameters:
        items (List of :obj:`~pyrogram.types.InputRichBlock`):
            Media blocks in the collage (typically :class:`~pyrogram.types.InputRichBlockPhoto`,
            :class:`~pyrogram.types.InputRichBlockVideo`, etc.).

        caption (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Caption of the collage.
    """

    def __init__(
        self,
        items: list[InputRichBlock],
        caption: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.items = items
        self.caption = caption

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockCollage(
            items=[item.write() for item in self.items],
            caption=_to_page_caption(text=self.caption),
        )


class InputRichBlockSlideshow(InputRichBlock):
    """A slideshow block, corresponding to the HTML tag ``<slideshow>``.

    Displays a set of media blocks in a slideshow/carousel layout.

    Parameters:
        items (List of :obj:`~pyrogram.types.InputRichBlock`):
            Media blocks in the slideshow (typically :class:`~pyrogram.types.InputRichBlockPhoto`,
            :class:`~pyrogram.types.InputRichBlockVideo`, etc.).

        caption (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Caption of the slideshow.
    """

    def __init__(
        self,
        items: list[InputRichBlock],
        caption: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.items = items
        self.caption = caption

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockSlideshow(
            items=[item.write() for item in self.items],
            caption=_to_page_caption(text=self.caption),
        )


class InputRichBlockTable(InputRichBlock):
    """A table block, corresponding to the HTML tag ``<table>``.

    Parameters:
        title (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Title of the table, corresponding to the HTML tag ``<caption>``.

        rows (List of List of :obj:`~pyrogram.types.InputRichBlockTableCell`):
            Rows of the table. Each row is a list of cell objects.

        bordered (``bool``, *optional*):
            Pass *True* to display the table with a border.

        striped (``bool``, *optional*):
            Pass *True* to display the table with alternating row colors.
    """

    def __init__(
        self,
        title: str | raw.base.RichText,
        rows: list[list[InputRichBlockTableCell]],
        bordered: bool | None = None,
        striped: bool | None = None,
    ):
        super().__init__()

        self.title = title
        self.rows = rows
        self.bordered = bordered
        self.striped = striped

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockTable(
            title=_to_rich_text(self.title),
            rows=[
                raw.types.PageTableRow(cells=[cell.write() for cell in row])
                for row in self.rows
            ],
            bordered=self.bordered,
            striped=self.striped,
        )


class InputRichBlockTableCell(Object):
    """A cell in a table row (used with :class:`~pyrogram.types.InputRichBlockTable`).

    Parameters:
        text (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Text content of the cell.

        header (``bool``, *optional*):
            Pass *True* if the cell is a header cell (``<th>``).

        align_center (``bool``, *optional*):
            Pass *True* to center-align the cell content.

        align_right (``bool``, *optional*):
            Pass *True* to right-align the cell content.

        valign_middle (``bool``, *optional*):
            Pass *True* to middle-align the cell content vertically.

        valign_bottom (``bool``, *optional*):
            Pass *True* to bottom-align the cell content vertically.

        colspan (``int``, *optional*):
            Number of columns the cell spans.

        rowspan (``int``, *optional*):
            Number of rows the cell spans.
    """

    def __init__(
        self,
        text: str | raw.base.RichText,
        header: bool | None = None,
        align_center: bool | None = None,
        align_right: bool | None = None,
        valign_middle: bool | None = None,
        valign_bottom: bool | None = None,
        colspan: int | None = None,
        rowspan: int | None = None,
    ):
        super().__init__()

        self.text = text
        self.header = header
        self.align_center = align_center
        self.align_right = align_right
        self.valign_middle = valign_middle
        self.valign_bottom = valign_bottom
        self.colspan = colspan
        self.rowspan = rowspan

    def write(self) -> raw.types.PageTableCell:
        return raw.types.PageTableCell(
            text=_to_rich_text(self.text),
            header=self.header,
            align_center=self.align_center,
            align_right=self.align_right,
            valign_middle=self.valign_middle,
            valign_bottom=self.valign_bottom,
            colspan=self.colspan,
            rowspan=self.rowspan,
        )


class InputRichBlockDetails(InputRichBlock):
    """A details block, corresponding to the HTML tag ``<details>``.

    Creates a collapsible section that the user can expand or collapse.

    Parameters:
        summary (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Summary text of the details element, corresponding to the HTML tag ``<summary>``.
            This is the visible label when the section is collapsed.

        blocks (List of :obj:`~pyrogram.types.InputRichBlock`):
            Blocks inside the details element (hidden until expanded).

        is_open (``bool``, *optional*):
            Pass *True* to display the details element in the open (expanded) state.
    """

    def __init__(
        self,
        summary: str | raw.base.RichText,
        blocks: list[InputRichBlock],
        is_open: bool | None = None,
    ):
        super().__init__()

        self.summary = summary
        self.blocks = blocks
        self.is_open = is_open

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockDetails(
            title=_to_rich_text(self.summary),
            blocks=[b.write() for b in self.blocks],
            open=self.is_open,
        )


class InputRichBlockMap(InputRichBlock):
    """A map block, corresponding to the HTML tag ``<map>``.

    Embeds a geographic map with a pin at the specified location.

    Parameters:
        geo (:obj:`~pyrogram.raw.base.InputGeoPoint`):
            Geolocation of the map pin.

        zoom (``int``):
            Map zoom level (typically 1-20).

        w (``int``):
            Map width in pixels.

        h (``int``):
            Map height in pixels.

        caption (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Caption of the map.
    """

    def __init__(
        self,
        geo: raw.base.InputGeoPoint,
        zoom: int,
        w: int,
        h: int,
        caption: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.geo = geo
        self.zoom = zoom
        self.w = w
        self.h = h
        self.caption = caption

    def write(self) -> raw.base.PageBlock:
        return raw.types.InputPageBlockMap(
            geo=self.geo,
            zoom=self.zoom,
            w=self.w,
            h=self.h,
            caption=_to_page_caption(text=self.caption),
        )


class InputRichBlockAnimation(InputRichBlock):
    """An animation block, corresponding to the HTML tag ``<video>``.

    Displays an animated file (GIF-like) in the message.

    Parameters:
        video_id (``int``):
            Identifier of an uploaded document that represents an animation.

        has_spoiler (``bool``, *optional*):
            Pass *True* to cover the media preview with a spoiler animation.

        caption (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Caption of the block.
    """

    def __init__(
        self,
        video_id: int,
        has_spoiler: bool | None = None,
        caption: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.video_id = video_id
        self.has_spoiler = has_spoiler
        self.caption = caption

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockVideo(
            video_id=self.video_id,
            caption=_to_page_caption(text=self.caption),
            spoiler=self.has_spoiler,
        )


class InputRichBlockAudio(InputRichBlock):
    """An audio block, corresponding to the HTML tag ``<audio>``.

    Displays an audio file (music) in the message.

    Parameters:
        audio_id (``int``):
            Identifier of an uploaded document that represents an audio file.

        caption (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Caption of the block.
    """

    def __init__(
        self,
        audio_id: int,
        caption: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.audio_id = audio_id
        self.caption = caption

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockAudio(
            audio_id=self.audio_id,
            caption=_to_page_caption(text=self.caption),
        )


class InputRichBlockPhoto(InputRichBlock):
    """A photo block, corresponding to the HTML tag ``<photo>``.

    Displays a photo in the message.

    Parameters:
        photo_id (``int``):
            Identifier of an uploaded photo.

        has_spoiler (``bool``, *optional*):
            Pass *True* to cover the photo with a spoiler animation.

        url (``str``, *optional*):
            URL to open when the photo is clicked.

        webpage_id (``int``, *optional*):
            Identifier of the webpage to associate with the photo.

        caption (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Caption of the block.
    """

    def __init__(
        self,
        photo_id: int,
        has_spoiler: bool | None = None,
        url: str | None = None,
        webpage_id: int | None = None,
        caption: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.photo_id = photo_id
        self.has_spoiler = has_spoiler
        self.url = url
        self.webpage_id = webpage_id
        self.caption = caption

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockPhoto(
            photo_id=self.photo_id,
            caption=_to_page_caption(text=self.caption),
            spoiler=self.has_spoiler,
            url=self.url,
            webpage_id=self.webpage_id,
        )


class InputRichBlockVideo(InputRichBlock):
    """A video block, corresponding to the HTML tag ``<video>``.

    Displays a video in the message.

    Parameters:
        video_id (``int``):
            Identifier of an uploaded document that represents a video file.

        has_spoiler (``bool``, *optional*):
            Pass *True* to cover the video with a spoiler animation.

        autoplay (``bool``, *optional*):
            Pass *True* to start playing the video automatically.

        loop (``bool``, *optional*):
            Pass *True* to loop the video playback.

        caption (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Caption of the block.
    """

    def __init__(
        self,
        video_id: int,
        has_spoiler: bool | None = None,
        autoplay: bool | None = None,
        loop: bool | None = None,
        caption: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.video_id = video_id
        self.has_spoiler = has_spoiler
        self.autoplay = autoplay
        self.loop = loop
        self.caption = caption

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockVideo(
            video_id=self.video_id,
            caption=_to_page_caption(text=self.caption),
            autoplay=self.autoplay,
            loop=self.loop,
            spoiler=self.has_spoiler,
        )


class InputRichBlockVoiceNote(InputRichBlock):
    """A voice note block, corresponding to the HTML tag ``<audio>``.

    Displays a voice recording in the message.

    Parameters:
        audio_id (``int``):
            Identifier of an uploaded document that represents a voice note.

        caption (``str`` | :obj:`~pyrogram.raw.base.RichText`, *optional*):
            Caption of the block.
    """

    def __init__(
        self,
        audio_id: int,
        caption: str | raw.base.RichText | None = None,
    ):
        super().__init__()

        self.audio_id = audio_id
        self.caption = caption

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockAudio(
            audio_id=self.audio_id,
            caption=_to_page_caption(text=self.caption),
        )


class InputRichBlockButtonRow(InputRichBlock):
    """A row of buttons embedded directly into a rich message.

    This is part of the button revolution: buttons can live inside the message
    content itself instead of a separate reply markup.

    Parameters:
        buttons (List of :obj:`~pyrogram.types.InlineKeyboardButton`):
            The inline keyboard buttons to embed.
            Only *url*, *callback_data*, *switch_inline_query*,
            *switch_inline_query_current_chat* and *copy_text* buttons are supported.

        align (``str``, *optional*):
            Horizontal alignment of the row: "left", "center" or "right". Defaults to "center".
    """

    def __init__(
        self, buttons: list, align: Literal["left", "center", "right"] = "center"
    ):
        super().__init__()

        self.buttons = buttons
        self.align = align

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockButtonRow(
            align_left=self.align == "left",
            align_center=self.align == "center",
            align_right=self.align == "right",
            buttons=[_to_page_button(b) for b in self.buttons],
        )


def _to_page_button(button) -> raw.types.PageButton:
    """Build a raw PageButton from a high-level InlineKeyboardButton."""
    label = _to_rich_text(str(button.text))

    if button.callback_data is not None:
        data = (
            button.callback_data.encode()
            if isinstance(button.callback_data, str)
            else button.callback_data
        )
        button_type = raw.types.InlineButtonTypeCallback(data=data)
    elif button.url is not None:
        button_type = raw.types.InlineButtonTypeUrl(url=button.url)
    elif button.switch_inline_query_current_chat is not None:
        button_type = raw.types.InlineButtonTypeSwitchInline(
            query=button.switch_inline_query_current_chat,
            same_peer=True,
        )
    elif button.switch_inline_query is not None:
        button_type = raw.types.InlineButtonTypeSwitchInline(
            query=button.switch_inline_query
        )
    elif button.copy_text is not None:
        button_type = raw.types.InlineButtonTypeCopy(copy_text=button.copy_text)
    else:
        raise ValueError(
            "Embedded page buttons support url/callback_data/switch_inline/copy_text only"
        )

    return raw.types.PageButton(text=label, type=button_type)


class InputRichBlockThinking(InputRichBlock):
    """A thinking block (collapsible text that reveals after a bot's reasoning).

    This block is used to show the bot's reasoning process that was collapsed
    or hidden behind a "thinking" indicator.

    Parameters:
        text (``str`` | :obj:`~pyrogram.raw.base.RichText`):
            Text of the block (the reasoning content).
    """

    def __init__(
        self,
        text: str | raw.base.RichText,
    ):
        super().__init__()

        self.text = text

    def write(self) -> raw.base.PageBlock:
        return raw.types.PageBlockThinking(text=_to_rich_text(self.text))
