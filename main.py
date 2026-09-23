import os
import io
from dotenv import load_dotenv
import discord
from discord import app_commands
from PIL import Image
import aiohttp

load_dotenv()
 
token = os.getenv("DISCORD_TOKEN")

api_key=os.getenv("CDN_API_KEY")
server_url=os.getenv("SERVER_URL")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree= app_commands.CommandTree(client)

markdown_format=True

async def strip_metadata(attachment):
    image_bytes=await attachment.read()

    with Image.open(io.BytesIO(image_bytes)) as img:
        if img.format:
            format=img.format
        else:
            format="PNG"
        clean_img= Image.new(img.mode, img.size)
        clean_img.putdata(list(img.getdata()))
        # Creating temporary file and then storing it without metadata
        buffer=io.BytesIO()
        clean_img.save(buffer, format=format)
        buffer.seek(0)

        return buffer.getvalue(), format.lower()

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}", flush=True)

@tree.command(name="ping", description="Ping the bot to check connection")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! Latency: {latency} ms")

@tree.command(name="clear", description="clearing the bot's messages")
async def clear(interaction: discord.Interaction, clear: int):
    await interaction.response.send_message("Clearing messages...")
    async for msg in interaction.channel.history(limit=clear):
                if msg.author == client.user:
                    await msg.delete()
    global conversation
    conversation=[]

@tree.command(name="markdown", description="toggle markdown formatting for bot's messages")
@app_commands.choices(format=[
    app_commands.Choice(name="on", value="on"),
    app_commands.Choice(name="off", value="off")
])
async def markdown(interaction: discord.Interaction, format: app_commands.Choice[str]):
    await interaction.response.send_message(f"Markdown format: {format.value}")
    global markdown_format
    markdown_format = True if format.value == "on" else False
    print(f"Markdown format changed to: {markdown_format}", flush=True)

@tree.command(name="about", description="Get information about this chatbot")
async def about(interaction: discord.Interaction):
    await interaction.response.send_message("This is a discord chatbot, built as a wrapper around openrouter api, where variety of AI models can be directly accessed from discord chats."
    "\n\n_Built by hackerskills_")

@client.event
async def on_message(message):

    if message.author == client.user:
        return 
    #ignored bot's own messages to stop looping

    image_attachments=[]

    for attachment in message.attachments:
        if attachment.content_type and attachment.content_type.startswith('image/'):
            image_attachments.append(attachment)

    if not image_attachments:
        return

    headers={"Authorization": f"Bearer {api_key}"}

    async with aiohttp.ClientSession() as session:
        for attachment in image_attachments:
            clean_bytes, extension = await strip_metadata(attachment)
            mime_type = f"image/{extension}"

        formdata = aiohttp.FormData()
        formdata.add_field(
            "file",
            clean_bytes,
            filename=f"image.{extension}",
            content_type=mime_type
            )

        url = f"{server_url}/upload"
        async with session.post(
            url,
            headers=headers,
            data=formdata
        ) as response:
            if response.status>= 200 and response.status < 300:
                response = await response.json()
                cdn_url = response.get("url")
                print(response, flush=True)
                await message.channel.send(f"Image uploaded successfully:\n`{cdn_url}`")
                if markdown_format:
                    await message.channel.send(f"![](<{cdn_url}>)")
                print(f"Image uploaded successfully: {cdn_url}", flush=True)
            else:
                await message.channel.send(f"Failed to upload image. Status code: {response.status}")
                print(f"Failed to upload image. Status code: {response.status}", flush=True)

        print("hello, world", flush=True)
        await message.channel.send("hello, world")

client.run(token)