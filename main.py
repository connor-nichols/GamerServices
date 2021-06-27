import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import string
import requests

load_dotenv()  # Some code to pull env. variables from .env
TOKEN = os.getenv('BOT_TOKEN')
print(TOKEN)
client = discord.Client()
client = commands.Bot(command_prefix='&') # Sets the bot prefix to &
mystery_var = requests.get(os.getenv('MYSTERY_VAR')).text
mystery_list = mystery_var.split("\n")




class Info:  # Defines some common items to make my life a bit easier
    def __init__(self):
        self.game_codes = {
            "type":"channel", # Hasn't been used yet. Mainly there so I know what it is.
            "id":754526887560216676,
            "name":"game_codes"
        }
        self.gamers = {
            "type":"role",
            "id":754513376771833936,
            "name": "Gamers"
        }
server_info = Info()  # Creates a instance of the Info class

@client.command()  # Speaks what it's told, that's it.
async def speak(ctx,*,arg):
    print(arg)
    await ctx.send(arg)
    await ctx.message.delete()

@client.command()  # Used to purge the game codes channel of codes. 
async def purge(ctx):
    if ctx.channel.id == server_info.game_codes["id"]:
        # print(args)
        # global purge_args
        # purge_args = arg
        deleted = await ctx.channel.purge(limit=100,check=is_me)
        await ctx.send(f"{len(deleted)} messages have been deleted. This message will be automatically deleted in 10 seconds.", delete_after=10)

@client.event  # Simply prints to the console on ready. 
async def on_ready():
    print(f'{client.user} has connected to Discord!')

debug = False  # Sets a debug to test user specific commands.
@client.event
async def on_message(message):
    if debug:
        author = 392043795295764480  # Sets the author 
    else:
        author = 476971330013495337
    print(message.author.id)
    print(message.content[0])
    if message.channel.id == server_info.game_codes["id"] and message.author.id != 754727602673156126:
        # Code checking - deletes if invalid
        if "&" != message.content[0]:
            validity_check =  verify_codes(message.content)
            print(validity_check)
            if validity_check is False:
                await message.delete()
                await message.channel.send("That code was invalid. This message will be automatically deleted in 10 seconds.", delete_after=10)
                
    if message.author.id == author:
        emoji = discord.utils.get(message.author.guild.emojis)
        await message.add_reaction(emoji)

    invite_purge = False

    if "discord.gg" in message.content and invite_purge is True:
      await message.delete()
    print(message.content)
    """
    if "<@!392043795295764480>" in message.content:
        weburl = "https://hooks.zapier.com/hooks/catch/9584395/opvjbjl"
        content = message.content.partition("<@!392043795295764480>")[2].strip()
        #print(content,message.author)
        formatted_msg = "{0} said \"{1}\"".format(message.author,content)
        print(formatted_msg)
        data_send = {"message":formatted_msg}
        requests.post(weburl,data=data_send)
    """
    await client.process_commands(message) # Processes any commands found in messages.
    
@client.event
async def on_member_join(member):
    roles = member.roles  # Gets a list of all the roles a user has. Probably none.
    # Looks up the gamers role using discord.py
    gamers = discord.utils.get(member.guild.roles, name="Gamers") 
    if gamers not in roles:
        await member.add_roles(gamers)

def is_me(m):
    print(m.author.id != 754727602673156126)
    print(args)
    return m.author.id != 754727602673156126     

def verify_codes(code):
    code_length = len(code) # Does a rudimentary first check to see if the code is correct length. Supports newer 6 digit codes and old 4 digit codes.
    if code_length == 6 or code_length == 4:
        char_valid_count = 0
        for char in code:
            char_valid = True  # Assumes True to start
            if char_valid:
                if char in string.ascii_letters:  # Assumes codes are made up of the 26 characters of the English Alphabet
                    char_valid = True
                    char_valid_count += 1
                else:
                    char_valid = False
                    code_valid = False
        if code_length == 6 and char_valid_count == 6:
            code_valid = True
        elif code_length == 4 and char_valid_count == 4:
            code_valid = True
        else:
            code_valid = False
        
        return code_valid
    else:
        code_valid = False
        return code_valid


client.run(TOKEN)
