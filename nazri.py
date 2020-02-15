# -*- coding: utf-8 -*-
# @ Script for free library linepy fadhiilrachman
# @ Copyright 2020 Muhammad Nazri A thanks for HelloWorld
from Module.linepy import *
from Module.akad import *
from time import sleep
from gtts import gTTS
from Liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, six, ast, pytz, urllib, urllib3, urllib.parse, traceback, atexit, wikipedia, subprocess, errno


#Disarankan Login Pake Email
#client = LINE() <<Login Link
client = LINE("email","password") #<<<login email
#appName = "DESKTOPWIN 5.20.2"
#client = LINE("token",appName=appName)<<Loguin with token
client.log("YOUR TOKEN : {}".format(str(client.authToken)))
channel = Channel(client,client.server.CHANNEL_ID['LINE_TIMELINE'])
client.log("CHANNEL TOKEN : " + str(channel.getChannelResult()))
clientMid = client.profile.mid
clientProfile = client.getProfile()
clientSettings = client.getSettings()
clientPoll = OEPoll(client)
botStart = time.time()

msg_dict = {}
msg_send = {}

settings = {
    "setKey": False,
    "ChangeVideoProfile": False,
    "ChangeVideoProfile2": False,
    "keyCommand": ""
}

def restartBot():
    print ("[ INFO ] BOT RESTART")
    python = sys.executable
    os.execl(python, python, *sys.argv)
def cTime_to_datetime(unixtime):
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    return datetime.fromtimestamp(str(timeNow))
def dt_to_str(dt):
    return dt.strftime('%H:%M:%S')
def allowLiff():
    url = 'https://access.line.me/dialog/api/permissions'
    data = {
        'on': [
            'P',
            'CM'
        ],
        'off': []
    }
    headers = {
        'X-Line-Access': client.authToken,
        'X-Line-Application': client.server.APP_NAME,
        'X-Line-ChannelId': '1602687308',
        'Content-Type': 'application/json'
    }
    requests.post(url, json=data, headers=headers)
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@NazriGans "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
def sendTemplate(to, data):
    xyz = LiffChatContext(to)
    xyzz = LiffContext(chat=xyz)
    view = LiffViewRequest('1602687308-GXq4Vvk9', xyzz)
    token = client.liff.issueLiffView(view)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))
def command(text):
    pesan = text.lower()
    if settings["setKey"] == True:
        if pesan.startswith(settings["keyCommand"]):
            cmd = pesan.replace(settings["keyCommand"],"")
        else:
            cmd = "Undefined command"
    else:
        cmd = text.lower()
    return cmd
def helpmessage():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpMessage ="╭─「Help Message」─" + "\n" + \
                    "│ Use 「"+ key +"」Use The key To Prefix " + "\n" + \
                    "│ " + key + "Help" + "\n" + \
                    "│ " + key + "Mention" + "\n" + \
                    "│ " + key + "Restartbot" + "\n" + \
                    "│ " + key + "Allowliff" + "\n" + \
                    "│ " + key + "Joox「Search」" + "\n" + \
                    "│ " + key + "Youtube「URL」" + "\n" + \
                    "│ " + key + "Stickergif/「StickerID」" + "\n" + \
                    "│ " + key + "Stickerpng/「StickerID」" + "\n" + \
                    "│ " + key + "Changevideoprofile" + "\n" + \
                    "├─「Maker」─" + "\n" + \
                    "│ • VERSION : HelloWorld" + "\n" + \
                    "╰────────────"
    return helpMessage
