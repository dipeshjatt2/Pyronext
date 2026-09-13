<div align="center">
  <img src="https://img.icons8.com/color/150/000000/telegram-app.png" alt="Pyronext Logo" width="100"/>
  <h1>🔥 Pyronext</h1>
  <p><b>Advanced, Ultra-Fast & Fully Featured MTProto API Framework for Telegram</b></p>
  
  <p>
    <a href="https://pypi.org/project/pyronext/"><img src="https://img.shields.io/pypi/v/pyronext?style=for-the-badge&color=blue" alt="PyPI Version"/></a>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
    <img src="https://img.shields.io/badge/MTProto_Layer-229-orange?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram API Layer"/>
    <img src="https://img.shields.io/badge/Framework-Asyncio-green?style=for-the-badge&logo=python&logoColor=white" alt="Asyncio"/>
    <a href="https://t.me/pyronext"><img src="https://img.shields.io/badge/Community-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Community"/></a>
  </p>
</div>

---

## ⚡ Overview

**Pyronext** is a modern, high-performance Telegram MTProto client and bot framework in Python. Built for speed, stability, and full MTProto compliance, Pyronext is an enhanced, drop-in replacement for Pyrogram with support for Telegram's latest features.

> [!TIP]
> **100% Drop-In Compatible**: Install `pyronext` and keep all your existing `import pyrogram` code intact. No syntax rewrites required!

---

## ✨ Highlights

| Feature | Description |
| :--- | :--- |
| **🤫 Ephemeral Messages** | Full native support for Telegram ephemeral bot commands, ephemeral updates, and message send/edit/delete APIs. |
| **⭐ Telegram Stars** | Manage Star subscriptions (`edit_user_star_subscription`) and process refunds (`refund_star_payment`). |
| **🎯 Robust Command Filters** | `filters.command` with regex metacharacter safety (e.g. `/c++`, `/buy.now`, `/+`), plus filters for `business`, `story`, `forum`, and `quote`. |
| **🔘 Advanced Inline Buttons** | Full support for `SwitchInlineQueryChosenChat` to prompt user/group/channel inline queries, plus fixed `message.click()` without timeouts. |
| **🤖 Bot Profile Management** | Dynamic localized bot name management via `get_bot_name()` and `set_bot_name()`. |
| **🚀 WarpCrypto Acceleration** | Native cryptographic primitives for fast encryption, decryption, and media chunk streaming. |
| **⚡ MTProto Layer 229** | Always synced with the latest Telegram server layer definitions. |

---

## 🛠 Installation

### Via `uv` (Recommended)
```bash
uv pip install pyronext
```

### Via `pip`
```bash
pip install pyronext
```

*(If you previously had original `pyrogram` installed, uninstall it first to avoid namespace collisions: `pip uninstall pyrogram`)*

---

## 📖 Feature Showcases & Usage Guides

### 1. 🤫 Ephemeral Bot Commands & Messages
Telegram allows bots to send **ephemeral messages**—messages visible only to a specific user inside a group or private chat.

#### Setting Ephemeral Commands
```python
from pyrogram import Client, idle
from pyrogram.types import BotCommand

app = Client("my_bot", api_id=12345, api_hash="your_api_hash", bot_token="your_bot_token")

async def main():
    await app.start()
    # Mark commands with is_ephemeral=True
    await app.set_bot_commands([
        BotCommand("secret", "View your secret info (only visible to you)", is_ephemeral=True),
        BotCommand("help", "Public help command")
    ])
    await idle()
    await app.stop()

app.run(main())
```

#### Handling Ephemeral Commands & Replying
When a user taps `/secret` in the chat, Telegram delivers an ephemeral message update. Reply with `reply_ephemeral()`:

