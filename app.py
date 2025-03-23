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




def failed (message):
    embed = discord.Embed(title="Error", description=message, color=0xff0000)
    return embed



@bot.event
async def on_ready():
    print(f'{bot.user} 🎉')


@bot.command()
async def roblox_user(ctx, user_id: int):
    """Fetches Roblox user details by ID"""
    try:
        if user_id is None:
            await ctx.send(embed=failed("Please provide a valid user ID, Example: `!roblox_user 1`"))
        else:
            user = await roblox_client.get_user(user_id)
            embed = discord.Embed(title=f"Roblox User: {user.name}", color=0x00ff00)
            embed.add_field(name="ID", value=user.id)
            embed.add_field(name="Display name", value=user.display_name)
            embed.add_field(name="Description", value=user.description)
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(embed=failed(str(e)))

bot.run(discordbottoken)
