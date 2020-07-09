import discord
from discord.ext import commands
from pathlib import Path

import yaml

# Loads config file
config = yaml.safe_load(open(str(Path(__file__).parent.absolute() / 'config.yaml')))

# Creates bot instance: change command_prefix='<insert prefix here>'
client = commands.Bot(command_prefix='.', help_command=None)

# Simple event telling you the bot is ready
@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as: {client.user}')

# Creates roles upon bot joining the guild
@client.event
async def on_guild_join(guild):
    if config['autoCreateRoles']:
        await guild.create_role(name='13+')
        await guild.create_role(name='12-')

# DMs the user asking him if he's 13+ or not upon user joining the guild
@client.event
async def on_member_join(member):
    # Sends the message (question)
    question = '**For full access to our server please answer folowing question:\nAre you 13+?**'
    embed = discord.Embed(title=question, description=u'\U00000020')
    embed.set_author(name=f'Server {member.guild.name}', icon_url=member.guild.icon_url)
    embed.set_footer(text='Bot made by Jaro#5648 :)')
    msg = await member.send(embed=embed)
    channel = msg.channel

    # Adds reactions for the user to answer
    y_emoji = u'\U0001F1FE' # Letter Y
    n_emoji = u'\U0001F1F3' # Letter N
    await msg.add_reaction(y_emoji)
    await msg.add_reaction(n_emoji)

    # Check that tells if the emoji is YES or NO
    def rcheck(payload):
        if payload.user_id == member.id:
            if payload.channel_id == channel.id:
                payloadtest = payload
                emoji = payload.emoji
                name = emoji.name
                if name == y_emoji or name == n_emoji:
                    return True

    # Waits for the user to react to the question with Y or N
    payload = await client.wait_for('raw_reaction_add', check=rcheck, timeout=None)

    # Gets the roles by name
    role13plus = discord.utils.get(member.guild.roles, name='13+')
    role12minus = discord.utils.get(member.guild.roles, name='12-')

    # Assigns the user it's role
    if payload.emoji.name == y_emoji:
        if config['role13+']:
            await member.add_roles(role13plus)
    elif payload.emoji.name == n_emoji:
        if config['role12-']:
            await member.add_roles(role12minus)

    # The bot sends a response after assigning role to the user
    answer = '**Role has been assigned to you! You\'re welcome!**'
    newembed = discord.Embed(title=answer, description=u'\U00000020')
    newembed.set_author(name=f'Server {member.guild.name}', icon_url=member.guild.icon_url)
    newembed.set_footer(text='Bot made by Jaro#5648 :)')
    await member.send(embed=newembed)

client.run(config['token'])