```python
from pyrogram import Client, filters

app = Client("my_bot", api_id=12345, api_hash="your_api_hash", bot_token="your_bot_token")

@app.on_message(filters.command("secret"))
async def handle_secret(client, message):
    # Replies with an ephemeral message visible ONLY to the user who clicked it!
    ephemeral_msg = await message.reply_ephemeral(
        "🤫 This is a secret message only you can see!"
    )

app.run()
```

#### Editing & Deleting Ephemeral Messages
Ephemeral messages can be updated or deleted directly:

```python
# Using Message bound methods:
await ephemeral_msg.edit_ephemeral_text("Updated secret text!")
await ephemeral_msg.delete_ephemeral()

# Or using client-level methods:
await app.edit_ephemeral_message_text(
    chat_id=chat_id,
    receiver_user_id=user_id,
    ephemeral_message_id=message_id,
    text="Updated content"
)

await app.delete_ephemeral_message(
    chat_id=chat_id,
    receiver_user_id=user_id,
    ephemeral_message_id=message_id
)
```

---

### 2. ⭐ Telegram Stars & Subscriptions
Manage user star payments and recurring subscriptions:

```python
# Refund a Telegram Stars charge
await app.refund_star_payment(
    user_id=user_id,
    telegram_payment_charge_id="charge_id_here"
)

# Cancel an active user Stars subscription (stops auto-renewal)
await app.edit_user_star_subscription(
    user_id=user_id,
    telegram_payment_charge_id="charge_id_here",
    is_canceled=True
)

# Re-enable an active subscription
await app.edit_user_star_subscription(
    user_id=user_id,
    telegram_payment_charge_id="charge_id_here",
    is_canceled=False
)
```

---

### 3. 🤖 Localized Bot Name Management
Get or update your bot's name dynamically for specific languages:

```python
# Get bot name for English and Spanish
en_name = await app.get_bot_name(language_code="en")
es_name = await app.get_bot_name(language_code="es")

# Set bot name per language
await app.set_bot_name("Pyronext Assistant", language_code="en")
await app.set_bot_name("Asistente Pyronext", language_code="es")
```

---

### 4. 🔘 Advanced Inline Keyboards & `SwitchInlineQueryChosenChat`
Prompt users to select a target chat when switching to inline mode:

```python
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    SwitchInlineQueryChosenChat
)

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "Share to Group/Channel",
            switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(
                query="check this out!",
                allow_group_chats=True,
                allow_channel_chats=True,
                allow_user_chats=False
            )
        )
    ]
])

await app.send_message(chat_id, "Choose where to share:", reply_markup=keyboard)
```

---

### 5. 🎯 Enhanced Message Filters
Pyronext includes modern filters and fixes regex bugs in command parsing:

```python
from pyrogram import Client, filters

# 1. Commands with metacharacters now work seamlessly:
@app.on_message(filters.command(["c++", "buy.now", "+"]))
async def custom_commands(client, message):
    await message.reply_text(f"Executed: {message.command[0]}")

# 2. Telegram Business messages:
@app.on_message(filters.business)
async def business_handler(client, message):
    print("Received message via Business connection!")

# 3. Forum topic messages:
@app.on_message(filters.forum)
async def forum_handler(client, message):
    print(f"Forum message in topic: {message.message_thread_id}")

# 4. Messages containing Stories:
@app.on_message(filters.story)
async def story_handler(client, message):
    print("Message contains a story")

# 5. Messages with Quotes:
@app.on_message(filters.quote)
async def quote_handler(client, message):
    print("User quoted a specific text snippet")
```

---

### 6. 🖱️ Reliable Button Clicking (`Message.click()`)
Automate button clicks with zero timeouts and correct label resolution:

```python
# Click button by index (row 0, button 0):
await message.click(0)

# Click button by 2D coordinates (x=1, y=0):
await message.click(1, 0)

# Click button by text label:
await message.click("Confirm Payment")
```

---

## 📄 License & Disclaimer

Pyronext is licensed under the [LGPLv3 License](LICENSE).

> [!NOTE]
> Pyronext is an independent community project based on the open-source Telegram MTProto architecture.
