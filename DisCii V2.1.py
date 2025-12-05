import os
import sys
import asyncio
import threading
import discord
import keyboard
import json
import time
from collections import deque

# ─│┌┐└┘↑↓

intents = discord.Intents.default()
intents.message_content = True

SAVE_FILE = "saved_messages.json"

def barr(leng, char):
    return char * leng

# --- Saved Messages Storage ---
def load_saved():
    """Load saved messages from JSON file, create file if missing."""
    if not os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "w") as f:
            json.dump([], f)
    with open(SAVE_FILE, "r") as f:
        return json.load(f)

def save_message(author, content):
    """Save a new message to JSON file."""
    data = load_saved()
    data.append({"author": author, "content": content})
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def delete_last_message():
    """Delete the last saved message from JSON file."""
    data = load_saved()
    if data:
        removed = data.pop()
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return removed
    return None

# --- Globals ---
t5m = deque(maxlen=5)
t5ma = deque(maxlen=5)
return_to_menu = False      # hotkey-triggered return
menu_lock = threading.Lock()  # prevent overlapping menu redraws
username = "User"           # will be set on_ready

client = discord.Client(intents=intents)

# --- Discord Events ---
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Add to rolling viewer
    t5m.append(str(message.content))
    t5ma.append(str(message.author))

    # Show messages
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Message viewer + sender — Welcome {username}!\n")
    print("Press 's' to save last message.")
    print("Type 'exit' at any prompt to return to the main menu.\n")

    for author, msg in zip(t5ma, t5m):
        boxlen = max(len(author), len(msg))
        print("┌" + barr(boxlen, "─") + "┐")
        print(author + barr(boxlen - len(author), " ") + "│")
        print("│" + msg + barr(boxlen - len(msg), " ") + "│")
        print("└" + barr(boxlen, "─") + "┘")
        print()

@client.event
async def on_ready():
    global username
    username = str(client.user.name)

    # Start hotkey loop in async
    asyncio.create_task(hotkey_loop())
    # Start menu in separate thread
    threading.Thread(target=run_menu, daemon=True).start()

# --- Menu runner (separate thread, never blocks discord loop) ---
def run_menu():
    global return_to_menu
    while True:
        with menu_lock:
            mainmenu()
        if return_to_menu:
            return_to_menu = False

# --- Menus ---
def mainmenu():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Welcome {username}!\n")
    print("Main Menu")
    print("1, message viewer + sender")
    print("2, autobot menu")
    print("3, saved messages")
    print("\nType 'exit' at any time to return here.")
    print("\nDis.Cli made by 1Skee_ And Dimitri84")
    comm = input("> ").strip().lower()

    # Global exit: already in main menu; if typed, just re-render
    if comm == "exit":
        return

    if comm == "1":
        messages()
    elif comm == "2":
        autobot()
    elif comm == "3":
        savedmess()
    else:
        print("Unknown option. Type 1, 2, or 3. ('exit' to stay here)")
        time.sleep(1)

def messages():
    global return_to_menu
    while True:
        if return_to_menu:
            return_to_menu = False
            break

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Message viewer + sender — Welcome {username}!\n")
        print("Type your message to send. Type 'exit' to return to main menu.\n")
        ch = client.get_channel(channel_id_here)  # replace with your channel ID

        msg = input("> ").strip()
        if msg.lower() == "exit":
            break
        if not msg:
            continue
        if ch:
            asyncio.run_coroutine_threadsafe(ch.send(msg), client.loop)
            print("Sent.")
            time.sleep(0.3)

def autobot():
    global return_to_menu
    while True:
        if return_to_menu:
            return_to_menu = False
            break

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Autobot menu\n")
        print("Type 'exit' to return to main menu.")

        cmd = input("> ").strip().lower()
        if cmd == "exit":
            break
        elif cmd:
            print(f"Unknown command: {cmd}")
            time.sleep(0.6)

def savedmess():
    global return_to_menu
    while True:
        if return_to_menu:
            return_to_menu = False
            break

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Saved Messages\n")
        data = load_saved()
        if not data:
            print("No saved messages yet.")
        else:
            for i, msg in enumerate(data, 1):
                boxlen = max(len(msg["author"]), len(msg["content"]))
                print("┌" + barr(boxlen, "─") + "┐")
                print(msg["author"] + barr(boxlen - len(msg["author"]), " ") + "│")
                print("│" + msg["content"] + barr(boxlen - len(msg["content"]), " ") + "│")
                print("└" + barr(boxlen, "─") + "┘")
                print()
        print("Commands: 'c' to delete the last saved message, 'exit' to return to main menu.")

        cmd = input("> ").strip().lower()
        if cmd == "exit":
            break
        elif cmd == "c":
            removed = delete_last_message()
            if removed:
                print(f"Deleted last saved message from {removed['author']}: {removed['content']}")
            else:
                print("No saved messages to delete.")
            time.sleep(0.8)
        else:
            print("Unknown command. Use 'c' or 'exit'.")
            time.sleep(0.8)

# --- Hotkeys (async, non-blocking) ---
async def hotkey_loop():
    global return_to_menu
    while True:
        # Back to menu hotkey
        if keyboard.is_pressed("\\"):
            return_to_menu = True

        # Save last message hotkey (viewer feedback prints to terminal)
        if keyboard.is_pressed("s"):
            if t5m and t5ma:
                save_message(t5ma[-1], t5m[-1])
                print(f"Saved message from {t5ma[-1]}: {t5m[-1]}")

        await asyncio.sleep(0.05) 

# --- Run Bot ---
client.run('bot_token_here')