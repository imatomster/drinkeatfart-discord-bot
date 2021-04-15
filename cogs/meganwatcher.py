from riotwatcher import LolWatcher, ApiError
import discord
from discord.ext import commands, tasks
# Importing Riotwatcher Token from .env File
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN_RIOTWATCHER = os.getenv('TOKEN_RIOTWATCHER')

# Setting up LolWatcher (need to refresh every 24 hours)
watcher = LolWatcher(TOKEN_RIOTWATCHER)


class MeganWatcher(commands.Cog, name='League of Legends Commands'):
    """Constructor for the cog"""

    def __init__(self, bot_instance):
        self.bot_instance = bot_instance
        # Start the Background Task Checkers
        self.check_megan.start()
        self.game_id = 0

    @tasks.loop(minutes=10)
    async def check_megan(self):
        """Background Task"""
        channel = self.bot_instance.get_channel(791495496266022922)
        discord_id = '<@754199681415905331>'
        cousin = ['TechnoCrest', 'nindragon',
                  'Dansing Queen', 'AsianPanCakes', '32oz']

        user = watcher.summoner.by_name('na1', 'DurianLuver')
        summoner_name = user['name']

        # Check if in game
        try:
            spectator = watcher.spectator.by_summoner('na1', user['id'])
        except ApiError as error_variable:
            if error_variable.response.status_code == 404:
                print(
                    f'It seems like "{summoner_name}" is not ingame right now\n{error_variable}')
        else:
            current_game_id = spectator['gameId']

            if(self.game_id != current_game_id):
                self.game_id = current_game_id

                for i in range(0, 10):
                    for names in cousin:
                        if(spectator['participants'][i]['summonerName'] == names):
                            cousin.remove(names)

                if(len(cousin) > 1):
                    comma_names = '\n'
                    for i in range(len(cousin)):
                        comma_names = comma_names + f':rage: {cousin[i]} :rage:\n'
                    await channel.send(f'**WHY IS {discord_id} IN GAME RIGHT NOW WITHOUT:**\n{comma_names}\n**Surrender now and invite us...**\n*Or compensate at: https://venmo.com/twin-tummy-bot*')
                    print(f'{summoner_name} is in game: {current_game_id}')

            else:
                print(
                    f'{summoner_name} is still in the same game: {current_game_id}')

    @commands.command()
    async def cancel(self, ctx):
        self.check_megan.stop()

    @check_megan.before_loop
    async def before_check_megan(self):
        """Not Running Task until bot_instance is loaded"""
        print('Waiting before looping...')
        await self.bot_instance.wait_until_ready()

    @check_megan.after_loop
    async def after_check_megan(self):
        """Declaring that Loop is done"""
        print('Done!')


def setup(bot_instance):
    """Adds Cog to Bot"""
    bot_instance.add_cog(MeganWatcher(bot_instance))
