import os
from twitchio.ext import commands

class TwitchBot(commands.Bot):

    def __init__(self):
        self.__channels = os.environ['CHANNEL'].split(',')
        super().__init__(
            irc_token        = os.environ['TMI_TOKEN'],
            client_id        = os.environ['CLIENT_ID'],
            nick             = os.environ['BOT_NICK'],
            prefix           = os.environ['BOT_PREFIX'],
            initial_channels = self.__channels
        )

    async def event_ready(self):
        """ The event when the bot is online!

        This function would only call once.
        """
        print(f"{os.environ['BOT_NICK']} is online!")
        ws = self._ws  # this is only needed to send messages within event_ready
        print(self.__channels)
        for channel in self.__channels:
            await ws.send_privmsg(channel, f"/me has landed!")

    async def event_message(self, ctx):
        """ This function would execute each time once the message send to chat.
        """
        # make sure the bot ignores itself and the streamer
        if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
            return

        await self.handle_commands(ctx)

        if 'hello' in ctx.content.lower():
            await ctx.channel.send(f"Hi, @{ctx.author.name}!")
