import discord
import asyncio
from time import sleep, time
from json import load as json_load

print(discord.__version__)


with open("config.json") as f:
    CONFIG = json_load(f)


OPTIONS = {}
DEFAULT = {}
DEFAULT["alone_time"] = 300
DEFAULT["reason"] = "as-tu oublié de te déconnecter du vocal? ne t'inquiete pas je l'ai fait pour toi :)"	
DEFAULT["prefix"] = "&"	
DEFAULT["running"] = True
DEFAULT["emoji"] = "👌"
DEFAULT["deltime"] = 86400
DEFAULT["frst_time"] = 1800
DEFAULT["role"] = "modifier"

client = discord.Client()
CHANNELS = {}

async def option(message, var, value, *args):
    OPTIONS[message.guild.id][var] = type(OPTIONS[message.guild.id][var])(value)

async def change_presence(message, *args):
    await client.change_presence(activity=discord.Activity(name=" ".join(args), type=discord.ActivityType.playing))
    print("desc change to :", " ".join(args)) 

async def toogle_stop(message, *args):
    OPTIONS[message.guild.id]["running"] = not OPTIONS[message.guild.id]["running"]
    if OPTIONS[message.guild.id]["running"] == True:
        await change_presence(message, 'online and ready &help')
        print("resuming by :", message.author)
    else:
        print("stopped by :", message.author)
        await change_presence(message, 'paused by :', str(message.author))

    

async def helpp(message, *args):
    mem = message.author
    await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])
    await mem.create_dm()
    await mem.dm_channel.send("__**command list:**__ \n\n**option alone_time :** temps (en sec) qu'un utilisateur peut rester seul dans un vocal (par défaut 5min)\n\n**option raison :** le message qui sera envoyé aux utilisateur kickés (le message se supprime au bout de <deltime>)\n\n**stop :** permet d'arrêter le bot temporairement en cas de problèmes (pour relancer le bot il suffit de refaire la commande)\n\n**option prefix :** permet de changer le préfix du bot (& par défaut)\n\n**help :** envoie ce message à l'utilisateur qui effectue la commande\n\n**option emoji :** l'emoji avec le quel le bot réagit quand une personne fait <préfix>help (par défaut : :ok_hand:)\n\n**option frst_time :** temps (en sec) avant que le bot ne kick une personne qui est seul dans un vocal et qui n'a jamais été en conversation avec un autre utilisateur (30min par défaut )\n\n**option deltime :** temps (en sec) avant que le bot supprime le message d'avertissement envoyé en dm (par défaut : 24h)\n\n**option role :** nom du role qu'un membre doit posséder pour modifier les differents parametres (`modifier` par défaut)\n\n*note : il vous faut la permission `déplacer les membres` ou le role defini par <role> pour parametrer le bot*\n\n`Une question/sugestion? contactez mon devloppeur : `<@259676097652719616>` :)`")
    print("help succsesfully send")
actions = {"option": option, "desc": change_presence, "stop": toogle_stop, "help": helpp}
perm_actions = ["option", "stop"]
admin_actions = ["desc"]

badwords = ["tg","TG","Tg","NTM","ntm","PD","pd","fdp","FDP","suce","Suce","SUCE","ftg","FTG"]

@client.event
async def on_message(message):
    if type(message.channel) != discord.TextChannel:
        if message.author.id == 697343120433741947:
            return
        if message.content in badwords:
            if message.author.id == 328521363180748801:
                print("insult in dm :", message.content)
                print("by :", message.author)
                return
            await message.author.dm_channel.send(">:(")
            print("insult in dm :", message.content)
            print("get trolled :", message.author)
            return
        print("dm ressage recived :", message.content)
        print("by :", message.author)
        return
    if len(message.content) and message.content[0] == OPTIONS[message.guild.id]["prefix"]:
        
        a = message.content[1:].split(" ")
        if a[0] not in actions:
            print("wrong command:", message.content, "by :", message.author)
            return
        if a[0] in admin_actions and message.author.id not in CONFIG["admins"]:
            print("wrong permission to use command:", message.content, "by :", message.author)
            return
        if a[0] in perm_actions and (message.author.guild_permissions.move_members == False and OPTIONS[message.channel.guild.id]["role"] not in list(map(lambda x: x.name, message.author.roles))):
            print("no perms nice try ", message.author)
            print(message.author.roles)
            return
        print("executing command:", message.content, "by :", message.author)
        await actions[a[0]](message, *a[1:])