def clientBot(op):
    try:
        if op.type == 0:
            print ("[ 0 ] END OF OPERATION")
            return
        if op.type == 25:
            try:
                print ("[ 25 ] MUHAMMAD NAZRI A SEDANG MENGIRIM PESAN :)")
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                setKey = settings["keyCommand"].title()
                if settings["setKey"] == False:
                    setKey = ''
                if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
                    if msg.toType == 0:
                        if sender != client.profile.mid:
                            to = sender
                        else:
                            to = receiver
                    elif msg.toType == 1:
                        to = receiver
                    elif msg.toType == 2:
                        to = receiver
                    if to in msg_send:
                        msg_send[to][msg.id] = None
                    else:
                        msg_send[to] = {}
                        msg_send[to][msg.id] = None
                    cmd = command(text)
                    if msg.contentType in [2,14]:#Jika Content Video Atau File
                        if settings['ChangeVideoProfile'] == True:
                            settings['ChangeVideoProfile']=False
                            client.downloadObjectMsg(msg.id,'path','video.mp4')
                            print('[Excuted] VideoProfileProcessing')
                            client.sendMessage(to, "Send picture to be profiled")
                            settings['ChangeVideoProfile2']=True
                    if msg.contentType == 1:#Jika Content Foto
                        if settings['ChangeVideoProfile2'] == True:
                            settings['ChangeVideoProfile2']=False
                            client.downloadObjectMsg(msg.id,'path','foto.jpg')
                            client.updateProfileVideoPicture('video.mp4','foto.jpg')
                            print('[Excuted] ChangeVideoProfileSuccess')
                            client.sendMessage(to, 'Success Change Video Profile')
                    if msg.contentType == 0:
                        if cmd == "help":
                                helpMessage = helpmessage()
                                mids = "u6d4334e595623ab502647e8e622c4cc8"
                                naz = client.getContact(mids)
                                dt={
                                    'type': 'text',
                                    'text': '{}'.format(str(helpMessage)),
                                    'sentBy': {
                                      'label': 'Muhammad Nazri AsyAry',
                                      'iconUrl' : 'https://os.line.naver.jp/os/p/%s' % client.profile.mid,
                                      'linkUrl' : 'https://line.me/ti/p/~cringelo'
                                    }
                                }
                                sendTemplate(to, dt)
                        elif cmd == "changevideoprofile":
                            client.sendMessage(to,'Send Video To Be Profile')
                            settings['ChangeVideoProfile']=True
                        elif cmd == 'allowliff':
                            allowliff()
                            client.sendMessage("Success")
                        elif cmd == 'restartbot':
                            restartBot()
                        elif cmd.startswith("joox"):
                            proses = text.split(" ")
                            urutan = text.replace(proses[0] + " ","")
                            r = requests.get("http://mnazria.herokuapp.com/api/joox?search={}".format(str(urllib.parse.quote(urutan))))
                            data = r.text
                            data = json.loads(data)
                            babi = ""
                            if data["picture"] == babi:
                                client.sendMessage(to,"Data Gambar Kosong")
                            else:
                                client.sendImageWithURL(to,data["picture"])
                            if data["lirik"] == babi:
                                client.sendMessage(to,"Data Lirik Kosong")
                            else:
                                client.sendMessage(to ,str(data["lirik"]))
                            if data["mp3"] == babi:
                                client.sendMessage(to,"Data Lagu Kosong")
                            else:
                                client.sendAudioWithURL(to,data["mp3"])
                        elif cmd.startswith("youtube"):
                                try:
                                    sep = msg.text.split(" ")
                                    kudanil = text.replace(sep[0] + " ","")
                                    r = requests.get("https://mnazria.herokuapp.com/api/ytdl?url={}".format(kudanil))
                                    data = r.text
                                    data = json.loads(data)
                                    ret = "Judul :\n{}\n".format(data["desc"])
                                    ret += "Deskripsi :\n{}\n".format(data["description_video"])
                                    ret += "Size Audio :{}\n".format(data["size_audio"])
                                    ret += "Size Video :{}\n".format(data["size_video"])
                                    ret += "Url Audio Download:\n{}\n".format(data["url_audio"])
                                    ret += "Url Video Download:\n{}\n".format(data["url_video"])
                                    client.sendMessage(to, str(ret))
                                except Exception as error:
                                    client.sendMessage(to,"Status: 404\nReason: Link Youtube {} tidak ditemukan\nExample: https://youtube.be/bla2".format(error))
                        elif cmd.startswith("stickergif"):
                              try:
                                  sep = msg.text.split("/")
                                  nom = sep[1].replace(" ","")
                                  arr = "line://ti/p/~{}".format(client.getProfile().userid)                                                                
                                  data = {                                                                                                                    
                                        "type": "template",
                                        "altText": "Mengirim Sticker",
                                        "template": {
                                            "type": "image_carousel",                                                                                               
                                            "columns": [
                                                {
                                                  "imageUrl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/IOS/sticker_animation@2x.png".format(nom),
                                                  "action": {                                                                                                               
                                                  "type": "uri",
                                                  " ": " ",
                                                  "uri": "https://line.me/ti/p/~cringelo"
                                                  }
                                                }
                                            ]
                                        }
                                  }
                                  sendTemplate(to,data)
                              except Exception as error:
                                  client.sendMessage(msg.to, "error\n" + str(error))
                            elif cmd.startswith("stickerpng"):
                              try:
                                  sep = msg.text.split("/")
                                  nom = sep[1].replace(" ","")
                                  arr = "line://ti/p/~{}".format(client.getProfile().userid)                                                                
                                  data = {                                                                                                                    
                                        "type": "template",
                                        "altText": "Mengirim Sticker",
                                        "template": {
                                            "type": "image_carousel",                                                                                               
                                            "columns": [
                                                {
                                                  "imageUrl": "https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png".format(nom),
                                                  "action": {                                                                                                               
                                                  "type": "uri",
                                                  " ": " ",
                                                  "uri": "https://line.me/ti/p/~cringelo"
                                                  }
                                                }
                                            ]
                                        }
                                  }
                                  sendTemplate(to,data)
                        elif cmd == 'mention':
                            group = client.getGroup(to)
                            midMembers = [contact.mid for contact in group.members]
                            midSelect = len(midMembers)//20
                            for mentionMembers in range(midSelect+1):
                                no = 0
                                ret_ = "「 Mention Group 」"
                                dataMid = []
                                for dataMention in group.members[mentionMembers*20 : (mentionMembers+1)*20]:
                                    dataMid.append(dataMention.mid)
                                    no += 1
                                    ret_ += "\n{}. @!".format(str(no))
                                ret_ += "\n「 Total {} Tag 」".format(str(len(dataMid)))
                                sendMention(to, ret_, dataMid)
            except Exception as error:
                client.sendMessage(to, "" + str(error)) 
                traceback.print_tb(error.__traceback__)
    except Exception as error:
        client.sendMessage(to, "" + str(error)) 
        traceback.print_tb(error.__traceback__)
        
while True:
    try:
        ops = clientPoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                clientBot(op)
                clientPoll.setRevision(op.revision)
    except Exception as error:
        client.sendMessage(to, "{}".format(str(error)))
        traceback.print_tb(error.__traceback__)  
