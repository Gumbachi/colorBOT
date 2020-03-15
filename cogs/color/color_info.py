import io

import discord
from discord.ext import commands

from classes import Guild
from functions import is_disabled
from authorization import authorize


class ColorInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="colors", aliases=["colours", "c"])
    async def show_colors(self, ctx):
        """Display an image of equipped colors."""
        authorize(ctx, "color")

        guild = Guild.get(ctx.guild.id)
        fp = io.BytesIO(guild.draw_colors())

        # send info to channel or user
        if is_disabled(ctx.channel):
            await ctx.message.delete()
            await ctx.author.send(content=f"**{ctx.guild.name}**:",
                                  file=discord.File(fp, filename="colors.png"))
        else:
            await ctx.send(file=discord.File(fp, filename="colors.png"))

    @commands.command(name="info", aliases=["about"])
    async def show_color_info(self, ctx, *, query):
        authorize(ctx, "colors")
        guild = Guild.get(ctx.guild.id)

        color = guild.find_color(query, threshold=0)

        members = (member.name for member in color.members)
        color_embed = discord.Embed(
            title=color.name,
            description=(f"Hexcode: {color.hexcode}\n"
                         f"RGB: {color.rgb}\n"
                         f"Members: {', '.join(members)}\n"
                         f"Index: {color.index}\n"
                         f"Role ID: {color.role_id}"),
            color=discord.Color.from_rgb(*color.rgb))

        # manage recipient and cleanup if needed
        if is_disabled(ctx.channel):
            await ctx.message.delete()
            await ctx.author.send(embed=color_embed)  # to user
        else:
            await ctx.send(embed=color_embed)


def setup(bot):
    bot.add_cog(ColorInfo(bot))