@client.event
async def on_ready():
    print('{} is online and ready to kick'.format(client.user))
    await change_presence(None, 'online and ready &help') 
    for server in client.guilds:
        OPTIONS[server.id] = dict(DEFAULT)
        
@client.event
async def on_guild_join(guild):
    OPTIONS[guild.id] = dict(DEFAULT)

async def on_delay(channel, first=False):
    if not OPTIONS[channel.guild.id]["running"]:
        if channel in CHANNELS:
            del CHANNELS[channel]
        return
    if first:
        print(channel.members[0].name, "is alone in", channel.name, "waiting for someone in the server :", channel.name,)
        print("starting the alone time countdown before kicking(", OPTIONS[channel.guild.id]["frst_time"], "sec )")
        await asyncio.sleep(OPTIONS[channel.guild.id]["frst_time"])
        try:
            print("Countdown ended for", channel.members[0].name, "in", channel.name, "(", channel.name, ")")
        except:
            print("Countdown ended but the member has left the channel before")
    else:
        print(channel.members[0].name, "is now alone in the channel", channel.name, "in the server :", channel.guild.name)
        print("starting the alone time countdown before kicking(", OPTIONS[channel.guild.id]["alone_time"], "sec )")
        await asyncio.sleep(OPTIONS[channel.guild.id]["alone_time"])
        try:
            print("Countdown ended for", channel.members[0].name, "in", channel.name, "(", channel.name, ")")
        except:
            print("Countdown ended but the member has left the channel before")
        
    while not OPTIONS[channel.guild.id]["running"]:
        if first:
            await asyncio.sleep(OPTIONS[channel.guild.id]["frst_time"])
        else:
            await asyncio.sleep(OPTIONS[channel.guild.id]["alone_time"])
    if channel in CHANNELS:
        del CHANNELS[channel]
        members = channel.members
        nb = len(members)
        if nb != 1:
            if nb > 1:
                print("there is now", nb, "person connected in", channel.name, "(", channel.guild, ") with", members[0], "aborting kicking procedure...")
                return
            if nb == 0:
                print("there is no one in the channel", channel.name, "can't process to kick...")
                return
        print(members[0], "is still alone in", channel.name, "on", channel.guild, "starting kicking procedure...")
        await members[0].edit(voice_channel=None, reason=OPTIONS[channel.guild.id]["reason"])
        print(members[0], "kicked!")
        await members[0].create_dm()
        try:
            await members[0].dm_channel.send(OPTIONS[channel.guild.id]["reason"], delete_after = OPTIONS[channel.guild.id]["deltime"])
        except Exception as e:
            if e.code == 50007:
                print("can't send dm to", members[0], "the user must have bocked me")
        
    
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel and before.channel != after.channel:
        if after.channel in CHANNELS:
            del CHANNELS[after.channel]
        if len(after.channel.members) == 1:
            CHANNELS[after.channel] = True
            print("channel changed for", member.name, "(", before.channel, "->", after.channel, ")")
            await on_delay(after.channel, first=True)
    
    if before.channel and  before.channel != after.channel:
        if len(before.channel.members) == 1:
            CHANNELS[before.channel] = True
            print(member.name, "leave")
            await on_delay(before.channel)
        else:
            if before.channel in CHANNELS:
                del CHANNELS[before.channel]
        
client.run(CONFIG["token"])

