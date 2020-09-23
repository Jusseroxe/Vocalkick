import discord
import asyncio
from time import sleep, time
from json import load as json_load
from discord.utils import get

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
global mute
global chat
global ids
global idmute
global me
me = 0
ids = 0
idmute = 0
chat = False
mute = False
idbck = 0
meid = 0
memid = 0

client = discord.Client()
CHANNELS = {}

async def option(message, var, value, *args):
    OPTIONS[message.guild.id][var] = type(OPTIONS[message.guild.id][var])(value)
    await message.add_reaction("👌")

async def change_presence(message, *args):
    await client.change_presence(activity=discord.Activity(name=" ".join(args), type=discord.ActivityType.playing))
    print("desc change to :", " ".join(args)) 

async def toogle_stop(message, *args):
    OPTIONS[message.guild.id]["running"] = not OPTIONS[message.guild.id]["running"]
    if OPTIONS[message.guild.id]["running"] == True:
        await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])
        await change_presence(message, '&help | online and ready')
        print("resuming by :", message.author)
    else:
        print("stopped by :", message.author)
        await change_presence(message, '&help | paused by :', str(message.author))
        await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])

async def mutee(message, *args):
    global idmute
    idmute = int(args[0])
    if idmute == 259676097652719616:
        await message.add_reaction("🤫")
        await message.author.create_dm()
        await message.author.dm_channel.send(message.content + "\n\n mdr non")
        return
    if idmute in muted:
        await message.add_reaction("❔")
        await message.author.create_dm()
        await message.author.dm_channel.send(str(idmute) + "is already muted", delete_after = 100)
        print(idmute, "already muted")
    if idmute not in muted:
        muted.append(idmute)
        await message.add_reaction("🟢")
        print(idmute, "is now muted")
        return
async def veriff(message, *args):
    nom = " ".join(args).lower()
    print(args)
    try:
        
        if nom in classe:
            print("validé")
            await message.add_reaction("👌")
            print("renaming...")
            rename = args[-1][0].upper() + args[-1][1:].lower() + " " + args[0][0].upper() + "."
            await message.author.edit(nick=rename)
            print("recherche du groupe...")
            groupe = classe[nom]
            await message.author.add_roles(get(message.guild.roles, name=groupe))
            await message.author.add_roles(get(message.guild.roles, name="Elève"))
            if "A" in groupe:
                print("groupe A")
                await message.author.add_roles(get(message.guild.roles, name="A"))
                return
            elif "B" in groupe:
                print("groupe B")
                await message.author.add_roles(get(message.guild.roles, name="B"))
                return
            elif "C" in groupe:
                print("groupe C")
                await message.author.add_roles(get(message.guild.roles, name="C"))
                return
            elif "D" in groupe:
                print("groupe D")
                await message.author.add_roles(get(message.guild.roles, name="D"))
                return
        else:
            await message.add_reaction("❌")
            print("inconnu")
            return
    except:
        await message.add_reaction("❔")
        print("critical error")

    
async def unmutee(message, *args):
    global muted
    print(muted)
    idmute = args[0]
    try:
        idmute = int(args[0])
    except:
        if idmute == 'all':
            muted = []
            return
        await message.add_reaction("👌")
    finally:
        if idmute not in muted:
            await message.add_reaction("❔")
            return
        if idmute in muted:
            muted.remove(idmute)
            await message.add_reaction("👌")
            return
    
async def chatt(message, *args):
    global chat
    global ids
    global me
    global idbck
    global meid
    global memid
    try:
        ids = int(args[0])
        if ids != idbck:
            if meid or memid != 0:
                if meid or memid != none:
                    await meid.create_dm()
                    await meid.dm_channel.send("Chat closed with " + str(memid))
                    await memid.create_dm()
                    await memid.dm_channel.send("Chat closed with " + str(meid))          
        me = message.author.id
        meid = client.get_user(me)
        memid = client.get_user(ids)
        await memid.create_dm()
        await memid.dm_channel.send("Connexion etablihed with " + str(meid))
        await meid.create_dm()
        await meid.dm_channel.send("Connexion etablihed with " + str(memid))
        chat = True
        await message.add_reaction("🟢")
        ids = idbck
        return
    except ValueError:
        if args[0] == "stop":
            chat = False
            await meid.create_dm()
            await meid.dm_channel.send("Chat closed with " + str(memid))
            await memid.create_dm()
            await memid.dm_channel.send("Chat closed with " + str(meid))
            await message.add_reaction("👌")
            return
        print("I had a invalid id can't process to chat")
        await message.add_reaction("❔")
        return
    except AttributeError:
        print("can't open a chat with", ids, "i don't know this id")
        await message.add_reaction("❌")
        return
    except IndexError:
        print("I don't recive any id I don't know what to do")
        await message.add_reaction("❔")
        await message.author.create_dm()
        await message.author.send("**__Syntax Error__** \n\n If you want to talk to someone use : `&chat <id>` \n If you want to stop the chat use `&chat stop`", delete_after = 100)

