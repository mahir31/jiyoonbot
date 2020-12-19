import discord
from discord.ext import commands


class helpembeds(commands.HelpCommand):
    
    COLOUR = int('4eca58', 16)

    def add_aliases(self, embed, mapping):
        if mapping.aliases:
            embed.set_footer(text='Aliases: ' + ', '.join(mapping.aliases))

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='All Commands', colour=self.COLOUR)
        description = self.context.bot.description
        if description:
            embed.description = description
        
        for cog, bot_commands in sorted(mapping.items(), key=lambda x: len(x[1]), reverse=True):
            if cog is None:
                name = 'Other'
            else:
                name = cog.qualified_name
            commandlist = await self.filter_commands(bot_commands, sort=True)
            if commandlist:
                value = '\n'.join(f'`{self.clean_prefix}{c.name}`' for c in bot_commands)
                embed.add_field(name=name, value=value)
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f'{cog.qualified_name}', colour=self.COLOUR)
        if cog.description:
            embed.description = cog.description
        commandlist = await self.filter_commands(cog.get_commands(), sort=True)
        for command in commandlist:
            embed.add_field(
                name=f'`{self.get_command_signature(command)}`',
                value='> ' + (command.short_doc or 'command has no description'),
                inline=False,
            )
        await self.get_destination().send(embed=embed)
    
    async def send_group_help(self, group):
        embed = discord.Embed(title=f'{group.qualified_name}', colour=self.COLOUR)
        if group.help:
            embed.description = group.help
        elif group.short_doc:
            embed.description = group.short_doc
        
        if isinstance(group, commands.Group):
            commandlist = await self.filter_commands(group.commands, sort=False)
            for command in commandlist:
                    embed.add_field(
                    name=f'`{self.get_command_signature(command)}`',
                    value='> ' + (command.short_doc),
                    inline=False
                )
        await self.get_destination().send(embed=embed)
    
    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f'`{self.get_command_signature(command)}`',
            colour=self.COLOUR
        )
        self.add_aliases(embed, command)
        embed.description = ''
        if command.brief:
            embed.description += command.brief
        if command.help:
            embed.description += f'```{command.help.format(prefix=self.clean_prefix)}```'
        await self.get_destination().send(embed=embed)
    
    async def group_help_brief(self, ctx, group):
        embed = discord.Embed(colour=self.COLOUR)
        embed.description = '`' + ctx.prefix + group.qualified_name
        embed.description = f' [{" | ".join(c.name for c in group.commands)}]`'
        embed.set_footer(text=f'Use {ctx.prefix}help {group.qualified_name} for more details')
        await ctx.send(embed=embed)