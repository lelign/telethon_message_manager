import asyncio
from telethon import TelegramClient, events
from telethon.utils import get_display_name
import string
from aiogram.types import Message # pip3 install aiogram
import os
import re
import shutil
import datetime
from datetime import datetime


from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import DeleteMessagesRequest
from telethon import types
from telethon import utils
from telethon.tl.types import ChannelParticipantsAdmins

'''
from https://my.telegram.org/apps
App api_id: 30603011
App api_hash: b19dcf65395bedabc414b0c05084c42c
App title: ign_alex_bot_application
Short name: IgnAlexBotApp
bot username ign_921_alex_bot
bot name ign_alex_bot
https://web.telegram.org/a/#-1001761952037 < = ntv channel
https://web.telegram.org/a/#-1003516778239 <= test channel
TOKEN = '8022469006:AAENQHhdpjB84mUPpiguAH4rAD-xhVIY4Yo'
# Channel(s) to monitor (can be username or ID)
# Use a list for multiple channels
my_channel_ids = ['@ign_alex_test_channel']
'''

#if os.name == 'nt':
#    _ = os.system('cls')
# For macOS and Linux (posix systems)
#else:
#    _ = os.system('clear')
 # assign log
API_ID = 30603011     # from https://my.telegram.org/apps
API_HASH = 'b19dcf65395bedabc414b0c05084c42c' # from https://my.telegram.org/apps
client = TelegramClient('ign', API_ID, API_HASH)
channel = "ign_alex_test_channel"
channel_name = 'test_ch_ign_alex'
# API ID and API HASH
api_id = 30603011
api_hash = 'b19dcf65395bedabc414b0c05084c42c'

entity_id = -1003516778239 # https://web.telegram.org/a/#-1003516778239 <= test channel
group_in_channel_id = -1003667572076 # https://web.telegram.org/a/#-1003667572076 <= test_ch_ign_alex

session_name = 'session_name'
session_name = 'phone'

chan_admin = []
client = TelegramClient(session_name, api_id, api_hash)


def create_log_dict():
    log_dict = {
                'date_time_now: ': '',
                'replayed: ': '', 
                'original_message_time: ': '',
                'original_message_ID: ':'',
                'original_message_sender_ID: ':'',
                'original_message_sender_full: ':'',
                'original_message_sender_disp: ':'',
                'original_message_text: ':'',
                'replayed_message_time: ': '',
                'replayed_message_ID: ':'',
                'replayed_message_sender_ID: ':'',
                'replayed_message_sender_full: ':'',
                'replayed_message_sender_disp:':'',
                'replayed_message_text: ':'', 
                'ban: ': '',
                'cause_to_delete: ': '',
                'message_to_ban: ':''
                }
    for key in log_dict.keys():
        log_dict[key] = False
    return log_dict 

