from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from roblox import Client
from roblox.thumbnails import AvatarThumbnailType


load_dotenv()
discordbottoken = os.getenv("DISCORD_BOT_TOKEN")

roblox_client = Client(os.getenv("ROBLOX_COOKIE"))

# PREFIX = "💀!"
PREFIX = "!" # change it 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def failed(message):
    embed = discord.Embed(title="Error", description=message, color=0xff0000)
    return embed

@bot.event
async def on_ready():
    print(f'{bot.user}🎉')


@bot.command()
async def about(ctx):
    embed = discord.Embed(title="About", description="This is a simple discord bot that fetches Roblox user information and badge information, Powered by ro.py", color=0x00ff00)
    embed.add_field(name="Author", value="Chip", inline=True)
    embed.add_field(name="Github", value="[Github](https://github.com/triisdang)", inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def roblox_user(ctx, user_id: str):  
    if not user_id.isdigit():  
        await ctx.send(embed=failed(f"Please provide a valid user ID, Example: `{PREFIX}roblox_user 1`"))
        return  

    user_id = int(user_id)  

    try:
        user = await roblox_client.get_user(user_id)

        user_thumbnails = await roblox_client.thumbnails.get_user_avatar_thumbnails(
            users=[user_id], 
            type=AvatarThumbnailType.full_body, 
            size=(420, 420)
        )

        embed = discord.Embed(title=f"Roblox User: {user.name}", color=0x00ff00)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Display name", value=user.display_name, inline=True)
        embed.add_field(name="Description", value=user.description or "No description.", inline=True)
        embed.add_field(name="Is banned?" , value=user.is_banned, inline=True)
        embed.add_field(name="Join date", value=user.created, inline=True)
        if user_thumbnails:
            embed.set_thumbnail(url=user_thumbnails[0].image_url)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(embed=failed(str(e)))

@bot.command()
async def fetchbadge(ctx, badge_id: str):
    if not badge_id.isdigit():
        await ctx.send(embed=failed(f"Please provide a valid badge ID, Example: `{PREFIX}fetchbadge 3141599589206075`"))
        return
    
    badge_id = int(badge_id)
    try : 
        badge = await roblox_client.get_badge(badge_id)

        badge_icons = await roblox_client.thumbnails.get_badge_icons(
        badges=[badge],
        size=(150, 150)
        )
        statistics = badge.statistics
        embed = discord.Embed(title=f"Badge: {badge.name}", color=0x00ff00)
        embed.add_field(name="ID", value=badge.id, inline=False)
        embed.add_field(name="Description", value=badge.description or "No description.", inline=True)
        embed.add_field(name="Enabled", value=badge.enabled, inline=True)
        embed.add_field(name="Created", value=badge.created, inline=True)
        embed.add_field(name="Updated", value=badge.updated, inline=True)
        embed.add_field(name="Awarded count", value=statistics.awarded_count, inline=True)
        embed.add_field(name="Win rate percentage", value=f"{statistics.win_rate_percentage}%", inline=True)
        embed.set_thumbnail(url=badge_icons[0].image_url)

        await ctx.send(embed=embed) 
    except Exception as e:
        await ctx.send(embed=failed(str(e)))

@bot.command()
async def fetchgame(ctx, place_id: str):
    if not place_id.isdigit():
        await ctx.send(embed=failed(f"Please provide a valid game ID, Example: `{PREFIX}fetchgame 3141599589206075`"))
        return
    
    place_id = int(place_id)
    try:  
        place = await roblox_client.get_place(place_id)
        place.url = place.url
        place_thumbnails = await roblox_client.thumbnails.get_place_icons(
            places=[place],
            size=(512, 512)
        )
        embed = discord.Embed(title=f"Game: {place.name}", color=0x00ff00)
        embed.add_field(name="ID", value=place.id, inline=False)
        embed.add_field(name="Description", value=place.description or "No description.", inline=True)
        embed.add_field(name="Is playable?", value="Yes" if place.is_playable else "No", inline=True)
        embed.add_field(name="Who made it?", value=f"{place.builder} (ID : {place.builder_id})", inline=True)
        embed.add_field(name="Game link", value=f"Click me![{place.url}]", inline=True)
        embed.add_field(name="Price", value=place.price if not place.price == 0 else "Free", inline=True)
        embed.set_thumbnail(url=place_thumbnails[0].image_url)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(embed=failed(str(e)))
        return
        
bot.run(discordbottoken)
