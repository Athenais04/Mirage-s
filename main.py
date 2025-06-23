import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import sys
from keep_alive import keep_alive  # importe ta fonction keep_alive

print("Python version:", sys.version)

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_NAME_TO_WATCH = "RL en attente"
ROLE_TO_PING = "RL STAFF"
CHANNEL_ID = 1382315923427295275  # à adapter

@bot.event
async def on_ready():
    print(f"Bot prêt : {bot.user}")

@bot.event
async def on_member_update(before, after):
    print(f"Mise à jour détectée pour {after.name}")
    added_roles = [r for r in after.roles if r not in before.roles]
    for role in added_roles:
        if role.name == ROLE_NAME_TO_WATCH:
            channel = bot.get_channel(CHANNEL_ID)
            staff_role = discord.utils.get(after.guild.roles, name=ROLE_TO_PING)
            if channel and staff_role:
                await channel.send(f"{staff_role.mention} : {after.mention} a reçu le rôle **{ROLE_NAME_TO_WATCH}** !")

token = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
    keep_alive()  # démarre Flask en thread séparé pour UptimeRobot
    bot.run(token)
