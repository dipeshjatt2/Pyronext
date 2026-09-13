<div align="center">
  <img src="https://img.icons8.com/color/150/000000/telegram-app.png" alt="Pyronext Logo" width="100"/>
  <h1>🔥 Pyronext</h1>
  <p><b>Advanced, Modern & Fully Customized MTProto API Framework for Telegram</b></p>
  
  <p>
    <a href="https://pypi.org/project/pyronext/"><img src="https://img.shields.io/pypi/v/pyronext?style=for-the-badge&color=blue" alt="PyPI Version"/></a>
    <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"/>
    <img src="https://img.shields.io/badge/API_Layer-Latest-orange?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram API Layer"/>
    <img src="https://img.shields.io/badge/Framework-Asyncio-green?style=for-the-badge&logo=python&logoColor=white" alt="Asyncio"/>
  </p>
</div>

---

## ⚡ About Pyronext

**Pyronext** is an advanced and actively maintained fork of Electrogram (which stems from Pyrogram). It has been updated for the latest Telegram MTProto layers and specifically modified, patched, and optimized to fix underlying bugs found in the original framework. 

It is designed to be a **drop-in replacement** for Pyrogram, meaning you don't have to rewrite any of your existing bot code or imports!

## ✨ Key Features & Fixes

- **Drop-In Replacement**: Install `pyronext` but continue to `import pyrogram`. Everything remains backwards compatible.
- **Flawless Inline Callbacks**: Permanently fixes the notorious `message.click()` timeout bug and unhandled retry loops from the original framework. 
- **Latest MTProto Layer**: Synced with the most recent Telegram API updates.
- **Enhanced Reliability**: Internal networking, sessions, and callback answer requests are patched for flawless execution and better type safety.
- **Fully Asynchronous**: Built heavily on Python's `asyncio` for blazing fast concurrent processing.

---

## 🛠 Installation

You can install Pyronext directly from PyPI (recommended):

```bash
pip install pyronext
```
*(If you have `pyrogram` or `electrogram` installed, make sure to uninstall them first to avoid namespace conflicts: `pip uninstall pyrogram electrogram`)*

### Installing from Source
If you want to install the absolute latest development version from GitHub using `uv`:
```bash
git clone https://github.com/dipeshjatt2/Pyronext.git
cd Pyronext
uv pip install -e .
```

---

## 🚀 Quick Start Guide

Using Pyronext is exactly the same as using Pyrogram. 

### 1. Simple Echo Bot
Here is a basic example of an Echo Bot:

```python
from pyrogram import Client, filters

app = Client("my_bot", api_id=12345, api_hash="your_api_hash", bot_token="your_bot_token")

@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply_text(message.text)

app.run()
```

### 2. Clicking Inline Buttons (Fixed in Pyronext!)
Pyronext features a fully repaired `Message.click()` method. You can now easily automate button presses without MTProto timeouts:

```python
from pyrogram import Client, filters

app = Client("my_account", api_id=12345, api_hash="your_api_hash")

@app.on_message(filters.bot & filters.regex("Choose an option"))
async def handle_bot_menu(client, message):
    # Click the first button natively!
    await message.click(0)
    print("Button successfully clicked!")

app.run()
```

---

## ⚠️ Disclaimer

This repository is **Pyronext (an Electrogram/Pyrogram fork)** created specifically for our projects and modified to suit our needs.

Please understand that any issues, modifications, or deviations from the original project are solely our responsibility. Do not hold the original Pyrogram or Electrogram authors accountable for any problems or discrepancies that may arise from using this repository.

---
<div align="center">
  Developed & Maintained by <b>Dipesh Chaudhary</b><br>
  Join our community: <a href="https://t.me/pyronext">@pyronext</a>
</div>
