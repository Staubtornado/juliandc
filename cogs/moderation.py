import asyncio
import discord
from discord import colour
from discord.ext import commands
import discord.utils
import configparser

#embed = discord.Embed(title = 'Fehler', description = 'Die Anzahl an Nachrichten muss zwischen 1 und 100 liegen.', colour = int(config.get('COLOUR', 'rot'), base = 16))

config = configparser.ConfigParser()
config.read('settings.cfg')

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def clear(self, ctx, *, amount = 10):
        if amount <= 0 or amount > 100:
            return await ctx.send('The amount must be between 1 and 100.')
        else:
            return await ctx.channel.purge(limit = amount)

    @commands.command()
    async def mute(self, ctx, member: discord.Member, *, reason = None):
        confirmation = await ctx.send(embed = discord.Embed(title = 'Bestätigung...', description = f'Möchtest du {member.mention} wirklich muten? Die Person wird keine Text- und Sprachchannel mehr nutzen können.', colour = int(config.get('COLOUR', 'rot'), base = 16)))
        await confirmation.add_reaction('✅')
        await confirmation.add_reaction('❌')

        def check(reaction, user):
            if user == ctx.author and reaction.message == confirmation and str(reaction.emoji) == '✅':
                return user == ctx.author and reaction.message == confirmation and str(reaction.emoji) == '✅'
        
            if user == ctx.author and reaction.message == confirmation and str(reaction.emoji) == '❌':
                return user == ctx.author and reaction.message == confirmation and str(reaction.emoji) == '❌'
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout = 60.0, check = check)
        except asyncio.TimeoutError:
            await confirmation.delete
            return await ctx.send(embed = discord.Embed(title = 'Abgebrochen...', description = f'Es erfolge keine Bestätigung seitens des Moderators innerhalb von 60 Sekunden. {member.mention} wurde nicht gemuted.', colour = int(config.get('COLOUR', 'rot'), base = 16)))
        else:
            if user == ctx.author and reaction.message == confirmation and str(reaction.emoji) == '✅':
                role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not role:
            role = await ctx.guild.create_role(name="Muted")
                                                                                                                                                                                     
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, speak=False, connect=False, send_messages=False, read_message_history=True, read_messages=False)
        
        await member.add_roles(role, reason=reason)
        await member.send(embed = discord.Embed(title = 'Muted...', description = f'Du wurdest im {ctx.guild.name} gemuted.', colour = int(config.get('COLOUR', 'rot'), base = 16)) .add_field(name = 'Moderator', value = ctx.author.mention, inline = False) .add_field(name = 'Details', value = reason, inline = False))
        
        return await ctx.send(embed = discord.Embed(title = 'Erfolg...', description = f'{member.mention} wurde erfolgreich gemuted.', colour = int(config.get('COLOUR', 'rot'), base = 16)))

    @commands.command(name = 'ban')
    @commands.has_any_role('Kaiser', 'König')
    async def mute(self, ctx, member: discord.Member, *, reason = None):
        confirmation = await ctx.send(embed = discord.Embed(title = 'Bestätigung...', description = f'Möchtest du {member.mention} wirklich bannen? Alle seine Nachrichten der letzten 14 Tage werden gelöscht und er verliert Zugriff auf diesen Server.', colour = int(config.get('COLOUR', 'rot'), base = 16)) .set_footer(text = 'Der Grund wird dem Nutzer mitgeteilt.'))
        await confirmation.add_reaction('✅')
        await confirmation.add_reaction('❌')

    @commands.command()
    async def test(self, ctx):
        if 'mute' in "{'join': <discord.ext.commands.core.Command object at 0x00000235A256E910>, 'summon': <discord.ext.commands.core.Command object at 0x00000235A256E700>, 'leave': <discord.ext.commands.core.Command object at 0x00000235A4021850>, 'disconnect': <discord.ext.commands.core.Command object at 0x00000235A4021850>, 'volume': <discord.ext.commands.core.Command object at 0x00000235A4021490>, 'now': <discord.ext.commands.core.Command object at 0x00000235A4035310>, 'current': <discord.ext.commands.core.Command object at 0x00000235A4035310>, 'playing': <discord.ext.commands.core.Command object at 0x00000235A4035310>, 'pause': <discord.ext.commands.core.Command object at 0x00000235A4035370>, 'pa': <discord.ext.commands.core.Command object at 0x00000235A4035370>, 'resume': <discord.ext.commands.core.Command object at 0x00000235A4035400>, 're': <discord.ext.commands.core.Command object at 0x00000235A4035400>, 'res': <discord.ext.commands.core.Command object at 0x00000235A4035400>, 'stop': <discord.ext.commands.core.Command object at 0x00000235A40352B0>, 'skip': <discord.ext.commands.core.Command object at 0x00000235A4035550>, 's': <discord.ext.commands.core.Command object at 0x00000235A4035550>, 'forceskip': <discord.ext.commands.core.Command object at 0x00000235A40355B0>, 'fs': <discord.ext.commands.core.Command object at 0x00000235A40355B0>, 'fskip': <discord.ext.commands.core.Command object at 0x00000235A40355B0>, 'queue': <discord.ext.commands.core.Command object at 0x00000235A40354F0>, 'shuffle': <discord.ext.commands.core.Command object at 0x00000235A40356A0>, 'remove': <discord.ext.commands.core.Command object at 0x00000235A4035730>, 'loop': <discord.ext.commands.core.Command object at 0x00000235A40357C0>, 'play': <discord.ext.commands.core.Command object at 0x00000235A40358B0>, 'p': <discord.ext.commands.core.Command object at 0x00000235A40358B0>, 'load': <discord.ext.commands.core.Command object at 0x00000235A40359D0>, 'unload': <discord.ext.commands.core.Command object at 0x00000235A4035A30>, 'reload': <discord.ext.commands.core.Command object at 0x00000235A4035AC0>, 'clear': <discord.ext.commands.core.Command object at 0x00000235A40E4850>, 'ban': <discord.ext.commands.core.Command object at 0x00000235A40E49A0>, 'test': <discord.ext.commands.core.Command object at 0x00000235A40E4A30>}":
            return await ctx.send('loaded')
        elif 'test' in "{'join': <discord.ext.commands.core.Command object at 0x00000235A256E910>, 'summon': <discord.ext.commands.core.Command object at 0x00000235A256E700>, 'leave': <discord.ext.commands.core.Command object at 0x00000235A4021850>, 'disconnect': <discord.ext.commands.core.Command object at 0x00000235A4021850>, 'volume': <discord.ext.commands.core.Command object at 0x00000235A4021490>, 'now': <discord.ext.commands.core.Command object at 0x00000235A4035310>, 'current': <discord.ext.commands.core.Command object at 0x00000235A4035310>, 'playing': <discord.ext.commands.core.Command object at 0x00000235A4035310>, 'pause': <discord.ext.commands.core.Command object at 0x00000235A4035370>, 'pa': <discord.ext.commands.core.Command object at 0x00000235A4035370>, 'resume': <discord.ext.commands.core.Command object at 0x00000235A4035400>, 're': <discord.ext.commands.core.Command object at 0x00000235A4035400>, 'res': <discord.ext.commands.core.Command object at 0x00000235A4035400>, 'stop': <discord.ext.commands.core.Command object at 0x00000235A40352B0>, 'skip': <discord.ext.commands.core.Command object at 0x00000235A4035550>, 's': <discord.ext.commands.core.Command object at 0x00000235A4035550>, 'forceskip': <discord.ext.commands.core.Command object at 0x00000235A40355B0>, 'fs': <discord.ext.commands.core.Command object at 0x00000235A40355B0>, 'fskip': <discord.ext.commands.core.Command object at 0x00000235A40355B0>, 'queue': <discord.ext.commands.core.Command object at 0x00000235A40354F0>, 'shuffle': <discord.ext.commands.core.Command object at 0x00000235A40356A0>, 'remove': <discord.ext.commands.core.Command object at 0x00000235A4035730>, 'loop': <discord.ext.commands.core.Command object at 0x00000235A40357C0>, 'play': <discord.ext.commands.core.Command object at 0x00000235A40358B0>, 'p': <discord.ext.commands.core.Command object at 0x00000235A40358B0>, 'load': <discord.ext.commands.core.Command object at 0x00000235A40359D0>, 'unload': <discord.ext.commands.core.Command object at 0x00000235A4035A30>, 'reload': <discord.ext.commands.core.Command object at 0x00000235A4035AC0>, 'clear': <discord.ext.commands.core.Command object at 0x00000235A40E4850>, 'ban': <discord.ext.commands.core.Command object at 0x00000235A40E49A0>, 'test': <discord.ext.commands.core.Command object at 0x00000235A40E4A30>}":
            return await ctx.send('As expected')
        else:
            return await ctx.send('Not loaded')

def setup(bot):
    bot.add_cog(moderation(bot))