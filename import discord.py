import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os
import asyncio

from pytube import YouTube

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

queued_songs = []


ffmpeg_path = r'C:\Users\akoma\Downloads\ffmpeg-2023-06-08-git-024c30aa3b-full_build\bin\ffmpeg.exe'

with open('mytoken', 'r') as file:
    TOKEN = file.read()

# Use the file_contents variable in your code


@bot.command()
async def play(ctx,url):
    voice_channel = ctx.author.voice.channel

    if ctx.voice_client is None or not ctx.voice_client.is_connected():
        vc = await voice_channel.connect()
    else:
        vc = ctx.voice_client


    yt = YouTube(url)

    audio_stream = yt.streams.get_audio_only()
    audio_stream.download(filename='temp')
  #  os.system(r'"C:\Users\akoma\Downloads\ffmpeg-2023-06-08-git-024c30aa3b-full_build\bin\ffmpeg.exe" -i temp.mp4 -acodec libvorbis temp.ogg')
    ctx.voice_client.play(discord.FFmpegPCMAudio(executable=ffmpeg_path, source='temp'), after=lambda error: asyncio.run_coroutine_threadsafe(on_audio_end(ctx), bot.loop))



async def on_audio_end(ctx):
   # if error:
    #    print('audio error:', error) n

    # check if there are queued songs
    if not queued_songs:
        # disconnect from the voice channel if there are no more songs
        await ctx.voice_client.disconnect()
        return

        # get the next song from the queue
    url = queued_songs.pop(0)
    yt = YouTube(url)

    # download the song using YTDL
    audio_stream = yt.streams.get_audio_only()
    audio_stream.download(filename='temp')
    #ctx.voice_client.play(discord.FFmpegPCMAudio(executable=r"C:\Users\akoma\Downloads\ffmpeg-2023-06-08-git-024c30aa3b-full_build\bin\ffmpeg.exe", source=r"C:\Users\akoma\temp"))
    ctx.voice_client.play(discord.FFmpegPCMAudio(executable=ffmpeg_path, source='temp'), after=lambda error: asyncio.run_coroutine_threadsafe(on_audio_end(ctx), bot.loop))

    
@bot.command() 
async def q(ctx, url):
    queued_songs.append(url)
    await ctx.send(f'this the queue nigga {queued_songs}')

    if ctx.voice_client:
        if not ctx.voice_client.is_playing():
            await on_audio_end(ctx)

    else:
            voice_channel = ctx.author.voice.channel
            vc = await voice_channel.connect()

            await on_audio_end(ctx)



@bot.command() 
async def whatsq(ctx):
        if not queued_songs:
            await ctx.send('no songs nigga')
        else:
            await ctx.send(f'this the queue nigga {queued_songs}')

@bot.command() 
async def skip(ctx):
    if ctx.author.id == 176359387181481984: 

    
        if not queued_songs:
            # disconnect from the voice channel if there are no more songs
            await ctx.voice_client.disconnect()
            return

            # get the next song from the queue
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        
        #   await on_audio_end(ctx)
            await ctx.send('Skipped the current song')
        else:
            await ctx.send('I am not currently playing any songs')
    else:
        await ctx.send("Error! e_code: 308, muncher detected")
        if ctx.voice_client.is_playing():

            queued_songs[0]=('https://www.youtube.com/watch?v=y9YruhZoZ6o')
           
            ctx.voice_client.stop()



        #   await on_audio_end(ctx)
        #     await ctx.send('Skipped the current song')
        # else:
        #     await ctx.send('I am not currently playing any songs')



    

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(TOKEN)  # Replace with your bot's token

