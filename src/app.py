from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from roblox import Client
from roblox.thumbnails import AvatarThumbnailType
from roblox import groups
from yay.package import *
from yay.update import *
from better_profanity import profanity as pf
import discord_webhook as dh
from discord_webhook import DiscordWebhook, DiscordEmbed    

load_dotenv()
discordbottoken = os.getenv("DISCORD_BOT_TOKEN")

roblox_client = Client(os.getenv("ROBLOX_COOKIE"))
devmode = os.getenv("devmode")
discordhookurl = os.getenv("dishook")
# PREFIX = "💀!"
PREFIX = "!" # change it 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


if devmode == "false":
    bot.remove_command("feedback")
else:
    print("i said dont enable this in the .env file!!! 😡😡😡")
    if discordhookurl == "none":
        print("you know 0 skillz about python huh? 😡😡😡 DISNABLE DEVMODE NOW!")
        bot.remove_command("feedback")
    else:
        print("you are a good developer, but you still need to learn more about python and discord.py, fork this project 😍😍😍😍")
        print("and make it better, i will be waiting for you to make it better 😍😍😍😍.")


def failed(message):
    embed = discord.Embed(title="Error", description=message, color=0xff0000)
    return embed

def feedbackform(message, author):
    webhook = DiscordWebhook(url=discordhookurl, username="John the feedback guy", avatar_url="https://cdn.discordapp.com/attachments/1355188785314529360/1355200439016095905/0eTzq1g.png?ex=67e81043&is=67e6bec3&hm=ae9a383c67c1b55c22342a37f98b7267c40621887ebc372777518f394f0f8a33&")
    embed = DiscordEmbed(title="Feedback", description=message, color=0x00ff00)
    embed.set_footer(text=f"Feedback from {author}")
    webhook.add_embed(embed)
    response = webhook.execute()
    return response

@bot.event
async def on_ready():
    print(f'{bot.user}🎉')

@bot.command()
async def checkforupdates(ctx) :
    newupdate = newupdates()
    if newupdate == True :
        embed = discord.Embed(title="Update", description="There is a new update available!", color=0x0000FF)
        embed.add_field(name="Latest version", value=get_latest_release(), inline=True)
        embed.add_field(name="Current version", value="0.0.0", inline=True)
        embed.add_field(name="Github", value="[Download the latest version from github](https://github.com/triisdang/Bloxskull)",inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Update", description="You are using the latest version!", color=0x00ff00)
        await ctx.send(embed=embed)


@bot.command()
async def about(ctx):
    embed = discord.Embed(title="About", description="This is a simple discord bot that fetches Roblox user information and badge information, Powered by ro.py", color=0x00ff00)
    embed.add_field(name="Author", value="Chip", inline=True)
    embed.add_field(name="Github", value="[Github](https://github.com/triisdang)", inline=True)
    await ctx.send(embed=embed)


@bot.command()
async def fetchuser(ctx, user_id: str):  
    if not user_id.isdigit() or user_id == "":  
        randomuser = pickrandom("user")
        await ctx.send(embed=failed(f"Please provide a valid user ID, Example: `{PREFIX}fetchuser {randomuser}`"))
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
        randombadge = pickrandom("badge")
        await ctx.send(embed=failed(f"Please provide a valid badge ID, Example: `{PREFIX}fetchbadge {randombadge}`"))
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
        randomgame = pickrandom("game")
        await ctx.send(embed=failed(f"Please provide a valid game ID, Example: `{PREFIX}fetchgame {randomgame}`"))
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
        embed.add_field(name="Description", value=place.description or "No description.", inline=False)
        embed.add_field(name="Is playable?", value="Yes" if place.is_playable else "No", inline=True)
        embed.add_field(name="Who made it?", value=f"{place.builder} (ID : {place.builder_id})", inline=True)
        embed.add_field(name="Game link", value=f"[Click me!]({place.url})", inline=True)
        embed.add_field(name="Price", value=place.price if not place.price == 0 else "Free", inline=True)
        embed.set_thumbnail(url=place_thumbnails[0].image_url)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(embed=failed(str(e)))
        return
    

@bot.command()
async def fetchgroup(ctx, group_id: str):
    if not group_id.isdigit():
        randomgroup = pickrandom("group")
        await ctx.send(embed=failed(f"Please provide a valid group ID, Example: `{PREFIX}fetchgroup {randomgroup}`"))
        return
    try: 
        groups = await roblox_client.get_group(group_id)
        group_thumbnails = await roblox_client.thumbnails.get_group_icons(
            groups=[groups],
            size=(150, 150)
        )
        embed = discord.Embed(title=f"Group: {groups.name}", color=0x00ff00)
        embed.add_field(name="ID", value=groups.id, inline=False)
        embed.add_field(name="Description", value=groups.description or "No description.", inline=False)
        embed.add_field(name="Owner", value=f"{groups.owner}", inline=True)
        embed.add_field(name="Member count", value=groups.member_count, inline=True)
        embed.add_field(name="Is locked?", value="Yes" if groups.is_locked == True else "No" , inline=True)
        embed.add_field(name="Shout", value=groups.shout, inline=True)
        embed.set_thumbnail(url=group_thumbnails[0].image_url)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(embed=failed(str(e)))
        return
@bot.command()
async def feedback(ctx, *, feedback: str):
        if not feedback:
            await ctx.send(embed=failed("Please provide a feedback."))
            return
        pf.load_censor_words()
        feedback = pf.censor(feedback) # nuh uh
        if feedback == "": 
            await ctx.send(embed=failed("Please provide a valid feedback."))
            return

        response = feedbackform(feedback.replace('*','X'), ctx.author)
        if response.status_code == 200:
            embed = discord.Embed(title="Feedback", description="Your feedback has been sent successfully!", color=0x00ff00)
            if "*" not in feedback:
                embed.set_footer(text=f":D")
            else:
                embed.set_footer(text=f"Don't say bad things to the devs, they are working hard to make this bot better every day! 💖")
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=failed("Failed to send feedback. Please try again later.. :(. Error : " + str(response)))
            return

bot.run(discordbottoken)