def fill_and_write_logs(log_dict, log_error):
    if True:
        ''' check if sender already in ban_list'''
        if check_files_exist(log_error):
            ban_ids = set(line.strip() for line in open( os.path.join(work_dir, 'ban_list.txt') ) )
            for ban in ban_ids:
                if log_dict['original_message_sender_ID: '] in ban:
                    log_dict['ban: '] = True                                                        
                    log_dict['message_to_ban: '] = 'Вы добавлены в бан, больше не пишите сюда.'
                    log_dict['cause_to_delete: '] = 'already in ban'
                    break
            if not log_dict['ban: ']:
                '''admin's ban''' 
                #breakpoint()       
                if (log_dict['replayed: ']  
                    and log_dict['replayed_message_sender_ID: '] == 'None'  
                    and log_dict['replayed_message_text: '] == 'В бан'
                    ):
                    #breakpoint()
                    log_dict['ban: '] = True
                    log_dict['message_to_ban: '] = 'Администратор канала отправил вас в бан'
                    with  open( os.path.join(work_dir, 'ban_list.txt'), 'a') as f_ban:
                        f_ban.write(log_dict['original_message_sender_disp: '] + ' ' +
                                    log_dict['original_message_sender_ID: '] + ' ' +
                                    'Администратор отправил в бан\n'
                                    )

                '''check words and ban'''            
                obscene_words = set(line.strip() for line in open(os.path.join(work_dir, 'obscene.txt'), encoding="utf-8"))
                bad_messages = set(line.strip() for line in open(os.path.join(work_dir, 'bad_messages.txt'), encoding="utf-8"))
                
                client_wrote = re.sub(r'[^a-zA-Zа-яА-Я]', ' ', log_dict['original_message_text: '] ).lower().split(' ')
                
                '''check if sender sent obscene'''                
                for word in client_wrote: # log_dict['original_message_text: ']:
                    #breakpoint()
                    if word.lower() in obscene_words:
                        log_dict['cause_to_delete: '] = word 
                        log_dict['ban: '] = True
                        log_dict['message_to_ban: '] = 'Вы добавлены в бан причина: ' + '<' + word +'>'
                        with  open( os.path.join(work_dir, 'ban_list.txt'), 'a') as f_ban:
                            f_ban.write(log_dict['original_message_sender_disp: '] + ' ' +
                                    log_dict['original_message_sender_ID: '] + ' ' +
                                    'добавлен в бан причина <' + word + '> '+ log_dict['original_message_text: '] + '\n'
                                    )
                        break
                for bad_m in bad_messages:
                        if bad_m.lower() in client_wrote:
                            log_dict['cause_to_delete: '] = bad_m
                            log_dict['ban: '] = True
                            log_dict['message_to_ban: '] = 'Вы добавлены в бан причина: ' + '<' + bad_m +'>'
                            with  open( os.path.join(work_dir, 'ban_list.txt'), 'a') as f_ban:
                                f_ban.write(log_dict['original_message_sender_disp: '] + ' ' +
                                        log_dict['original_message_sender_ID: '] + ' ' +
                                        'добавлен в бан причина <' + bad_m + '> '+ log_dict['original_message_text: '] + '\n'
                                        )
                            break

        log_dict['date_time_now: '] = '\t\t' + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for key in log_dict.keys():
            print(f'{key} {log_dict[key]}')
        try:
            if not os.path.isfile('events.txt'):
                with open('events.txt', 'w', encoding='utf-8') as f:
                    pass
            #with open('events.txt', 'r') as f_read:
            #    prev_mes = f_read.read()
            with open('events.txt', 'a', encoding='utf-8') as f:
                f.write('\n')   
            with open('events.txt', 'a', encoding='utf-8') as f:
                for key in log_dict.keys():
                    f.write(f'{key}\t\t{log_dict[key]} \n')
            #    f.write(prev_mes)
        except Exception as e:
                log_error.append(f"\n\tError could'nt write, replayed is {log_dict['replayed: ']} {e}")
        return log_dict, log_error

def check_files_exist(log_error):
    #source_files = ('bad_messages.txt' , 'obscene.txt', 'ban_list.txt')
    files_exist = True
    global work_dir
    #global log_dict
    for file in source_files:    
        destination_file = os.path.join(work_dir, file)
        try:
            if not os.path.exists(destination_file):
                shutil.copyfile(file, destination_file)  
        except shutil.SameFileError:
            files_exist = False
            log_error.append('Error shutil.SameFileError: ' + str(file))
            break
        except PermissionError:
            files_exist = False
            log_error.append('Error Permission denied')
            break
        except FileNotFoundError:
            files_exist = False
            #print(f"One of the files was not found: {file} {destination_file}")
            log_error.append('One of the files was not found: ' + str(file) + ' ' + str(destination_file))
            break
        return files_exist

    #oscene_words = set(line.strip() for line in open(os.path.join(work_dir, 'obscene.txt'), encoding="utf-8"))
    #return obscene_words

