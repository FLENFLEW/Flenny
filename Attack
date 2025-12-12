import discord
from discord.ext import commands, tasks
import random
import asyncio
import os

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Variables
mute_role_id = None  # will be set with !setmute
blocked_role_id = 1289449242506821681  # your blocked role

# Helper: check if user has Manage Server permission
def is_admin(ctx):
    return ctx.author.guild_permissions.manage_guild

# ---------------- Commands ----------------

@bot.command()
async def setmute(ctx, role: discord.Role):
    if not is_admin(ctx):
        await ctx.send("❌ You don't have permission to use this command.")
        return
    global mute_role_id
    mute_role_id = role.id
    await ctx.send(f"✅ Mute role set to {role.name}.")

@bot.command()
async def block(ctx, member: discord.Member):
    if not is_admin(ctx):
        await ctx.send("❌ You don't have permission to use this command.")
        return
    role = ctx.guild.get_role(blocked_role_id)
    if role in member.roles:
        await ctx.send(f"❌ {member.mention} is already blocked.")
        return
    await member.add_roles(role)
    await ctx.send(f"✅ {member.mention} is now blocked from using !attack.")

@bot.command()
async def unblock(ctx, member: discord.Member):
    if not is_admin(ctx):
        await ctx.send("❌ You don't have permission to use this command.")
        return
    role = ctx.guild.get_role(blocked_role_id)
    if role not in member.roles:
        await ctx.send(f"❌ {member.mention} is not blocked.")
        return
    await member.remove_roles(role)
    await ctx.send(f"✅ {member.mention} can now use !attack.")

@bot.command()
async def attack(ctx, member: discord.Member):
    global mute_role_id
    if mute_role_id is None:
        await ctx.send("❌ No mute role set. Use !setmute first.")
        return
    # Check blocked role
    blocked_role = ctx.guild.get_role(blocked_role_id)
    if blocked_role in ctx.author.roles:
        await ctx.send("❌ You are blocked from using this command.")
        return
    if member == ctx.author:
        await ctx.send("❌ You cannot attack yourself!")
        return

    await ctx.send(f"⚔️ {ctx.author.mention} is attacking {member.mention}...")
    # Loading animation simulation
    loading_msg = await ctx.send("Loading: 0%")
    for i in range(10, 101, 10):
        await asyncio.sleep(0.3)
        await loading_msg.edit(content=f"Loading: {i}%")
    power = random.randint(0, 100)
    await asyncio.sleep(0.5)
    await loading_msg.edit(content=f"Final Power: **{power}%**")

    mute_role = ctx.guild.get_role(mute_role_id)

    if power >= 60:
        duration = random.randint(30, 120)
        await member.add_roles(mute_role)
        await ctx.send(f"🎯 Success! {member.mention} has been muted for {duration} seconds.")
        await asyncio.sleep(duration)
        await member.remove_roles(mute_role)
        await ctx.send(f"🔓 {member.mention} is now unmuted.")
    else:
        duration = random.randint(30, 100)
        await ctx.author.add_roles(mute_role)
        await ctx.send(f"💥 Backfire! {ctx.author.mention} has been muted for {duration} seconds.")
        await asyncio.sleep(duration)
        await ctx.author.remove_roles(mute_role)
        await ctx.send(f"🔓 {ctx.author.mention} is now unmuted.")

# ---------------- Bot Run ----------------
bot.run(os.getenv("TOKEN"))
