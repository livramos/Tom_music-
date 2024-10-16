# Importar as bibliotecas necessárias
import discord
import os
import asyncio
import yt_dlp
from discord import FFmpegPCMAudio  # Certifique-se de que está assim
from dotenv import load_dotenv

# Carregar o arquivo .env
load_dotenv()

# Função principal que executa o bot
def run_bot():
    TOKEN = os.getenv('discord_token')
    
    intents = discord.Intents.default()
    intents.message_content = True  # Habilitar o conteúdo das mensagens
    client = discord.Client(intents=intents)
    
    # Conectando com o YouTube
    voice_clients = {}  # Dicionário para armazenar os voice clients
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)
    
    # FFMPEG configurações
    ffmpeg_options = {'options': '-vn'}
    
    # Evento que confirma que o bot está pronto
    @client.event
    async def on_ready():
        print(f'{client.user} is now on your server!')
    
    # Evento que trata mensagens enviadas
    @client.event
    async def on_message(message):
        # Verificar se a mensagem é o comando &play
        if message.content.startswith("&play"):
            try:
                # Verificar se o usuário está em um canal de voz
                if message.author.voice is None:
                    await message.channel.send("Você precisa estar em um canal de voz para usar este comando.")
                    return

                # Conectar ao canal de voz do autor
                voice_channel = message.author.voice.channel
                if message.guild.id not in voice_clients:
                    voice_client = await voice_channel.connect()
                    voice_clients[message.guild.id] = voice_client
                else:
                    voice_client = voice_clients[message.guild.id]

            except Exception as e:
                print(f"Erro ao conectar ao canal de voz: {e}")
                await message.channel.send("Houve um erro ao tentar conectar ao canal de voz.")
                return

            # Verificar se há uma URL fornecida com o comando
            try:
                url = message.content.split()[1]
            except IndexError:
                await message.channel.send("Você precisa fornecer uma URL para o comando &play.")
                return

            try:
                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

                # Pegar a URL do áudio e tocar a música
                song = data['url']
                player = FFmpegPCMAudio(song, **ffmpeg_options)  # Alterado para usar o player corretamente

                if not voice_client.is_playing():
                    voice_client.play(player)
                    await message.channel.send(f"Tocando agora: {data['title']}")
                else:
                    await message.channel.send("Já estou tocando uma música. Aguarde ela terminar.")

            except Exception as e:
                print(f"Erro ao tentar tocar a música: {e}")
                await message.channel.send("Houve um erro ao tentar tocar a música.")
    
    # Rodar o bot
    client.run(TOKEN)

run_bot()
# atualmente com erro na correlação entre o ffmpeg com o discord 
####class discord.FFmpegPCMAudio(source, *, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None) tenta isso aqui dps 
### https://discordpy.readthedocs.io/en/latest/api.html?highlight=ffmpeg#ffmpegaudio 
