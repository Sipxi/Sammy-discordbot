import discord
from discord.ext import commands
from discord.errors import Forbidden
from extensions.customCog import CustomCog
from extensions.customError import badName


# ? Global prefix for guild?
prefix = "!"
version = "1.0.0"
"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.
"""


async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send(
                "Hey, seems like I can't send embeds. Please check my permissions :)"
            )
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ",
                embed=embed,
            )


def title_embed():
    return discord.Embed(
        title="Commands and modules",
        color=discord.Color.blue(),
        description=f"Use `{prefix}help <module>` to gain more information about that module "
        f":smiley:\n",
    )


def no_permission_embed():
    return discord.Embed(
        title="What's that?!",
        description=f"What a naughty bbooooooy or girl... YOU can't use nor see this command :scream:",
        color=discord.Color.red(),
    )


def warning_embed(title, description):
    return discord.Embed(
        title=title,
        description=description,
        color=discord.Color.orange(),
    )


class Help(CustomCog):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @commands.command()
    async def help(self, ctx, *input) -> None:
        # Test for permissions
        async def predicate(cmd) -> bool:
            try:
                return await cmd.can_run(ctx)
            except commands.CommandError:
                return False

        # checks if cog parameter was given
        # if not: sending all modules and commands not associated with a cog
        if not input:
            help_message = title_embed()
            # iterating trough cogs, gathering descriptions
            cogs_desc = ""
            for cog in sorted(self.bot.cogs):
                print(cog)
                valid = False
                for command in self.bot.get_cog(cog).get_commands():
                    valid = await predicate(command)
                    # if command is not hidden and valid break
                    if not command.hidden and valid:
                        break
                if valid:
                    cogs_desc += f"`{cog}` {self.bot.cogs[cog].description}\n"

            # adding 'list' of cogs to embed
            help_message.add_field(name="Modules", value=cogs_desc, inline=False)

            # setting information about author
            help_message.add_field(
                name="About",
                value=f"The Bot's is developed by {ctx.guild.owner}, based on discord.py.\n\
                                    Please visit https://github.com/Sipxi/Sammy-discordbot to submit ideas or bugs.",
            )
            help_message.set_footer(text=f"Bot is running {version}")

        # block called when one cog-name is given
        # trying to find matching cog and it's commands
        elif len(input) == 1:
            for cog in self.bot.cogs:
                if cog.lower() == input[0].lower():
                    help_message = title_embed()
                    # getting commands from cog
                    for command in self.bot.get_cog(cog).get_commands():
                        valid = await predicate(command)
                        # if cog is not hidden
                        if not command.hidden and valid:
                            help_message.add_field(
                                name=f"`{prefix}{command.name}`",
                                value=command.help,
                                inline=False,
                            )
                            # send no permissions messege
                        else:
                            help_message = no_permission_embed()
                    break
            # If input not found
            else:
                try:
                    for cog in self.bot.cogs:
                        for command in self.bot.get_cog(cog).get_commands():
                            if command.name.lower() == input[0].lower():
                                raise StopIteration
                    else:
                        raise badName
                # If found a command
                except StopIteration:
                    valid = await predicate(command)
                    if not command.hidden and valid:
                        # making title - getting description from doc-string below class
                        help_message = discord.Embed(
                            title=f"{command.name} - Commands",
                            description=(command.description),
                            color=discord.Color.green(),
                        )
                        # send no permissions messege
                    else:
                        help_message = no_permission_embed()
                # If didn't find command and cog
                except badName:
                    title = "What's that?!"
                    description = f"I've never heard from a module called `{input[0]}` before :scream:"
                    help_message = warning_embed(title, description)

        # If more than one parameter
        elif len(input) > 1:
            help_message = discord.Embed(
                title="That's too much.",
                description="Please request only one module at once :sweat_smile:",
                color=discord.Color.orange(),
            )

        await send_embed(ctx, help_message)


def setup(bot):
    bot.add_cog(Help(bot))
