# imports
import discord, datetime, asyncio
from discord.ext import commands
from webserver import keep_alive
import os

# public variables
prefix = "p!"

channel = ""

welcome_channel_id = 494176354234007553

message_log_channel_id = 818402622176231434

mod_log_channel_id = 818510780969648138

platt_guild_id = 493807792315170836

joker_guild_id = 831934428862742578

client = commands.Bot(command_prefix=prefix,  case_insensitive=True)

# run code


# role command joker
@client.command()
@commands.cooldown(1, 60, commands.cooldowns.BucketType.member)
async def role(ctx, role_name):
  joker_guild = client.get_guild(joker_guild_id)
  guild = ctx.guild
  role_name = str(role_name)
  role_n = discord.utils.get(guild.roles, name=role_name)
  if guild == joker_guild:
    if not role_n:
      self_role = await guild.create_role(name=role_name)
      await ctx.author.add_roles(self_role)
      await ctx.send(f"Successfully added the role {role_name} to {ctx.author.mention}")
    else:
      await ctx.send("This role exists already. Please ask an admin to get the role.")
    
# send people dms
@client.command()
@commands.cooldown(1, 30, commands.cooldowns.BucketType.member)
async def dm(ctx, user: discord.Member):
  await ctx.send("Wath do you want to say?")
  def check(m):
    return m.author.id == ctx.author.id
  message = await client.wait_for("message", check=check)
  await user.send(f"A message of {str(message.author)}: {message.content}")
  await ctx.send(f"Successfully sent a message to {str(user)}")

# change nickname
@client.command()
@commands.has_permissions(administrator=True)
async def nick(ctx, user: discord.Member, nick):
  guild = ctx.guild
  await user.edit(nick=nick)
  await ctx.channel.send(f"Nickname changed for {user.name} to {nick}")
  await user.send(f"Your nickname on the {guild.name} Server is now {nick}")

# delete nickname
@client.command()
@commands.has_permissions(administrator=True)
async def clearNick(ctx, user: discord.Member):
  guild = ctx.guild
  await user.edit(nick=user.name)
  await ctx.channel.send(f"Nickname cleared for {user.name}")
  await user.send(f"Your nickname on the {guild.name} Server was cleared")

# clan role
@client.command()
@commands.cooldown(1, 60, commands.cooldowns.BucketType.member)
async def clan(ctx, clan_role):
    guild = ctx.guild
    clanName = str(clan_role)
    clan_role = discord.utils.get(guild.roles, name=clanName)

    if not clan_role:
        clan_role = await guild.create_role(name=clanName, hoist=True)

    await ctx.author.add_roles(clan_role)
    await ctx.send(f"{ctx.author.mention} was added the clan-role {clanName}.")
    await ctx.author.send(f'Hey {ctx.author.mention}! You got the Role "{clanName}" now!')

# server roles
@client.command()
async def serverRoles(ctx):
    guild=ctx.guild
    roles=[role for role in guild.roles]
    embed = discord.Embed(title="all Serverroles of the server " + str(guild.name), description="Server role list", timestamp=datetime.datetime.utcnow())

    embed.set_thumbnail(url=str(guild.icon_url))
    embed.set_footer(text=str(guild.name), icon_url=str(guild.icon_url))

    embed.add_field(name="all Server Roles [" + str(len(guild.roles)) + "(with @everyone)]", value=[role.mention for role in roles])

    await ctx.send(embed=embed)

# add role
@client.command()
@commands.has_permissions(administrator=True)
async def addRole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{role} was added to {user.mention}")

# clear
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    deletion = await ctx.channel.purge(limit=amount)
    await ctx.channel.send(f"i've deleted {len(deletion)} messages")

# timer
@client.command()
async def timer(ctx, seconds):
    secondint=int(seconds)
    if secondint > 300:
        await ctx.send("i can't go over 5 min")
    elif secondint <= 0:
        await ctx.send("i can't do a negative timer")
    else:
        message = await ctx.send(f"{seconds}")
        await asyncio.sleep(0.7)
        while True:
            secondint -=1
            if secondint == 0:
                await message.edit(content="countdown ended")
                break

            await message.edit(content=f"{secondint}")
            await asyncio.sleep(0.7)

# roleinfo
@client.command()
async def roleinfo(ctx, role: discord.Role):
    guild=ctx.guild
    embed = discord.Embed(title="Roleinfo of " + str(role), colour=role.colour, description= str(role.mention), timestamp=datetime.datetime.utcnow())

    embed.set_footer(text=str(guild), icon_url=str(guild.icon_url))

    embed.add_field(name="Role ID", value=str(role.id))
    embed.add_field(name="user", value=len(role.members))
    embed.add_field(name="Role created", value=role.created_at.strftime('%d/%m/%Y %H:%M:%S'))
    embed.add_field(name="Name", value=str(role.name))
    embed.add_field(name="Role position (from bottom)", value=str(int(role.position)))

    await ctx.send(embed=embed)

