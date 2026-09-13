from __future__ import annotations

import pyrogram
from pyrogram import raw, utils


class SetBotName:
    async def set_bot_name(
        self: pyrogram.Client,
        name: str,
        language_code: str = "",
        for_my_bot: int | str | None = None,
    ) -> bool:
        """Set the bot name for the given user language.

        Parameters:
            name (``str``):
                New bot name; 0-64 characters. Pass an empty string to remove.

            language_code (``str``, *optional*):
                A two-letter ISO 639-1 language code or an empty string.

            for_my_bot (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target bot.

        Returns:
            ``bool``: True on success.
        """
        return await self.invoke(
            raw.functions.bots.SetBotInfo(
                bot=utils.get_input_user(await self.resolve_peer(for_my_bot))
                if for_my_bot
                else None,
                lang_code=language_code,
                name=name,
            )
        )
