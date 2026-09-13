from __future__ import annotations

import pyrogram
from pyrogram import raw, utils


class EditUserStarSubscription:
    async def edit_user_star_subscription(
        self: pyrogram.Client,
        user_id: int | str,
        telegram_payment_charge_id: str,
        is_canceled: bool,
    ) -> bool:
        """Cancel or re-enable extension of a subscription paid in Telegram Stars.

        Parameters:
            user_id (``int`` | ``str``):
                Identifier of the user whose subscription will be edited.

            telegram_payment_charge_id (``str``):
                Telegram payment identifier of the subscription.

            is_canceled (``bool``):
                Pass True to cancel the subscription, or False to re-enable extension.

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self.invoke(
            raw.functions.payments.BotCancelStarsSubscription(
                user_id=utils.get_input_user(await self.resolve_peer(user_id)),
                charge_id=telegram_payment_charge_id,
                restore=not is_canceled,
            )
        )