async def get_sender_name_by_id(user_id):
    global log_error
    full_name = False
    display_name = False
    try:
        # Get the full entity (User, Chat, or Channel) by its ID
        entity = await client.get_entity(user_id)
        #print('\nentity:\n', entity)
        
        # If it's a User, you can access first_name, last_name, or username
        if hasattr(entity, 'first_name'):
            full_name = f"{entity.first_name or ''} {entity.last_name or ''}".strip()
            # Use telethon.utils.get_display_name() for a robust solution
            from telethon import utils
            display_name = utils.get_display_name(entity)
            #print(f"Sender ID: {user_id}, Name: {full_name}, Display Name: {display_name}, Username: @{entity.username}" if entity.username else f"Sender ID: {user_id}, Name: {full_name}, Display Name: {display_name}")
            return display_name, full_name
        elif hasattr(entity, 'title'):
            # If it's a Channel or Chat
            #print(f"Chat/Channel ID: {user_id}, Title: {entity.title}")
            return entity.title, full_name
        else:
            #print(f"Entity found but name/title not available for ID: {user_id}")
            return display_name, full_name

    except ValueError as e:
        #print(f"Error: Could not find the entity corresponding to {user_id}. Ensure you have 'encountered' this user (e.g., in a common chat).")
        log_error.append('Error: Could not find the entity corresponding to {user_id}')
        return None
    except Exception as e:
        log_error.append('Error: An unexpected error occurred: {e}')
        #print(f"An unexpected error occurred: {e}")
        return None

