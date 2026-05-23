import os
import discord
from discord.ext import commands
from datetime import datetime

TOKEN = os.environ["DISCORD_TOKEN"]

OWNER_ID = 1505927771115880520

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

messages_forwarded = 0
replies_sent = 0
start_time = None

@bot.event
async def on_ready():
    global start_time
    start_time = datetime.now()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        if message.author.id != OWNER_ID:
            global messages_forwarded
            await message.channel.send("✅ Message received! Staff will reply soon.")

            owner = await bot.fetch_user(OWNER_ID)

            embed = discord.Embed(
                title="📩 New Modmail",
                description=message.content,
                color=discord.Color.blue()
            )
            embed.add_field(
                name="User",
                value=f"{message.author} ({message.author.id})",
                inline=False
            )
            await owner.send(embed=embed)
            messages_forwarded += 1

    await bot.process_commands(message)

@bot.command()
async def reply(ctx, user_id: int, *, message):
    if ctx.author.id != OWNER_ID:
        return

    try:
        user = await bot.fetch_user(user_id)

        embed = discord.Embed(
            title="📨 Staff Reply",
            description=message,
            color=discord.Color.green()
        )
        await user.send(embed=embed)
        global replies_sent
        replies_sent += 1
        await ctx.send("✅ Reply sent.")
    except Exception:
        await ctx.send("❌ Could not send message.")

@bot.command()
async def status(ctx):
    if ctx.author.id != OWNER_ID:
        return

    uptime = ""
    if start_time:
        delta = datetime.now() - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime = f"{hours}h {minutes}m {seconds}s"

    embed = discord.Embed(
        title="📊 Bot Status",
        color=discord.Color.blurple()
    )
    embed.add_field(name="🟢 Status", value="Online", inline=True)
    embed.add_field(name="⏱️ Uptime", value=uptime or "Unknown", inline=True)
    embed.add_field(name="📩 Messages Forwarded", value=str(messages_forwarded), inline=True)
    embed.add_field(name="📨 Replies Sent", value=str(replies_sent), inline=True)

    await ctx.send(embed=embed)

bot.run(TOKEN)
