# Home task bot v.1.2.1

import json
import vk_api
import requests

from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from const import *
from driveManager import DriveManager

import pprint
import io
import vk_api

driveManager = DriveManager('data/dataFile.json', '1-3NBgarr57RzAn7iyr3-jQP8CEkEaf0S')

driveManager.setFileId(driveManager.findFile())
driveManager.download()

data = []
try:
    with open('data/dataFile.json', 'r') as file:
        data = json.load(file)
except:
    pass

vk_session = vk_api.VkApi(token=TOKEN)
vk_session._auth_token()

vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, PUBLIC_ID)

print("Bot has been launched.")

while True:
    try:
        for event in longpoll.listen():
            print("there is new event - " + str(event.type))
            if (event.type == VkBotEventType.MESSAGE_NEW):
                print(str(event.object.from_id) + " - " + event.object.text)
                if (event.from_chat):
                    request = event.object.text
                    if ("$ввести" in request.lower()):
                        toAddArr = request.split(' ', 3)
                        if (len(toAddArr) == 4):
                            print(request)
                            data.append({'date': toAddArr[1], 'subject': toAddArr[2], 'content': toAddArr[3]})
                            with open("data/dataFile.json", "w") as file:
                                json.dump(data, file)
                            
                            driveManager.load()

                            vk.messages.send(chat_id = event.chat_id, message = "Информация записана!", random_id = get_random_id())
                        print(len(toAddArr))
                    elif (request.lower() == "$посмотретьвсе"):
                        if len(data) > 0:
                            for dataCell in data:
                                vk.messages.send(chat_id = event.chat_id, message = "Дата: " + dataCell['date'] + "; Предмет: " + dataCell['subject'] + "; Д/з: " + dataCell['content'], random_id = get_random_id())
                        else:
                            vk.messages.send(chat_id = event.chat_id, message = "Нет информации!", random_id = get_random_id())
                    elif ("$посмотреть" in request.lower()):
                        toAddArr = request.split(' ')
                        if (len(toAddArr) == 2):
                            isThereHomeTask = False
                            if len(data) > 0:
                                for dataCell in data:
                                    if (dataCell['date'] == toAddArr[1]):
                                        vk.messages.send(chat_id = event.chat_id, message = "Предмет: " + dataCell['subject'] + "; Д/з: " + dataCell['content'], random_id = get_random_id())
                                        isThereHomeTask = True
                            else:
                                vk.messages.send(chat_id = event.chat_id, message = "Нет информации!", random_id = get_random_id())
                            if (not isThereHomeTask):
                                vk.messages.send(chat_id = event.chat_id, message = "Нет информации!", random_id = get_random_id())
                        else:
                            print(len(toAddArr))
                    elif (request.lower() == "$очиститьвсе"):
                        data = []
                        with open("data/dataFile.json", 'w') as file:
                            file.write("")
                        
                        driveManager.deleteAll()

                        vk.messages.send(chat_id = event.chat_id, message = "Данные очищены.", random_id = get_random_id())
                    elif (request.lower() == "$привет"):
                        vk.messages.send(chat_id = event.chat_id, message = "Привет!", random_id = get_random_id())
    except requests.exceptions.Timeout:
        print("Timeout occured")