async def bann(message, *args):
    idcs = int(args[0])
    clid = client.get_user(idcs)
    await ban(clid, reason=None, delete_message_days=0)

async def sayy(message, *args):
    ch = int(args[0])
    mss = " ".join(args[1:])
    channel = client.get_channel(ch)
    await channel.send(mss)
    await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])
    return

    
async def helpp(message, *args):
	mem = message.author
	await mem.create_dm()
	await mem.dm_channel.send("__**command list:**__ \n\n**option alone_time :** temps (en sec) qu'un utilisateur peut rester seul dans un vocal (par défaut 5min)\n\n**option raison :** le message qui sera envoyé aux utilisateur kickés (le message se supprime au bout de <deltime>)\n\n**stop :** permet d'arrêter le bot temporairement en cas de problèmes (pour relancer le bot il suffit de refaire la commande)\n\n**option prefix :** permet de changer le préfix du bot (& par défaut)\n\n**help :** envoie ce message à l'utilisateur qui effectue la commande\n\n**option emoji :** l'emoji avec le quel le bot réagit quand une personne fait <préfix>help (par défaut : :ok_hand:)\n\n**option frst_time :** temps (en sec) avant que le bot ne kick une personne qui est seul dans un vocal et qui n'a jamais été en conversation avec un autre utilisateur (30min par défaut )\n\n**option deltime :** temps (en sec) avant que le bot supprime le message d'avertissement envoyé en dm (par défaut : 24h)\n\n**option role :** nom du role qu'un membre doit posséder pour modifier les differents parametres (`modifier` par défaut)\n\n**mute :** pour muter une personne sur tout les serveurs ou est installé le bot s'utilise de la facon &mute <id>\n\n**unmute :** pour unmute les gens mutés s'utilise de la facon &unmute <id> (pour unmuter tout le monde vous pouvez utiliser &unmute all)\n\n**say :** pour que le bot envoi un message a votre place dans un salon choisi s'utillise de la facon &say <id du channel> <message>\n\n**chat :** fonctionalitée experimentale pour parler a traver le bot avec d'autres personnes s'utilise de la facon &chat <id> (pour fermer le chat utilisez &chat stop)")
	await mem.dm_channel.send("\n\n ```note : il vous faut la permission `déplacer les membres` ou le role defini par <role> pour parametrer le bot```\n\n__**En devloppement**__\n\n**ban :** pour bannir une personne d'un serveur ou de tous les serveurs ou le bot est connecté s'utilise de la facon &ban <id> (all) (pour pouvoir ban cette personne sur tout les serveurs vous devez avoir la permission de bannir des membres sur tout ces serveurs)\n\n**kick :** pour kicker une personne d'un serveur ou de tous les serveurs ou le bot est connecté s'utilise de la facon &kick <id> (all) (pour pouvoir kick cette personne sur tout les serveurs vous devez avoir la permission d'expulser des membres sur tout ces serveurs) \n\n`Une question/sugestion? contactez mon devloppeur : `<@259676097652719616>` :)`")
	await message.add_reaction(OPTIONS[message.channel.guild.id]["emoji"])
	print("help succsesfully send")
