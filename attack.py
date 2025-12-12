import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

mute_role_id = None  # will be set using !setmute
blocked_role_id = 1289449242506821681  # your blocked role


def is_admin(ctx):
    return ctx.author.guild_permissions.manage_guild


@bot.command()
async def setmute(ctx, role: discord.Role):
    global mute_role_id
    if not is_admin(ctx):
        await ctx.send("❌ You don't have permission to use this command.")
        return

    mute_role_id = role.id
    await ctx.send(f"✅ Mute role set to **{role.name}**.")


@bot.command()
async def block(ctx, member: discord.Member):
    if not is_admin(ctx):
        await ctx.send("❌ You don't have permission to use this command.")
        return

    role = ctx.guild.get_role(blocked_role_id)
    if role in member.roles:
        await ctx.send("❌ That user is already blocked.")
        return

    await member.add_roles(role)
    await ctx.send(f"🚫 {member.mention} is now blocked from using **!attack**.")


@bot.command()
async def unblock(ctx, member: discord.Member):
    if not is_admin(ctx):
        await ctx.send("❌ You don't have permission to use this command.")
        return

    role = ctx.guild.get_role(blocked_role_id)
    if role not in member.roles:
        await ctx.send("❌ That user is not blocked.")
        return

    await member.remove_roles(role)
    await ctx.send(f"✅ {member.mention} can now use **!attack**.")


@bot.command()
async def attack(ctx, member: discord.Member):
    global mute_role_id

    if mute_role_id is None:
        await ctx.send("❌ No mute role set. Use **!setmute @Role** first.")
        return

    blocked_role = ctx.guild.get_role(blocked_role_id)
    if blocked_role in ctx.author.roles:
        await ctx.send("❌ You are blocked from using this command.")
        return

    if member == ctx.author:
        await ctx.send("❌ You cannot attack yourself.")
        return

    await ctx.send(f"⚔️ {ctx.author.mention} is attacking {member.mention}...")

    msg = await ctx.send("Loading: 0%")

    for i in range(10, 101, 10):
        await asyncio.sleep(0.3)
        await msg.edit(content=f"Loading: {i}%")

    power = random.randint(0, 100)
    await asyncio.sleep(0.5)
    await msg.edit(content=f"Final Power: **{power}%**")

    mute_role = ctx.guild.get_role(mute_role_id)

    if power >= 60:
        duration = random.randint(30, 120)
        await member.add_roles(mute_role)
        await ctx.send(f"🎯 Success! {member.mention} muted for **{duration} seconds**.")
        await asyncio.sleep(duration)
        await member.remove_roles(mute_role)
        await ctx.send(f"🔓 {member.mention} is now unmuted.")
    else:
        duration = random.randint(30, 100)
        await ctx.author.add_roles(mute_role)
        await ctx.send(f"💥 Backfire! You got muted for **{duration} seconds**, {ctx.author.mention}.")
        await asyncio.sleep(duration)
        await ctx.author.remove_roles(mute_role)
        await ctx.send(f"🔓 You are unmuted now, {ctx.author.mention}.")


TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
