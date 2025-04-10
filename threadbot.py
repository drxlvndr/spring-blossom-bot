import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

log_channel = None

MAZE_IMAGE_URL = "https://cdn.discordapp.com/attachments/1359069286060261447/1359098672260059337/maze.jpg"

AUTHORIZED_USER_IDS = [779853330830458901]

def is_authorized(ctx):
    return ctx.author.id == ctx.guild.owner_id or ctx.author.id in AUTHORIZED_USER_IDS

class ThreadButton(Button):
    def __init__(self):
        super().__init__(label="Create Private Thread", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        global log_channel
        try:
            thread = await interaction.channel.create_thread(
                name=f"{interaction.user.name}'s Thread",
                type=discord.ChannelType.private_thread,
                auto_archive_duration=60
            )
            await thread.add_user(interaction.user)

            await thread.send(
                f"Hello {interaction.user.mention},\n"
                "Thank you for your interest in our **Spring Blossom Escape** event!\n\n"
                "Kindly follow the steps outlined below:\n\n"
                "1. Download the maze image provided below.\n"
                "2. Solve the maze to the best of your ability.\n"
                "3. Submit your completed maze in this thread.\n"
                "4. Ensure your **Discord username** is clearly visible on the submission image.\n\n"
                "❗ Submissions without a username will be considered **invalid**.\n\n"
                "The <@&1278742082231603350> team will review all submissions once the event concludes.\n\n"
                "✨ Best of luck!"
            )

            await thread.send(MAZE_IMAGE_URL)

            await interaction.response.send_message(f"✅ Created private thread: {thread.mention}", ephemeral=True)

            print(f"📌 {interaction.user} created a private thread: {thread.name} ({thread.id})")
            if log_channel:
                await log_channel.send(f"📌 {interaction.user.mention} created a private thread: {thread.mention}")

        except Exception as e:
            print(f"Error: {e}")
            try:
                await interaction.response.send_message("❌ Could not create thread.", ephemeral=True)
            except:
                pass
            if log_channel:
                await log_channel.send(f"❌ Failed to create thread for {interaction.user.mention}: `{e}`")

@bot.event
async def on_ready():
    global log_channel
    print(f"✅ Logged in as {bot.user}")

    channel = bot.get_channel(CHANNEL_ID)
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    panel_text = (
        "# Hey hey, MOBA fam~! <a:hi:1113066390480486492> <a:hi:1113066390480486492> \n"
        "<:DPandaFlowerHead:995283300576931851> Ready to join the <a:an_angela_flowerbloom:1356626214202380439> "
        "*_Spring Blossom Escape_* <a:an_angela_flowerbloom:1356626214202380439> adventure?  \n"
        "But before we get started, pretty pleaseeeeeeeeeee <a:nyaPlease:571243415631560713> make sure you’ve read and understood "
        "all the important info in the <#1301805733708435558> channel, okay? <a:BPandaOkay:993596849778851860> \n"
        "-# I'll be reallyyyyy upset if you get disqualified <a:8ACOSP_kittencry:755942090193633308> \n\n"
        "<a:nyaYay:649465448424800287> Once you're all set, just click the button below and a special little thread will bloom just for you!"
    )

    if channel:
        view = View()
        view.add_item(ThreadButton())
        await channel.send(panel_text, view=view)
    else:
        print("❌ Could not find the main panel channel.")

    if log_channel:
        await log_channel.send(f"✅ Bot is online as **{bot.user}** and ready to log thread activity.")
    else:
        print("❌ Could not find the log channel.")

@bot.command()
async def updatepanel(ctx, *, new_message: str):
    if not is_authorized(ctx):
        return await ctx.send("❌ You don’t have permission to use this command.", delete_after=5)

    print("🔧 Received !updatepanel command")

    async for message in ctx.channel.history(limit=50):
        if message.author == bot.user and message.components:
            try:
                await message.edit(content=new_message)
                await ctx.send("✅ Panel message updated!", delete_after=5)
                return
            except Exception as e:
                await ctx.send(f"❌ Failed to update panel: `{e}`", delete_after=5)
                return

    await ctx.send("❌ Couldn’t find the panel message in recent messages.", delete_after=5)

@bot.command()
async def sendpanel(ctx, channel: discord.TextChannel):
    if not is_authorized(ctx):
        return await ctx.send("❌ You don’t have permission to use this command.", delete_after=5)

    panel_text = (
        "# Hey hey, MOBA fam~! <a:hi:1113066390480486492> <a:hi:1113066390480486492> \n"
        "<:DPandaFlowerHead:995283300576931851> Ready to join the <a:an_angela_flowerbloom:1356626214202380439> "
        "*_Spring Blossom Escape_* <a:an_angela_flowerbloom:1356626214202380439> adventure?  \n"
        "But before we get started, pretty pleaseeeeeeeeeee <a:nyaPlease:571243415631560713> make sure you’ve read and understood "
        "all the important info in the <#1301805733708435558> channel, okay? <a:BPandaOkay:993596849778851860> \n"
        "-# I'll be reallyyyyy upset if you get disqualified <a:8ACOSP_kittencry:755942090193633308> \n\n"
        "<a:nyaYay:649465448424800287> Once you're all set, just click the button below and a special little thread will bloom just for you!"
    )

    view = View()
    view.add_item(ThreadButton())
    await channel.send(panel_text, view=view)
    await ctx.send(f"✅ Panel sent to {channel.mention}", delete_after=5)

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

bot.run(TOKEN)











