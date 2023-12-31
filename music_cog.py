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
                    await ctx.send("could not connect to the voice channel")
                    return
            
            else:
                await self.vc.move_to(self.music_queue[0][1])
                
            self.music_queue.pop(0)

            self.vc.play(discord.ffmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.playing  = False
    
    @commands.command(name = "play" , aliases = ["p", "playing"], help ="play the selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("connect to a voice channel")
             elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
		    self.is_playing = False
		    self.is_paused = True
		    self.vc.pause()
        elif self.is_paused:
		self.is_paused = False
		self.is_playing = True
		self.vc.resume()

    @commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
		self.is_paused = False
		self.is_playing = True
		self.vc.resume()
         @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)


    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()