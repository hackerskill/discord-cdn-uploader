# discord-exif-cdn-uploader
A discord bot to upload images to cdn with option to strip the metadata

## Features
* **CDN Uploader** — Directly upload images from Discord
* **Remove Metadata** — Removes the metadata of the image before sending
* **Markdown Format** — Automatically generates markdown format to directly paste
* **Discord Support** — Works directly in Discord DMs and servers
* **Slash Commands** — Short commands for controlling the bot

## Slash Commands
* **`markdown`** — Toggle sending of markdown format
* **`ping`** — Check chatbot connectivity status
* **`clear`** — Clear recent messages by chatbot
* **`about`** — Shows information about the bot itself

## Setup

1. Get API keys for Discord bot at [Discord Developer Portal](https://discord.com/developers/) and CDN.

2. Clone the repo

3. **Create and activate a virtual environment:**
   * **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
4. **Change `.env.example` to `.env` with the following keys-**
    * Discord token specific for a bot
    * CDN API key
    * CDN server URL

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Once setup is verified, `main.py` can be run to start the discord chatbot.

---

**Made by hackerskill**
