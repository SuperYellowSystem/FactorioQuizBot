import datetime
import discord
from discord.ext import commands as cmds
from fuzzywuzzy import fuzz

from cogs.utils import checks

import logging
logger = logging.getLogger(__name__)


class FAQCog:
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Frequently Asked Questions"

    def tags(self):
        tags = []
        for faq in self.bot.db.faqs:
            tags.append(faq["tag"])
        return tags

    def search_faq(self, guild_id, query):
        try:
            return next(faq for faq in self.bot.db.faqs if faq["guild_id"] == guild_id and faq["tag"] == query)
        except StopIteration as e:
            logger.warning("faq not found", e)
        except Exception as e:
            logger.error(e)

    @staticmethod
    async def check_image(ctx, faq, name, link=""):
        if not link:
            link = name
        if name[-3:] in ['png', 'jpg', 'gif'] or name[-4:] in ['jpeg']:
            faq["image"] = link
            return True
        else:
            em = discord.Embed(title="Error",
                               description="An invalid image was used."
                                           "The supported formats are `png`, `jpg`, `jpeg` & `gif`",
                               colour=0xDC143C)
            # em.set_footer(text=bot.user.name,
            #               icon_url=f"https://cdn.discordapp.com/avatars/{bot.user.id}/{bot.user.avatar}.png?size=64")
            await ctx.send(embed=em)
            return False

    def embed_faq(self, ctx, query, title=None, color=None):
        faquery = self.search_faq(ctx.guild.id, query)
        if not title:
            title = query.title()
        if not color:
            color = 0xDFDE6E
        content = faquery["content"]
        image = faquery["image"]
        timestamp = datetime.datetime.strptime(faquery["timestamp"], "%Y-%m-%d %H:%M:%S %Z")
        author = self.bot.get_user(int(faquery["creator"]))
        author_name = ctx.guild.get_member(author.id).display_name
        if author.avatar:
            author_pic = f"https://cdn.discordapp.com/avatars/{author.id}/{author.avatar}.png?size=64"
        else:
            author_pic = "https://cdn.discordapp.com/embed/avatars/0.png"
        em = discord.Embed(title=title,
                           description=content,
                           timestamp=timestamp,
                           colour=color)
        if image:
            em.set_image(url=image)
        em.set_author(name=author_name, icon_url=author_pic)
        # em.set_footer(text=bot.user.name,
        #               icon_url=f"https://cdn.discordapp.com/avatars/{bot.user.id}/{bot.user.avatar}.png?size=64")
        return em

    @cmds.group(name="faq", aliases=["tag", "tags", "faw"], invoke_without_command=True)
    async def faq_command(self, ctx, *, query: str=""):
        """
        Shows the list of available FAQ tags.
        """
        query = query.lower()
        if not query:
            faqstr = self.tags()
            faqstr.sort()
            em = discord.Embed(title="List of FAQ tags",
                               description=', '.join(faqstr).title(),
                               colour=0xDFDE6E)

        elif self.search_faq(ctx.guild.id, query):
            em = self.embed_faq(ctx, query)

        else:
            close_items = []
            for item in self.tags():
                if fuzz.ratio(query, item) >= 75:
                    close_items.append(item.title())
            if len(close_items) > 0:
                if len(close_items) == 1:
                    em = self.embed_faq(ctx, close_items[0].lower(),
                                        title=f"Could not find \"{query.title()}\" "
                                              f"in FAQ tags. Did you mean \"{close_items[0]}\"?",
                                        color=0xFF8C00)
                else:
                    em = discord.Embed(title=f"Could not find \"{query.title()}\" in FAQ tags.",
                                       description=f"Did you mean {', '.join(close_items)}?",
                                       colour=0xFF8C00)
            else:
                em = discord.Embed(title="Error",
                                   description=f"Could not find \"{query.title()}\" "
                                               f"or any similarly named tags in FAQ tags.",
                                   colour=0xDC143C)
                em.set_footer(text=f"To see the list of all available FAQ tags, use {ctx.prefix}faq",
                              icon_url=f"https://cdn.discordapp.com/avatars/{self.bot.user.id}/"
                                       f"{self.bot.user.avatar}.png?size=64")
        await ctx.send(embed=em)

    @faq_command.command(name="add", aliases=["edit"])
    @checks.is_admin()
    async def faq_add(self, ctx, title: str, *, content: str = ""):
        """
        Add a new tag to the FAQ tags.
        Can add an image by either attaching it to the message, or using ~~ imageurl at the end.
        """
        updatebool = True
        title = title.lower()
        try:
            image_url = content.split('~~')[1].strip()
            content = content.split('~~')[0].strip()
        except IndexError:
            image_url = ""
        if len(title) > 256:
            em = discord.Embed(title="Error",
                               description="The title inputted is too long.\n"
                                           "The maximum title length is 256 characters.",
                               colour=0xDC143C)
            await ctx.send(embed=em)
            return
        if (not content and
                not ctx.message.attachments and
                not image_url):
            em = discord.Embed(title="Error",
                               description="Content is required to add an FAQ tag.",
                               colour=0xDC143C)
            # em.set_footer(text=self.bot.user.name, icon_url=f"https://cdn.discordapp.com/avatars/
            #               {self.bot.user.id}/{self.bot.user.avatar}.png?size=64")
            await ctx.send(embed=em)
            return

        else:
            currentfaq = {"guild_id": ctx.guild.id,
                          "tag": title,
                          "content": content,
                          "image": "",
                          "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                          "creator": str(ctx.message.author.id)}

            if image_url:
                if not await self.check_image(ctx, currentfaq, image_url):
                    updatebool = False
            elif ctx.message.attachments:
                attached_file = ctx.message.attachments[0]
                attached_file_name = attached_file.filename.lower()
                if not await self.check_image(ctx, currentfaq, attached_file_name, attached_file.url):
                    updatebool = False

        if updatebool:
            # check if tag existed
            for faq in self.bot.db.faqs:
                if title == faq["tag"] and ctx.guild.id == faq["guild_id"]:
                    currentfaq.update({"creator": faq["creator"]})
                    self.bot.db.edit_faq(currentfaq)
                    faq.update(currentfaq)
                    embed_title = f"Successfully edited \"{title.title()}\" in database"
                    break
            else:
                self.bot.db.save_faq(currentfaq)
                self.bot.db.faqs.append(currentfaq)
                embed_title = f"Successfully added \"{title.title()}\" to database"

            await ctx.send(embed=self.embed_faq(ctx, title, embed_title, 0x19B300))

    @faq_command.command(name="remove", aliases=["delete"])
    @checks.is_admin()
    async def faq_remove(self, ctx, *, title: str):
        """
        Remove a tag from the FAQ tags.
        """
        title = title.lower()
        faquery = self.search_faq(ctx.guild.id, title)
        if faquery:
            em = self.embed_faq(ctx=ctx,
                                query=title,
                                title=f"Successfully removed \"{title.title()}\" from FAQ tags.",
                                color=0xDC143C)
            self.bot.db.faqs = [faq
                                for faq in self.bot.db.faqs
                                if ctx.guild.id != faq["guild_id"] or title != faq["tag"]]
            self.bot.db.delete_faq(ctx.guild.id, title)
        else:
            em = discord.Embed(title="Error",
                               description="Query not in FAQ tags.",
                               colour=0xDC143C)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(FAQCog(bot))
