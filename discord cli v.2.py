import os
import sys
import asyncio
import threading
import discord
import keyboard

# ─│┌┐└┘↑↓

intents = discord.Intents.default()
intents.message_content = True

def barr(leng, char):
    retval = ""
    for i in range(int(leng)):
        retval = retval + char
    return retval

t5m = []
t5ma = []
return_to_menu = False

client = discord.Client(intents=intents)

# GLOBAL message receiver
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if len(t5m) < 5:
        t5m.append(str(message.content))
        t5ma.append(str(message.author))
    else:
        del t5m[0]
        del t5ma[0]
        t5m.append(str(message.content))
        t5ma.append(str(message.author))

    os.system("cls" if os.name == "nt" else "clear")
    print("Message viewer + sender.\nPress \\ to go back.\n")

    rendert5m = []
    rendert5ma = []
    rendert5m.extend(t5m)
    rendert5ma.extend(t5ma)

    for i in t5ma:
        tml = len(t5m[0])
        if len(str(i)) > tml:
            ulen = len(str(i))
            clen = len(rendert5m[0])
            temp = clen + 1
            print("┌" + barr(ulen, "─") + "┐")
            print(str(i) + " │")
            print("│" + rendert5m[0] + barr(ulen - temp + 1, " ") + "│")
            print("└" + barr(ulen, "─") + "┘")
            del rendert5m[0]
            del rendert5ma[0]
        elif len(str(i)) < tml:
            ulen = len(str(i))
            clen = len(rendert5m[0])
            temp = clen - ulen
            print("┌" + barr(clen, "─") + "┐")
            print(str(i) + barr(temp + 1, " ") + "│")
            print("│" + rendert5m[0] + "│")
            print("└" + barr(clen, "─") + "┘")
            del rendert5m[0]
            del rendert5ma[0]


@client.event
async def on_ready():
    asyncio.create_task(back_to_menu_loop())
    mainmenu(client.user.name)


def mainmenu(name):
    global return_to_menu
    return_to_menu = False
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Welcome {name}!\n")
    print("1, message viewer + sender")  # combined mode
    print("2, autobot menu")
    print("3, saved messages")
    comm = input("> ")
    if comm == "1":
        messages()
    if comm == "2":
        autobot()
    if comm == "3":
        savedmess()


def messages():
    os.system("cls" if os.name == "nt" else "clear")
    print("Message viewer + sender.\nType messages below. Type 'exit' to go back.\n")
    ch = client.get_channel(CHANNEL_ID_HERE)  # replace with your channel ID

    def input_thread():
        global return_to_menu
        while True:
            if return_to_menu:
                break
            msg = input(">")
            if msg.lower() == "exit":
                break
            if ch and msg.strip() != "":
                asyncio.run_coroutine_threadsafe(ch.send(msg), client.loop)
        mainmenu(client.user.name)

    threading.Thread(target=input_thread, daemon=True).start()


def autobot():
    os.system("cls" if os.name == "nt" else "clear")
    print("Autobot menu (placeholder). Press \\ to go back.")


def savedmess():
    os.system("cls" if os.name == "nt" else "clear")
    print("Saved messages menu (placeholder). Press \\ to go back.")


async def back_to_menu_loop():
    global return_to_menu
    while True:
        if keyboard.is_pressed("\\"):
            if not return_to_menu:
                return_to_menu = True
                mainmenu(client.user.name)
        await asyncio.sleep(0.2)


client.run('BOT_TOKEN_HERE')