actions = {"option": option,"verif": veriff,"desc": change_presence, "stop": toogle_stop, "help": helpp, "mute": mutee, "chat": chatt, "say": sayy, "unmute": unmutee, "ban": bann}
perm_actions = ["option", "stop", "mute", "say", "unmute"]
admin_actions = ["desc"]
classe = {'bastienne-banco théo': 'A-1', 'besnier clément': 'A-1', 'boisson leeloo': 'A-1', 'brunet quentin': 'A-1', 'dalleau alex': 'A-1', 'dhoury emma': 'A-1', 'fanget matthieu': 'A-1', 'godin luc': 'A-1', 'gonin flavien': 'A-1', 'guillemin matthieu': 'A-1', 'jay thomas': 'A-1', 'mathian thibault': 'A-1', 'mecheloukh sélim': 'A-1', 'mecheloukh soheïl': 'A-1', 'pognante jules': 'A-1', 'barth pierre': 'A-2', 'beaufils tao': 'A-2', 'consuegra yanis': 'A-2', 'derancourt rémi': 'A-2', 'doucet raphael': 'A-2', 'el assi nolan': 'A-2', 'gueguen axel': 'A-2', 'gundogan emin': 'A-2', 'hoarau océane': 'A-2', 'josserand jordan': 'A-2', 'mahri yassine': 'A-2', 'marizon flavien': 'A-2', 'steimer lilian': 'A-2', 'surre aymeric': 'A-2', 'vassal marco': 'A-2', 'barraud matthieu': 'B-1', 'blanco sacha': 'B-1', 'cros célian': 'B-1', 'de almeida goncalves syméon': 'B-1', 'gastaldo quentin': 'B-1', 'germani nicolas': 'B-1', 'gillot romain': 'B-1', 'guerin bastien': 'B-1', 'joyeux-bouillon estelle': 'B-1', 'lawriw elian': 'B-1', 'loiodice lukas': 'B-1', 'lucas maxence': 'B-1', 'mousques roméo': 'B-1', 'reynaud mathis': 'B-1', 'wibaillie valentin': 'B-1', 'albrand alexis': 'B-2', 'argoud thibaud': 'B-2', 'bonnefoy gael': 'B-2', 'bouchet adrien': 'B-2', 'choc noé': 'B-2', 'correnoz clement': 'B-2', 'delon loïc': 'B-2', 'doussot thibault': 'B-2', 'enrici mathis': 'B-2', 'mora hugo': 'B-2', 'morelle julien': 'B-2', 'pernier alexandre': 'B-2', 'salehddine othmane': 'B-2', 'thauvin- -tosetto lola': 'B-2', 'zahaf-kradra ilyas': 'B-2', 'adomo bitea adil massa': 'C-1', 'bel hadj asmaa': 'C-1', 'chalekh zineddine': 'C-1', 'cuerq florian': 'C-1', 'etievent lucas': 'C-1', 'lecornu raphael': 'C-1', 'lou lori': 'C-1', 'makri lina': 'C-1', 'mechehoud abdennour': 'C-1', 'pacotte gabriel': 'C-1', 'paillot jefferson': 'C-1', 'renard nathan': 'C-1', 'reynaud loris': 'C-1', 'robert marius': 'C-1', 'veillas matys': 'C-1', 'ben aïcha mohammed': 'C-2', 'chebout rayen': 'C-2', 'cole axel': 'C-2', 'da cruz benjamin': 'C-2', 'defleur thomas': 'C-2', 'dieudonne marc': 'C-2', 'gely ethan': 'C-2', 'gueripel paul': 'C-2', 'guichard lucas': 'C-2', 'hello adam': 'C-2', 'kilic mikâil': 'C-2', 'labatte elie': 'C-2', 'le menn lucas': 'C-2', 'lkima houda': 'C-2', 'rivière alexis': 'C-2', 'arnoux-bonkowski emmanuel': 'D-1', 'battesti loup': 'D-1', 'bernet elsa': 'D-1', 'carrel quentin': 'D-1', 'carta roni': 'D-1', 'dieu--guillot romain': 'D-1', 'duchet raphaël': 'D-1', 'elati adam': 'D-1', 'galleron evan': 'D-1', 'guillemin vincent': 'D-1', 'nascimento ardiles renato': 'D-1', 'piernas loïc': 'D-1', 'prochasson capucine': 'D-1', 'rognon nathan': 'D-1', 'sallé maxime': 'D-1', 'urru théo': 'D-1', 'amiot françois': 'D-2', 'arlè alexandre': 'D-2', 'belguendouz mehdi': 'D-2', 'ben youssef iheb': 'D-2', 'beyler wilson': 'D-2', 'del medico remi': 'D-2', 'dubonnet amandine': 'D-2', 'falcy marion': 'D-2', 'ferrouillet-reverdy laure': 'D-2', 'khababa abdel-rahim': 'D-2', 'lefranc nicolas': 'D-2', 'miras romain': 'D-2', 'ponal mathieu': 'D-2', 'roelandt zoé': 'D-2', 'rrahmani altin': 'D-2'}

