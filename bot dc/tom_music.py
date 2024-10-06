#vou importar as bibliotecas necessárias
import discord
import os 
import asyncio
import yt_dlp
from dotenv import load_dotenv
load_dotenv()

def run_bot():
    # o necessário pro bot existir 
    load_dotenv()
    TOKEN =os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.messages = True
    client=discord.Client(intents)
     #conectando com o youtube
    voice_client={}
    yt_dl_opitions={"format":"bestaudio/best"}
    ytdl=yt_dlp.YoutubeDL(yt_dl_opitions)
#comando para que o ffmpeg pegue somente o audio do video 
    ffmpeg_options= {'options':'-vn'}

 #criando a função ready 
    @client.event
    async def on_ready():
        print(f'{client.user} is now on your server!')

# criando o play :)
    @client.event
    async def on_message(message):
        #verificando se a mensagem é o comando de &play do nosso bot
        if message.content.startswith("&play"):
         try:
                voice_client= await message.author.voice.chanel.connect()
                voice_client[voice_client.guild.id]=voice_client
         except Exception as e:
            print(e)
        #separando a url do comando &play
        try: 
            url=message.content.split ()[1]
            loop=asyncio.get_event_loop()
            #extraindo as informações do video sem ter que baixa-las
            data= await loop.run_in_executor(None,lambda:ytdl.extract_info(url,dowload=False))
            #pegando a url do video e fazendo ele tocar musica!!!!!
            song=data['url']
            player=discord.ffmpegPCMAudio(song,**ffmpeg_options)
            voice_client[message.guild.id].play(player)
        except Exception as e:
            print(e)
