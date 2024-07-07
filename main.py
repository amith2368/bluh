import discord
import pyttsx3 as pyttsx3
from discord.ext import commands
from pydub import AudioSegment
from pydub.playback import play
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
bot = commands.Bot(command_prefix='^', intents=intents)

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the speech rate if needed


def save_tts(text, filename):
    engine.save_to_file(text, filename)
    engine.runAndWait()


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
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


# Command to play TTS message in the voice channel
@bot.command(name='say', help='Converts text to speech and plays it in the voice channel')
async def say(ctx, *, message):
    voice_client = ctx.guild.voice_client
    print('Joining Voice Channel')
    if not voice_client:
        await ctx.send("The bot is not connected to a voice channel.")
        return

    print('Creating TTS Message')
    # Convert the message to speech
    save_tts(message, "message.mp3")

    print('Playing the message')
    # Play the converted speech
    voice_client.play(discord.FFmpegPCMAudio("message.mp3"), after=lambda e: print('done', e))
    while voice_client.is_playing():
        await asyncio.sleep(1)

    # Clean up the audio file after playing
    os.remove("message.mp3")


# Run the bot with your token
if __name__ == '__main__':
    token = os.getenv('DISCORD_BOT_TOKEN')
    bot.run(token)

# Permission Integer 36713472