from telethon import TelegramClient, events, Button
import os 
from cfg import*
import psycopg2
import S5Crypto
import socket


bot = TelegramClient( 
    'github', api_id=API_ID, api_hash=API_HASH).start(bot_token =TOKEN )


@bot.on(events.NewMessage(pattern='/create_database'))
async def create(app: events.NewMessage.Event):
    username = app.message.chat.username
    if username == ADMIN:
        conexion = psycopg2.connect(
        host=HOST, 
        database=DATABASE, 
        user=USER, 
        password=PASSWORD
    )
        cursor = conexion.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
                username text
            );
        """)
        await app.respond('Database created')
        conexion.commit()
        conexion.close()
    else:
        await app.respond('❗️NO ESTÁS AUTORIZADO❗️')


@bot.on(events.NewMessage(pattern='/add'))
async def add(app: events.NewMessage.Event):
    username = app.message.chat.username
    text_user = app.message.text.split(' ')[1]
    text_user = text_user.replace('@', '')

    if username == ADMIN:
        conexion = psycopg2.connect(
        host=HOST, 
        database=DATABASE, 
        user=USER, 
        password=PASSWORD
    )
        cursor = conexion.cursor()
        cursor.execute(f"""
            INSERT INTO users (username) VALUES ('{text_user}');
        """)
        await app.respond('User added')
        conexion.commit()
        conexion.close()
    else:
        await app.respond('❗️NO ESTÁS AUTORIZADO❗️')

@bot.on(events.NewMessage(pattern='/del'))
async def del_(app: events.NewMessage.Event):
    username = app.message.chat.username
    text_user = app.message.text.split(' ')[1]
    text_user = text_user.replace('@', '')

    if username == ADMIN:
        conexion = psycopg2.connect(
        host=HOST, 
        database=DATABASE, 
        user=USER, 
        password=PASSWORD
    )
        cursor = conexion.cursor()
        cursor.execute(f"""
            DELETE FROM users WHERE username = '{text_user}';
        """)
        await app.respond('User deleted')
        conexion.commit()
        conexion.close()
    else:
        await app.respond('❗️NO ESTÁS AUTORIZADO❗️')


@bot.on(events.NewMessage(pattern='/users'))
async def users(app: events.NewMessage.Event):
    username = app.message.chat.username
    if username == ADMIN:
        conexion = psycopg2.connect(
        host=HOST, 
        database=DATABASE, 
        user=USER, 
        password=PASSWORD
    )
        cursor = conexion.cursor()
        cursor.execute(f"""
            SELECT * FROM users;
        """)
        rows = cursor.fetchall()
        await app.respond('\n'.join(f'{row[0]}' for row in rows))
        conexion.commit()
        conexion.close()



# Comando start
@bot.on(events.NewMessage(pattern='/start'))
async def start(app: events.NewMessage.Event):
    username = app.message.chat.username
    conexion = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT * FROM users WHERE username = '{username}'
    """)
    rows = cursor.fetchall()
    if len(rows) == 0:
        await app.respond(f'❗️Hola! @{username}\n\n❕Para poder usar el Bot contacte con mi desarrollador @JeanPssss ❕')
    else:
        await app.reply(f'Hola! @{username}',
        buttons=[
        [Button.inline('⚙️ Comandos ⚙️', data='command')],
        [Button.inline('💰 Comprar Código 💰', data='shop')],
        ])

@bot.on(events.CallbackQuery(data='start'))
async def help(app: events.CallbackQuery.Event):
    await app.edit(f'Hi!',
    buttons=[
        [Button.inline('⚙️ Comandos ⚙️', data='command')],
        [Button.inline('💰 Comprar Código 💰', data='shop')],
        ])


@bot.on(events.CallbackQuery(data='shop'))
async def help(app: events.CallbackQuery.Event):

    await app.edit('100 CUP = Pago mediante Transferencia Bancaria.\n150 CUP = Pago mediante Transferencia de Saldo.\n\nPara más información Contactar al Desarrollador.',
    buttons=[
        [Button.url('⚙️ Desarrollador ⚙️', 'https://t.me/JeanPssss')],
        [Button.inline('❕Atrás❕', data='start')],
    ])

@bot.on(events.CallbackQuery(data='command'))
async def help(app: events.CallbackQuery.Event):

    await app.edit('/se - Se usa para buscar proxys a partir de un IP y dos rangos.\nEjemplo: /se 1.1.1.1 1055 1100\nLo que hace es que buscara cuales puertos de este IP están abiertos del rango 1055 al 100.\n\n/de - Se usa para desencriptar un proxy encriptado.\nEjemplo: /de socks5://KKCGJEYJKGASDSAWQHHGIEYHKDJIDJKAGKSD',
    buttons=[
        [Button.inline('❕Atrás❕', data='start')],
    ])


@bot.on(events.NewMessage(pattern='/de'))
async def descrypt(app: events.NewMessage.Event):
    username = app.message.chat.username
    conexion = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT * FROM users WHERE username = '{username}'
    """)
    rows = cursor.fetchall()
    if len(rows) == 0:
        await app.respond('❗️NO ESTÁS AUTORIZADO❗️')
    else:
        proxy = app.message.text.split(' ')[1]
        if 'socks5://' in proxy:
            proxy = proxy.replace('socks5://', '')
            descrypt_proxy = S5Crypto.decrypt(f'{proxy}')
            await app.respond(f'Proxy Descryptado:\n\n{descrypt_proxy}')
        else:
            await app.respond('❗️Esté Proxy no es valido❗️')

@bot.on(events.NewMessage(pattern='/se'))
async def search(app: events.NewMessage.Event):
    username = app.message.chat.username
    conexion = psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT * FROM users WHERE username = '{username}'
    """)
    rows = cursor.fetchall()
    if len(rows) == 0:
        await app.respond('❗️NO ESTÁS AUTORIZADO❗️')
    else:
        ip = app.message.text.split(' ')[1]
        rangouno = int(app.message.text.split(' ')[2])
        rangodos = int(app.message.text.split(' ')[3])
        message = await app.respond(f'📡 Buscando Proxy  📡') 
        for port in range(rangouno,rangodos):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            result = sock.connect_ex((ip,port))
            
            if result == 0: 
                    print ("Puerto abierto!")
                    print (f"Puerto: {port}")  
                    proxy = f'{ip}:{port}'
                    proxy_new = S5Crypto.encrypt(f'{proxy}')
                    await message.edit(f'✅ Proxy Encontrado ✅\n\n<code>socks5://{proxy_new}</code>', parse_mode="html")
                    break

            else: 
                await message.edit(f'❌ Proxy no encontrado ❌', parse_mode="html")
                print(f"Puerto: {port} Cerrado")
                sock.close()
                




print('App Run...')
bot.loop.run_forever()