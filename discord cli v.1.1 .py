import os
import discord
import keyboard as k
import sys
#─│┌┐└┘↑↓

channel = discord.client.get_channel(1306777879090298943)
intents = discord.Intents.default()
intents.message_content = True

def barr(leng, char):                                   #make a string of charactors of length leng
    retval=""
    for i in range(int(leng)):
        retval=retval+char
    return(retval)

def box(user, content):                                 #renders a bow with a title and looks like
    if len(user) > len(content):  #renders the box on the user length                       #┌──────┐
        ulen=len(user)                                                                      #user   │
        clen=len(content)                                                                   #│conten│
        temp=clen+1                                                                         #└──────┘
        print("┌"+barr(ulen, "─")+'┐')
        print(user+' │')
        print("│"+content+barr(ulen-temp+1, ' ')+'│')
        print("└"+barr(ulen, "─")+'┘')

    elif len(user) < len(content):#renders the box on the content length
        ulen=len(user)
        clen=len(content)
        temp=clen-ulen
        print("┌"+barr(clen, "─")+'┐')
        print(user+barr(temp+1, " ")+'│')
        print("│"+content+'│')
        print("└"+barr(clen, "─")+'┘')

t5m=[]                                                  #most recent 5 messages contents
t5ma=[]                                                 #most recent 5 messages senders

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    mainmenu({client.user.name})

def mainmenu(name):
    os.system("cls")
    print(f"Welcome {name}!\n")
    print("1, messager")                                #launches the messaging system
    print("2, autobot menu")                            #set the bot so it will auto respond to commands. disabled by default
    print("3, saved messaged")                          #quick respond with premade messages
    comm=input(">")
    if comm == "1":
       messages()
    if comm == "2":
        autobot()
    if comm == "3":
        savedmess()

def messages():
    os.system("cls")
    print("press s to send a message")
    while True :
        @client.event
                                                        #receiving system↓
        async def on_message(message):                  #activated when a message is sent by anyone
            os.system("cls")
            print("press s to send a message")
            if len(t5m) < 5:                            #to keep the message count ≤ 5
                t5m.append(str(message.content))
                t5ma.append(str(message.author))
            else:
                del t5m[0]
                del t5ma[0]
                t5m.append(str(message.content))
                t5ma.append(str(message.author))
            rendert5m = []                              #clear rendering lists
            rendert5ma = []
            rendert5m.extend(t5m)                       #copy message lists to rendering lists
            rendert5ma.extend(t5ma)
            for i in t5ma:                              #rendering system
                box(rendert5ma[0], rendert5m[0])        #renders message box
                del rendert5m[0]                        #clears the first element in the rendering lists
                del rendert5ma[0]
                                                        #sending system goes here↓
        async def send_message() :
        if k.ispressed("s") = True:
            await channel.send(input("send: "))


def autobot():
    print("work")

def savedmess():
    print("work")

client.run('bot token goes here')                       #bot token