# userinfo
@client.command()
async def userinfo(ctx, user: discord.Member):
    roles=[role for role in user.roles]
    embed = discord.Embed(title="Userinfo of " + str(user), colour=user.colour, description= str(user.mention), timestamp=datetime.datetime.utcnow())

    embed.set_thumbnail(url=str(user.avatar_url))
    embed.set_footer(text=str(user), icon_url=str(user.avatar_url))

    embed.add_field(name="User ID", value=str(user.id))
    embed.add_field(name="Nickname", value=str(user.display_name))
    embed.add_field(name="highest Role", value=str(user.top_role.mention))
    embed.add_field(name="Roles [" + str(len(user.roles)-1) + "]", value=[role.mention for role in roles], inline=False)
    embed.add_field(name="joined Server", value=user.joined_at.strftime('%d/%m/%Y %H:%M:%S'))
    embed.add_field(name="joined Discord", value=user.created_at.strftime('%d/%m/%Y %H:%M:%S'))

    await ctx.send(embed=embed)

# serverinfo
@client.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Serverinfo of " + str(guild.name), description="Serverinfo", timestamp=datetime.datetime.utcnow())

    embed.set_thumbnail(url=str(guild.icon_url))
    embed.set_footer(text=str(guild.name), icon_url=str(guild.icon_url))

    embed.add_field(name="Server ID", value=str(guild.id))
    embed.add_field(name="Members", value=str(guild.member_count))
    embed.add_field(name="Roles", value=len(guild.roles))
    embed.add_field(name="Channels [" + str(len(guild.channels)) + "]", value="Text Channels: " + str(len(guild.text_channels)) + "\n Voice Channels: " + str(len(guild.voice_channels)) + "\n categories: " + str(len(guild.categories)))
    embed.add_field(name="emotes", value=len(guild.emojis))
    embed.add_field(name="ban count", value=len(await guild.bans()))
    embed.add_field(name="Server Boosts", value=guild.premium_subscription_count)
    embed.add_field(name="Boost Level", value=guild.premium_tier)
    embed.add_field(name="Server created at", value=guild.created_at.strftime('%d/%m/%Y %H:%M:%S'))
    embed.add_field(name="Server Region", value=str(guild.region))
    embed.add_field(name="Server owner", value="<@!" + str(guild.owner_id) + ">")

    await ctx.send(embed=embed)

# mute Member
@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member, reason=None):
    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name='Muted')

    if not muted_role:
        muted_role = await guild.create_role(name='Muted')
        
        for channel in guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)

    await user.add_roles(muted_role, reason=reason)
    await ctx.send(f'{user.mention} was muted because of "{reason}"')
    await user.send(f'Hey, du wurdest auf dem Server {guild.name} wegen "{reason}" gemuted! Bitte schau dass wenn du wieder entmuted wurdest, du die Regeln befolgst. Danke :thumbsup:')
    mod_log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(title="User muted",
                        colour=discord.Colour(0xd89600),
                        timestamp=datetime.datetime.utcnow())

    embed.set_author(name=str(user),
                    icon_url=str(user.avatar_url))

    embed.set_footer(text=str(user),
                    icon_url=str(user.avatar_url))

    embed.add_field(name="muted user:",
                    value=str(user))

    embed.add_field(name="gemuted von:",
                    value=str(ctx.message.author))

    await mod_log_channel.send(embed=embed)

# unmute Member
@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, user: discord.Member, reason=None):
    guild=ctx.guild
    muted_role = discord.utils.get(guild.roles, name='Muted')
    await user.remove_roles(muted_role)
    await ctx.channel.send(f'{user.mention}, you are now unmuted! Please follow the rules in the future, thanks!')
    await user.send(f'Hey {user}, you are now unmuted on the {guild} Server! Please follow the rules in the future, thanks!')
    mod_log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(title="User unmuted",
                        colour=discord.Colour(0x37ad00),
                        timestamp=datetime.datetime.utcnow())

    embed.set_author(name=str(user),
                    icon_url=str(user.avatar_url))

    embed.set_footer(text=str(user),
                    icon_url=str(user.avatar_url))

    embed.add_field(name="unmuted user:",
                    value=str(user))

    embed.add_field(name="unmuted von:",
                    value=str(ctx.message.author))

    await mod_log_channel.send(embed=embed)