badwords = ["tg","TG","Tg","NTM","ntm","PD","pd","fdp","FDP","suce","Suce","SUCE","ftg","FTG","Ntm"]
tg = ["fortnite", "Fortnite", "fortnayte", "fornite", "Fornite", "fortnayte", "Nite", "NITE", "FORTNITE"]
ppl = ["paperluigi", "Paperluigi", "PAPERLUIGI"]
pastg = ["unite", "tendinite"]
censure = [532351456955727874, 651542073278988288]
slp = [521030786334588958]
muted = []

@client.event
async def on_message(message):
    if type(message.channel) != discord.TextChannel:
        if message.author.id == 697343120433741947:
            return
        if chat == True:
            if message.author.id == ids:
                meid = client.get_user(me)
                await meid.create_dm()
                await meid.dm_channel.send(message.content)
                return
            if message.author.id == me:
                memid = client.get_user(ids)
                await memid.create_dm()
                await memid.dm_channel.send(message.content)
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
    if message.author.id in muted:
        await message.delete()
        return
    
    if message.guild.id in censure:
        a = message.content
        for mot in tg:
            if mot in a:                
                if message.author.id == 259676097652719616:
                    print("EYES INTENSIFIES")
                    await message.add_reaction("👀")
                    return
                print("bad msg in yoro :",message.content) 
                await message.add_reaction("🖕")
                await message.author.create_dm()
                try:
                    await message.author.dm_channel.send(message.content + " \n\n**delete this** :gun:")
                except Exception as e:
                    if e.code == 50007:
                        print("can't send dm to", message.author, "the user must have bocked me ce mechant :c")
                return
            
    if message.guild.id in slp:
        a = message.content
        for mot in ppl:
            if mot in a:                
                if message.author.id == 259676097652719616:
                    print("EYES INTENSIFIES")
                    await message.add_reaction("👀")
                    return
                print("ppl detect in :",message.content) 
                await message.delete()
                await message.author.create_dm()
                try:
                    await message.author.dm_channel.send(message.content + " \n\n**NO**")
                except Exception as e:
                    if e.code == 50007:
                        print("can't send dm to", message.author, "the user must have bocked me cette personne peu recommendable")
                return
        
        
    if len(message.content) and message.content[0] == OPTIONS[message.guild.id]["prefix"]:
        
        a = message.content[1:].split(" ")
        if a[0] not in actions:
            print("wrong command:", message.content, "by :", message.author)
            await message.add_reaction("❔")
            return
        if a[0] in admin_actions and message.author.id not in CONFIG["admins"]:
            print("wrong permission to use command:", message.content, "by :", message.author)
            await message.add_reaction("❌")
            return
        if a[0] in perm_actions and (message.author.guild_permissions.move_members == False and OPTIONS[message.channel.guild.id]["role"] not in list(map(lambda x: x.name, message.author.roles))):
            print("no perms nice try ", message.author)
            await message.add_reaction("❌")
            print(message.author.roles)
            return
        print("executing command:", message.content, "by :", message.author)
        await actions[a[0]](message, *a[1:])


@client.event
async def on_ready():
    print('{} is online and ready to kick'.format(client.user))
    mute = False
    await change_presence(None, '&help | online and ready') 
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
        print(channel.members[0].name, "is alone in", channel.name, "waiting for someone in the server :", channel.guild.name,)
        print("starting the alone time countdown before kicking(", OPTIONS[channel.guild.id]["frst_time"], "sec )")
        await asyncio.sleep(OPTIONS[channel.guild.id]["frst_time"])
        try:
            print("Countdown ended for", channel.members[0].name, "in", channel.name, "(", channel.guild.name, ")")
        except:
            print("Countdown ended but the member has left the channel before")
    else:
        print(channel.members[0].name, "is now alone in the channel", channel.name, "in the server :", channel.guild.name)
        print("starting the alone time countdown before kicking(", OPTIONS[channel.guild.id]["alone_time"], "sec )")
        await asyncio.sleep(OPTIONS[channel.guild.id]["alone_time"])
        try:
            print("Countdown ended for", channel.members[0].name, "in", channel.name, "(", channel.guild.name, ")")
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
                print("there is now", nb, "person connected in", channel.name, "(", channel.guild.name, ") with", members[0], "aborting kicking procedure...")
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

