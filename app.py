from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from roblox import Client

load_dotenv()
discordbottoken = os.getenv("DISCORD_BOT_TOKEN")

roblox_client = Client()

PREFIX = "💀!"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 🎉')


@bot.command()
async def roblox_user(ctx, user_id: int):
    """Fetches Roblox user details by ID"""
    try:
        user = await roblox_client.get_user(user_id)
        await ctx.send(f"Roblox User: {user.name} (ID: {user.id}) ")
    except Exception as e:
        await ctx.send(f"Error fetching user: {e} ")

bot.run(discordbottoken)