# VCMute Member
@client.command()
@commands.has_permissions(manage_roles=True)
async def vcmute(ctx, user: discord.Member, reason=None):
    guild = ctx.guild
    vcmuted_role = discord.utils.get(guild.roles, name='VCMuted')

    if not vcmuted_role:
        vcmuted_role = await guild.create_role(name='VCMuted')
        
        for channel in guild.channels:
            await channel.set_permissions(vcmuted_role, speak=False)

    await user.add_roles(vcmuted_role, reason=reason)
    await ctx.send(f'{user.mention} was vcmuted because of "{reason}"')
    await user.send(f'Hey, du wurdest auf dem Server {guild.name} wegen "{reason}" für voice channels gemuted! In Text channels kannst du nach wie vor Nachrichten senden :wink:. Bitte schau dass wenn du wieder enmuted wurdest, du die Regeln befolgst. Danke :thumbsup:')
    mod_log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(title="User voice-muted",
                        colour=discord.Colour(0xd89600),
                        timestamp=datetime.datetime.utcnow())

    embed.set_author(name=str(user),
                    icon_url=str(user.avatar_url))

    embed.set_footer(text=str(user),
                    icon_url=str(user.avatar_url))

    embed.add_field(name="voice-muted user:",
                    value=str(user))

    embed.add_field(name="voice-muted von:",
                    value=str(ctx.message.author))

    await mod_log_channel.send(embed=embed)
    
# unVCmute Member
@client.command()
@commands.has_permissions(manage_roles=True)
async def unvcmute(ctx, user: discord.Member, reason=None):
    guild=ctx.guild
    vcmuted_role = discord.utils.get(guild.roles, name='VCMuted')
    await user.remove_roles(vcmuted_role)
    await ctx.channel.send(f'{user.mention}, you are now unmuted! Please follow the rules in the future, thanks!')
    await user.send(f'Hey{user}, you are now unmuted on the {guild} Server! Please follow the rules in the future, thanks!')
    mod_log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(title="user unmuted (voice)",
                        colour=discord.Colour(0x37ad00),
                        timestamp=datetime.datetime.utcnow())

    embed.set_author(name=str(user),
                    icon_url=str(user.avatar_url))

    embed.set_footer(text=str(user),
                    icon_url=str(user.avatar_url))

    embed.add_field(name="(voice) unmuted user:",
                    value=str(user))

    embed.add_field(name="(voice) unmuted von:",
                    value=str(ctx.message.author))

    await mod_log_channel.send(embed=embed)

# Ban Member
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, reason=None):
    await user.ban(reason=reason)
    await ctx.send(f'{user.mention} was banned!')
    mod_log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(title="User banned",
                        colour=discord.Colour(0xde0004),
                        timestamp=datetime.datetime.utcnow())

    embed.set_author(name=str(user),
                    icon_url=str(user.avatar_url))

    embed.set_footer(text=str(user),
                    icon_url=str(user.avatar_url))

    embed.add_field(name="gebannter user:",
                    value=str(user))

    embed.add_field(name="gebannt von:",
                    value=str(ctx.message.author))

    await mod_log_channel.send(embed=embed)

# Unban Member
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, user):
    bannedUsers = await ctx.guild.bans()
    name, discrimator = user.split('#')

    for ban in bannedUsers:
        user = ban.user

        if(user.name, user.discriminator) == (name, discrimator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} was unbanned!')
            mod_log_channel = client.get_channel(mod_log_channel_id)
            embed = discord.Embed(title="User unbanned",
                                colour=discord.Colour(0x37ad00),
                                timestamp=datetime.datetime.utcnow())

            embed.set_author(name=str(user),
                            icon_url=str(user.avatar_url))

            embed.set_footer(text=str(user),
                            icon_url=str(user.avatar_url))

            embed.add_field(name="unbanned user:",
                            value=str(user))

            embed.add_field(name="unbanned von:",
                            value=str(ctx.message.author))

            await mod_log_channel.send(embed=embed)
        return

# Kick Member
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, reason=None):
    await user.kick(reason=reason)
    await ctx.send(f'{user.mention} was kicked!')
    mod_log_channel = client.get_channel(mod_log_channel_id)
    embed = discord.Embed(title="User gekickt",
                        colour=discord.Colour(0xde0004),
                        timestamp=datetime.datetime.utcnow())

    embed.set_author(name=str(user),
                    icon_url=str(user.avatar_url))

    embed.set_footer(text=str(user),
                    icon_url=str(user.avatar_url))

    embed.add_field(name="gekickter user:",
                    value=str(user))

    embed.add_field(name="gekickt von:",
                    value=str(ctx.message.author))

    await mod_log_channel.send(embed=embed)

# watch Avatar
@client.command()
async def av(ctx, user: discord.Member):
    embed = discord.Embed(timestamp=datetime.datetime.utcnow())

    embed.set_image(url=str(user.avatar_url))

    embed.set_author(name='This is the avatar of ' + str(user.name), icon_url=str(user.avatar_url))

    embed.set_footer(text=str(user),
                    icon_url=str(user.avatar_url))

    await ctx.send(embed=embed)

