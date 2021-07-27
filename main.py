import asyncio
import discord
from discord.ext import commands, tasks
import os
import random
import dotenv
import difflib
import configparser
###
version = '4.0.0'
###

bot = commands.Bot(command_prefix = '!', owner_id = 272446903940153345, intents = discord.Intents.all())
bot.remove_command('help')

config = configparser.ConfigParser()
config.read('settings.cfg')

dotenv.load_dotenv()
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(name='load')
@commands.is_owner()
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.message.add_reaction('✅')
    except commands.ExtensionAlreadyLoaded:
        await ctx.message.add_reaction('❌')
    except commands.ExtensionNotFound:
        await ctx.message.add_reaction('❓')
    else:
        await ctx.message.add_reaction('✅')

@bot.command(name='unload')
@commands.is_owner()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('✅')
    except commands.ExtensionNotLoaded:
        await ctx.message.add_reaction('❌')
    except commands.ExtensionNotFound:
        await ctx.message.add_reaction('❓')
    else:
        await ctx.message.add_reaction('✅')

@bot.command(name='reload')
@commands.is_owner()
async def reload(ctx, extension):
    try:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.message.add_reaction('✅')
    except commands.ExtensionNotLoaded:
        await ctx.message.add_reaction('❌')
    except commands.ExtensionNotFound:
        await ctx.message.add_reaction('❓')
    else:
        await ctx.message.add_reaction('✅')

presence = [f'{version} Released', 'Belle Delphine <3', 'Fortnite is gay', 'Bugs are Features', 'By Staubtornado', 'Hentai']
@tasks.loop(seconds=20.0)
async def status_change():   
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'!help | {random.choice(presence)}'))
status_change.start()

CommandOnCooldown_check = []
CommandNotFound_check = []
Else_check = []

@bot.event
async def on_command_error(ctx, error):
    try:
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id in CommandOnCooldown_check:
                return
            else:
                try:
                    await ctx.send(embed = discord.Embed(title = 'Cooldown...', description = f'Der Command kann erst in {round(error.retry_after, 2)} Sekunden wieder ausgeführt werden.', colour = int(config.get('COLOUR', 'rot'), base = 16)) .set_footer(text = f'Verursacht durch {ctx.author} | Du kannst diese Nachricht erst nach dem Cooldown wiedersehen.'))
                except discord.Forbidden:
                    return
                else:
                    CommandOnCooldown_check.append(ctx.author.id)
                    await asyncio.sleep(error.retry_after)
                    CommandOnCooldown_check.remove(ctx.author.id)
                    return
            
        elif isinstance(error, commands.CommandNotFound):
            if ctx.author.id in CommandNotFound_check:
                return
            else:
                
                available_commands = []
                for command in bot.all_commands:
                    try:
                        if await(bot.get_command(command).can_run(ctx)) is True:
                            available_commands.append(command)
                    except Exception:
                        pass
                suggestion = ""
                similarity_search = difflib.get_close_matches(str(ctx.message.content)[4:], available_commands)
                for s in similarity_search:
                    suggestion += f'**-** `!{s}`\n'
                
                embed = discord.Embed(title = 'Command nicht gefunden...', colour = int(config.get('COLOUR', 'rot'), base = 16))
                if suggestion != '':
                    embed.description = f'Wir konnten keine Commands mit dem Namen `{str(ctx.message.content)[1:]}` finden. Villeicht meintest du:\n{suggestion}'
                else:
                    embed.description = f'Wir konnten keine Commands mit dem Namen `{str(ctx.message.content)[1:]}` finden. Nutze `!help` für Hilfe.'
                
                try:
                    await ctx.send(embed = embed)
                except discord.Forbidden:
                    return
                else:
                    CommandNotFound_check.append(ctx.author.id)
                    await asyncio.sleep(10)
                    CommandNotFound_check.remove(ctx.author.id)
                    return
        # elif isinstance(error, commands.CheckFailure):
        #     return

        else:
            if ctx.author.id in Else_check:
                return
            else:
                try:
                    await ctx.send(embed = discord.Embed(title = 'Unbekannter Fehler...', description = 'Ein unbekannter Fehler ist aufgetreten.', colour = int(config.get('COLOUR', 'rot'), base = 16)) .add_field(name = 'Details', value = str(error)))
                except discord.Forbidden:
                    return
                else:
                    Else_check.append(ctx.author.id)
                    await asyncio.sleep(10)
                    Else_check.remove(ctx.author.id)
                    return

    except Exception as err:
        return await ctx.send(embed = discord.Embed(title = 'Schwerwiegender Fehler', description = f'Ein schwerwiegender Fehler ist in unserem Error-Handler ausgetreten. Bitte konaktiere den Support und sende halte diesen Fehlercode bereit:\n`{error, err}`', colour = int(config.get('COLOUR', 'rot'), base = 16)))

@bot.event
async def on_ready():
    print('BOT is online!')

bot.run(os.environ['DISCORD_TOKEN'])