import discord 
from discord.ext import commands    

from youtube_dl import youtubeDL

class music_cog(command.cog):
    def __init__(self, Bot):
        self.Bot = Bot

        self.playing = False
        self.paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format' : 'bestaudio' : 'noplaylist' : 'True'}
        self.FFMPEG_OPTIONS = {'before_options' : '-reconnect 1 -reconnected_streamd 1' '-reconnect_delay_max 5', 'option' : '-vn'}

        self.vc = None

    def search(self, item):
        with youtubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download = False)['entries'][0]
        except Exception:
            return = False
    return {'source' : info['formats'[0]['url']], 'title' : info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.ffmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.playing = False 
    
    async def play_music(self, ctx):
        if len(self.music_queue > 0):
            self.playing = True
            m_url= self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.semd("could not connect to the voice channel")
                    return
            
            else:
                await self.vc.move_to(self.music_queue[0][1])
                
            self.music_queue.pop(0)

            self.vc.play(discord.FF)

        else:
            self.playing  = False