# login
@client.event
async def on_ready():
    print("Bot Logged in successfully\n")
    welcome_channel = client.get_channel(welcome_channel_id)
    await welcome_channel.send("i'm now online :)")
    while not client.is_closed():
        await client.change_presence(status=discord.Status.online, activity=discord.Game('coded by Platt'))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.online, activity=discord.Game('YT: Platt - Brawl Stars (https://www.youtube.com/channel/UCBlg3iOMUCzyixFArn9lKBw)'))
        await asyncio.sleep(10)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f'on {len(client.guilds)} servers | p!'))
        await asyncio.sleep(10)

# message got posted
@client.event
async def on_message(message):
    if not message.author == client.user:
        platt_guild = client.get_guild(platt_guild_id)
        if message.guild == platt_guild:
            print('Neue Nachricht von ' + str(message.author) + " auf Platt's Server enthält:\"" + str(message.content) + '"\n')
            message_log_channel = client.get_channel(message_log_channel_id)
            embed = discord.Embed(title="Neue Nachricht",
                                colour=discord.Colour(0x37ad00),
                                timestamp=datetime.datetime.utcnow())

            embed.set_author(name=str(message.author),
                            icon_url=str(message.author.avatar_url))

            embed.set_footer(text=str(message.guild),
                            icon_url=str(message.guild.icon_url))

            embed.add_field(name="neue Nachricht von " + str(message.author) + " in #" + str(message.channel) + " enthält:",
                            value=str(message.content))

            await message_log_channel.send(embed=embed)
        else:
            print('Neue Nachricht von ' + str(message.author) + " aus den dm's enthält:\"" + str(message.content) + '"\n')

    if message.content.startswith(prefix + 'help'):
        await message.channel.send("sorry, i don't want to help you :rofl:")
    
    if message.content.startswith('<@!772888301942210571>'):
        await message.channel.send('Hello <@!' + str(message.author.id) + '>, whats up? My prefix is "p!".')

    if message.content.startswith(prefix + 'reactionRoleTest'):
        global channel
        welcome_channel = client.get_channel(welcome_channel_id)
        message = await welcome_channel.send('React with :thumbsup: for role')
        await message.add_reaction('👍')
        channel = message.channel
    await client.process_commands(message)

# message got edited
@client.event
async def on_message_edit(before, after):
  if not before.author == client.user:
    platt_guild = client.get_guild(platt_guild_id)
    if before.guild == platt_guild:
      print('Nachricht von ' + str(after.author) + " auf Platt's Server wurde bearbeitet\n")
      message_log_channel = client.get_channel(message_log_channel_id)
      embed = discord.Embed(title="Nachricht in #" + str(before.channel) + " wurde bearbeitet",
      colour=discord.Colour(0xd89600),
      timestamp=datetime.datetime.utcnow())

      embed.set_author(name=str(before.author), icon_url=str(before.author.avatar_url))

      embed.set_footer(text=str(before.author), icon_url=str(before.author.avatar_url))

      embed.add_field(name="Nachricht vorher: ", value=str(before.content))

      embed.add_field(name="bearbeitete Nachricht: ", value=str(after.content))

      await message_log_channel.send(embed=embed)
    else:
      print('Nachricht von ' + str(after.author) + " aus den dm's wurde bearbeitet\n")

# message got deleted
@client.event
async def on_message_delete(message):
    if not message.author == client.user:
        platt_guild = client.get_guild(platt_guild_id)
        if message.guild == platt_guild:
            print('Nachricht von ' + str(message.author) + " auf Platt's Server mit dem folgenen Inhalt wurde gelöscht:" + '"' + str(message.content) + '"\n')
            message_log_channel = client.get_channel(message_log_channel_id)
            embed = discord.Embed(title="Nachricht gelöscht",
                                colour=discord.Colour(0xde0004),
                                timestamp=datetime.datetime.utcnow())

            embed.set_author(name=str(message.author),
                            icon_url=str(message.author.avatar_url))

            embed.set_footer(text=str(message.guild),
                            icon_url=str(message.guild.icon_url))

            embed.add_field(name="Nachricht von " + str(message.author) + " in #" + str(message.channel) + " mit dem folgenden Inhalt wurde gelöscht:",
                            value=str(message.content))

            await message_log_channel.send(embed=embed)
        else:
            print('Nachricht von ' + str(message.author) + " aus den dm's mit dem folgenen Inhalt wurde gelöscht:" + '"' + str(message.content) + '"\n')

# reaction role
@client.event
async def on_reaction_add(reaction, user):
    global channel
    if user == client.user:
        return

    if reaction.message.channel == channel and reaction.emoji == "👍":
        role = reaction.message.guild.get_role(818172496724885586)
        await user.add_roles(role)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    await ctx.send(f"This command is on cooldown, try again after {round(error.retry_after)} seconds.")


# running webserver
keep_alive()
client.run(os.getenv("BOT_TOKEN"))