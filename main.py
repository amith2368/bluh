import discord
from discord.ext import commands
import asyncio
from gtts import gTTS
import os
from dotenv import load_dotenv
load_dotenv()

# Define intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Command to join a voice channel
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    channel = ctx.message.author.voice.channel
    await channel.connect()

# Command to leave the voice channel
@bot.command(name='leave', help='Tells the bot to leave the voice channel')
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

# Command to play TTS message in the voice channel
@bot.command(name='say', help='Converts text to speech and plays it in the voice channel')
async def say(ctx, *, message):
    voice_client = ctx.guild.voice_client
    if not voice_client:
        await ctx.send("The bot is not connected to a voice channel.")
        return

    # Convert the message to speech
    tts = gTTS(text=message, lang='en')
    tts.save("message.mp3")

    # Play the converted speech
    voice_client.play(discord.FFmpegPCMAudio("message.mp3"), after=lambda e: print('done', e))
    while voice_client.is_playing():
        await asyncio.sleep(1)
    
    # Clean up the audio file after playing
    os.remove("message.mp3")

# Run the bot with your token
token = os.getenv('DISCORD_BOT_TOKEN')
bot.run(token)