@client.on(events.NewMessage())  # <= all chats
async def my_event_handler(event):
    global source_files
    global work_dir
    global log_error
    
    #get_oscene_words(source_files, work_dir, log_array )
    #log_dict_len = len(log_array)
      
    try:
        #async for dialog_array in client.iter_dialog_arrays():
        ''' admin wrote <В бан>'''
        display_name = False
        full_name = False
        
        async for message in client.iter_messages(group_in_channel_id, limit=1):
            log_dict = create_log_dict()
            '''admin message ?'''
            if message.is_reply: 
                log_dict['replayed: '] = True                                
                # Get the original (parent) message object
                original_message = await message.get_reply_message()
                if original_message:
                    log_dict['original_message_time: '] = original_message.date
                    log_dict['original_message_ID: '] = str(original_message.id)
                    log_dict['original_message_sender_ID: '] = str(original_message.sender_id)
                    if original_message.sender_id:
                        display_name, full_name = await get_sender_name_by_id(original_message.sender_id)
                        log_dict['original_message_sender_full: '] = display_name
                        log_dict['original_message_sender_disp: '] = full_name
                    log_dict['original_message_text: '] = str(original_message.text).replace('\n', '').replace('\r', '').strip()
                    ''''''
                    log_dict['replayed_message_time: '] = message.date
                    log_dict['replayed_message_ID: '] = str(message.id)
                    log_dict['replayed_message_sender_ID: '] = str(message.sender_id)
                    if message.sender_id:
                        display_name_repl, full_name_repl = await get_sender_name_by_id(message.sender_id)
                        log_dict['replayed_message_sender_full: '] = display_name_repl
                        log_dict['replayed_message_sender_disp: '] = full_name_repl
                    log_dict['replayed_message_text: '] = str(message.text).replace('\n', '').replace('\r', '').strip()
                else:
                    log_error.append(f"\n\tError Could not fetch the original message (it might be too old or deleted")
               
                log_dict, log_error = fill_and_write_logs(log_dict, log_error)

                  
 
            else:
                log_dict['replayed: '] = False
                log_dict['original_message_time: '] = message.date
                log_dict['original_message_ID: '] = str(message.id)
                log_dict['original_message_sender_ID: '] = str(message.sender_id)
                if message.sender_id:
                    display_name, full_name = await get_sender_name_by_id(message.sender_id)
                    log_dict['original_message_sender_full: '] = display_name
                    log_dict['original_message_sender_disp: '] = full_name
                log_dict['original_message_text: '] = str(message.text).replace('\n', '').replace('\r', '').strip()

                log_dict, log_error = fill_and_write_logs(log_dict, log_error)


 
  
    except Exception as e:
        #print(f"\n\tError for dialog_array in client.iter_dialog_arrays(): {e}")
        log_error.append(f"\n\tError for dialog_array in client.iter_dialog_arrays(): {e}")
    
    for log in log_error:
        if 'Error' in log:
            print(f' \t\tthis error: \n\t\t\t{log}')
            try:
                if not os.path.isfile('error.log'):
                            with open('error.log', 'w', encoding='utf-8') as f:
                                pass
                #with open('error.log', 'r') as f_read:
                #    prev_mes = f_read.read()
                with open('error.log', 'a') as f:
                    f.write('\n\t' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") )  
                with open('error.log', 'a') as f:
                    for log in log_error:
                        f.write(f'{log}  \n')
                #    f.write(prev_mes)

            except:
                pass
    
    

async def main():
    await client.start()
    print("Client connected and listening for new messages...")

    await client.run_until_disconnected() # Keep the client running
if __name__ == '__main__':
    HOME = os.path.expanduser('~')
    #global log_dict
    global log_error
    log_error =[]
    global work_dir
    work_dir = os.path.join(HOME + "\\Documents\\Message_menager")
    log_error.append(work_dir)
    global source_files
    source_files = ('bad_messages.txt' , 'obscene.txt', 'ban_list.txt')
    #log_dict.append('work_dir: ' + str(work_dir))
    # Ensure the script runs within an asyncio event loop
    asyncio.run(main())














'''
async def my_event_handler(event):
    msg = event.text    

    print(f"[M] {msg}\n\n")
'''








'''
try:
    entity = 'шабашка'
    async for message in client.iter_messages(entity_id, search=entity):
        print(f"Found message (ID: {message.id}): {message.text}")
    sent_message = await client.send_message(entity, 'This message will be deleted shortly!')
    print(f"Sent message with ID: {sent_message.id}")
    await asyncio.sleep(3)
    await client.delete_messages(entity=entity, message_ids=[sent_message.id])  
except Exception as e:
        print(f"Error on start deleting message: {e}")
        

  
print(f"Deleted message with ID: {sent_message.id}")
'''




'''
async def delete_specific_message():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        # Delete a single message
        await client.delete_messages(chat_entity, message_ids=[message_id_to_delete])
        print(f"Message {message_id_to_delete} in entity {chat_entity} deleted (if permissions allowed).")
'''        




    
'''
async def main():
    async for message in client.iter_messages(-1003516778239, limit=5):
        print(message.id, message.text)


with client:
    client.loop.run_until_complete(main())
'''


'''
try:
    # print(f"New message in {event.chat.title}:\t\t {event.text}") # moved
    
    # print(event)
    # words_list = event.text.split()
    # print("words_list", words_list)
    message_words = set(event.text.translate(str.maketrans('', '', string.punctuation)).split())
    filtered_message = event.text
    contains_ban_word = False
    obscene = ""
    bad_message = ""
    for word in message_words:
        if word.lower() in OBSCENE_WORDS: # or word.lower() in:
            #filtered_message = filtered_message.replace(word, "*" * len(word))
            obscene = word
            print ("obscene \t\t\t", obscene)
            contains_ban_word = True
    bad_messages = set(line.strip() for line in open('bad_messages.txt', encoding="utf-8"))
    for bad_m in bad_messages:
        if bad_m.lower() in event.text.lower():
            bad_message = bad_m
            print ("bad_message \t\t\t", bad_message)
            contains_ban_word = True
    
    
    #print("filtered_message", filtered_message)
    message_id = event.message.id
   # Get the ID of the user who sent the message
    user_id = event.sender_id
    entity = await client.get_entity(user_id)
    entity_username_user_id = entity.username
    print(f"\nentity_username_user_id  \t\t{entity_username_user_id}")
    # Alternatively, get the full user object
    sender = await event.get_sender()
    #print(f"sender  {sender}\n\n")
    sender_id = sender.id
    print(f"\nsender_id  \t\t{sender_id}")
    entity = await client.get_entity(sender_id)
    entity_username_sender_id = entity.username
    print(f"\nentity_username_sender_id \t\t{entity_username_sender_id}")
    # Or get the entity directly from the ID
    # user_entity = await client.get_entity(user_id)
    if contains_ban_word:
        message_id_to_delete = message_id
        print(f"Received message fom user_id \t{user_id} sender_id \t{sender_id} with ID: \t{message_id}")
        try:
            # The method takes a list of message IDs
            await client.delete_messages(entity=entity_id, message_ids=[message_id_to_delete])
            print(f"\nMessage {event.text} ID {message_id_to_delete} deleted from entity {entity_id}.")
        except Exception as e:
            print(f"Error deleting message: {e}")
except Exception as e:
            print(f"Global error: {e}")
'''
