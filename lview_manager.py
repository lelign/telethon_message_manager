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
from pathlib import Path

#API_ID = 30603011     # from https://my.telegram.org/apps
#API_HASH = 'b19dcf65395bedabc414b0c05084c42c' # from https://my.telegram.org/apps
# client = TelegramClient('ign', API_ID, API_HASH)
#channel = "ign_alex_test_channel"
#channel_name = 'test_ch_ign_alex'
# API ID and API HASH
#api_id = 30603011

#api_hash = 'b19dcf65395bedabc414b0c05084c42c'
#api_hash = '27d3fd3d12a25884f4ef26c6db030a8a'
'''
from https://my.telegram.org/apps
app_title = 'ignalexbotapplication'
short_name = 'ignalexbota'
api_id = 35593352
api_hash = '27d3fd3d12a25884f4ef26c6db030a8a'
'''

#           
#           27d3fd3d12a25884f4ef26c6db030a8a
api_hash = '27d3fd3d12a25884f4ef26c6db030a8a'
#       35593352
api_id = 35593352
session_name = 'lview'
group_in_channel_id = -1003591196682 # lview_smartphone_channel Chat https://web.telegram.org/a/?account=2#-1003591196682 lview 
#-1003591196682
client = TelegramClient(session_name, api_id, api_hash)

def create_log_dict():
    log_dict = {'____________________________________________':'',
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
                'message_to_ban: ':'',
                'ban_list: ':'',
                'obscene: ':'',
                'bad_message: ':''
                }
    for key in log_dict.keys():
        if '____________________________________________' in key:
            log_dict[key] = '#'
        else:
            log_dict[key] = False
    return log_dict 

def make_desigion(log_dict, log_error, event):
    #global source_files
    cp_files = cp_source_files(source_files, log_error)
    global work_dir
    #global source_files
    global socseti_manager

    if True:
        ''' check if sender already in ban_list'''
        if check_files_exist(log_error):
            if not log_dict['ban: ']: #  log_dict['ban: '] = True line 331
                #breakpoint()
                #ban_ids = set()
                #file_soc = os.path.join(socseti_manager, 'ban_list.txt')
                try:
                    ban_ids = set(line.strip() for line in open(
                                                                os.path.join(
                                                                            socseti_manager, 
                                                                            'ban_list.txt'
                                                                            ), 
                                                                            encoding='utf-8'
                                                                )
                                )       
                    log_dict['ban_list: '] = True   
                except:
                    ban_ids = set(line.strip() for line in open( 'ban_list.txt', encoding='utf-8' ) )
                    log_dict['ban_list: '] = False
                '''check if client in ban already'''
                #breakpoint()
                if len(ban_ids) > 0:
                    for ban_id in ban_ids:                    
                        if str(log_dict['original_message_sender_ID: ']) in ban_id:
                            log_dict['ban: '] = True                                                        
                            log_dict['message_to_ban: '] = 'Вы добавлены в бан, больше не пишите сюда.'
                            log_dict['cause_to_delete: '] = 'уже в бане'
                            break
                        if str(log_dict['replayed_message_sender_ID: ']) in ban_id:
                            log_dict['ban: '] = True                                                        
                            log_dict['message_to_ban: '] = 'Вы добавлены в бан, больше не пишите сюда.'
                            log_dict['cause_to_delete: '] = 'уже в бане'
                            break
               
            #prev = log_dict['ban: ']
            #prev_type = type(prev)
            
            if not log_dict['ban: ']: #  log_dict['ban: '] = True line 115
                #breakpoint()
                client_wrote = []
                try:
                    client_wrote = re.sub(r'[^a-zA-Zа-яА-Я]', ' ', log_dict['original_message_text: '] ).lower().split(' ')
                except:
                    client_wrote.append(str(log_dict['original_message_text: ']))
                client_words_repl = []   
                try:
                    client_words_repl = re.sub(r'[^a-zA-Zа-яА-Я]', ' ', log_dict['replayed_message_text: '] ).lower().split(' ')
                except:
                    client_words_repl.append(str(log_dict['replayed_message_text: ']))
                client_wrote.extend(client_words_repl)
                #breakpoint()
  
                
                
                '''set obscene'''
                try:                    
                    obscene_words = set(line.strip() for line in open( 
                                                                        os.path.join(socseti_manager, 'obscene.txt'), 
                                                                        encoding="utf-8"
                                                                        )
                                        )
                    log_dict['obscene: '] = True
                except:
                    log_dict['obscene: '] = False        
                    obscene_words = set(line.strip() for line in open('obscene.txt', encoding="utf-8"))
                '''set bad messages'''
                try:                       
                    bad_messages = set(line.strip() for line in open
                                                                    (os.path.join(socseti_manager, 'bad_messages.txt'), 
                                                                     encoding="utf-8"
                                                                     )
                                        )
                    log_dict['bad_message: '] = True
                except:
                    log_dict['bad_message: '] = False        
                    bad_messages = set(line.strip() for line in open('bad_messages.txt', encoding="utf-8"))

                '''check if client sent obscene or bad message'''   
                words = []     
                '''check if client sent obscene'''           
                for word in client_wrote: # log_dict['original_message_text: ']:
                    #breakpoint()
                    if word.lower() in obscene_words:
                        words.append(word)
                        log_dict['cause_to_delete: '] = word
                        log_dict['ban: '] = True
                        log_dict['message_to_ban: '] = 'Вы добавлены в бан причина: ' + '<' + word +'>'                                                
                        break
                '''check if client sent bad message'''
                for word in bad_messages:
                        if word.lower() in client_wrote:
                            words.append(word)
                            log_dict['cause_to_delete: '] = words
                            log_dict['ban: '] = True
                            log_dict['message_to_ban: '] = 'Вы добавлены в бан причина: ' + '<' + str(words) +'>'
                            break


            event_time = '\t\t' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            '''write to ban list'''            
            if log_dict['ban: ']:
                #write_to_ban_list(log_dict, log_error)
                try:
                    if log_dict['replayed_message_sender_ID: '] > \
                                log_dict['original_message_sender_ID: ']:
                                log_dict['original_message_sender_ID: '] = str(log_dict['replayed_message_sender_ID: ']) + ' re'
                                log_dict['original_message_sender_disp: '] = log_dict['replayed_message_sender_disp: ']
                except:
                    pass
                to_write = str(event_time) + '\n' + str(log_dict['original_message_sender_disp: ']) + ' ' + \
                                str(log_dict['original_message_sender_ID: ']) + ' ' + \
                                'добавлен в бан причина <' + str(log_dict['cause_to_delete: ']) + '> '+ \
                                str(log_dict['original_message_text: ']) + '\n'                
                with open('ban_list.txt', 'a', encoding='utf-8') as f:
                        f.write(to_write)  
                                 
                try:      
                    with open( os.path.join(socseti_manager, 'ban_list.txt'), 'a', encoding='utf-8') as f_ban:
                        f_ban.write(to_write)
                    log_dict['ban_list: '] = True
                except:
                    log_dict['ban_list: '] = False
                
                 


        log_dict['date_time_now: '] = event_time
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
    source_files_bm_o = ('bad_messages.txt', 'obscene.txt')
    for file in source_files_bm_o:    
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

def cp_source_files(source_files, log_error):
    global socseti
    global socseti_manager
    result = True 
    path_socseti = Path(socseti)
    source_files_bm_o = ('bad_messages.txt', 'obscene.txt')
    if path_socseti.is_dir():
        path_message_manager = Path(socseti_manager)
        if not path_message_manager.is_dir():
            os.mkdir(str(path_message_manager))
        for file in source_files_bm_o:
            try:
                destinaation_file = os.path.join(str(path_message_manager), file)

                if not os.path.isfile(destinaation_file):
                    shutil.copy(file, destinaation_file)

                '''
                if os.path.isfile(destinaation_file):
                    shutil.copy(destinaation_file, file)
                else:
                    shutil.copy(file, destinaation_file)                
                '''
                
            except Exception as e:
                log_error.append(f"\n\tError cp source files: {e}")
                result = False
                break
    return result

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
    #print(str(event))
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
                    log_dict['replayed_message_text: '] = str(message.text).replace('\n', '').replace('\r', '').strip()
                    if message.sender_id:
                        display_name_repl, full_name_repl = await get_sender_name_by_id(message.sender_id)
                        log_dict['replayed_message_sender_full: '] = display_name_repl
                        log_dict['replayed_message_sender_disp: '] = full_name_repl
                    else:
                        if log_dict['replayed_message_text: '] == 'В бан':
                            log_dict['replayed_message_sender_full: '] = '\t\tADMIN_F'
                            log_dict['replayed_message_sender_disp: '] = '\t\tADMIN_D'
                            log_dict['ban: '] = True
                            log_dict['message_to_ban: '] = 'Администратор канала отправил вас в бан'
                            log_dict['cause_to_delete: '] = 'решение адимнистратора' 
                            log_dict['replayed_message_sender_ID: '] = '\t\tADMIN_ID'            
                else:
                    log_error.append(f"\n\tError Could not fetch the original message (it might be too old or deleted")
               
                 
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

            log_dict, log_error = make_desigion(log_dict, log_error, event)
            '''here may be log_dict returned witn ban'''
            #print(f"Message ID: {message.id}, Text: {message.text} \
            #      original_message_sender_ID {message.sender_id}")
            
            if log_dict['ban: ']:
                
                '''personal answer to sender'''
                if message.sender_id:
                    await client.send_message(message.sender_id, log_dict['message_to_ban: '])
                '''replay message'''
                await client.send_message(
                                            entity=group_in_channel_id,
                                            message='Сообщение удалено',
                                            reply_to=message.id
                                            )
                '''delete message'''               
                await client.delete_messages(
                                                entity=group_in_channel_id, 
                                                message_ids=[message.id]
                                            ) 


 
  
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
    

    result = True 
    path_socseti = Path("W:/ВИДЕО_ДЛЯ_ЭФИРА/СОЦСЕТИ")
    if path_socseti.is_dir():
        path_messege_manager = Path("W:/ВИДЕО_ДЛЯ_ЭФИРА/СОЦСЕТИ/MESSAGE_MANAGER")
        if not path_messege_manager.is_dir():
            os.mkdir(str(path_messege_manager))
        source_files_bm_o = ('bad_messages.txt', 'obscene.txt')
        for file in source_files_bm_o:
            try:
                if not os.path.isfile(os.path.join(str(path_messege_manager), file)):
                    shutil.copy(file, os.path.join(str(path_messege_manager), file))
            except Exception as e:
                log_error.append(f"\n\tError cp source files: {e}")
                result = False
                break
    return result    

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
    #work_dir = os.path.join(HOME + "\\Documents\\Message_menager")
    work_dir = os.getcwd()
    log_error.append(work_dir)
    global source_files
    source_files = ('bad_messages.txt' , 'obscene.txt', 'ban_list.txt')
    global socseti
    socseti = 'W:/ВИДЕО_ДЛЯ_ЭФИРА/СОЦСЕТИ'
    global socseti_manager
    socseti_manager = "W:/ВИДЕО_ДЛЯ_ЭФИРА/СОЦСЕТИ/MESSAGE_MANAGER"
    #log_dict.append('work_dir: ' + str(work_dir))
    # Ensure the script runs within an asyncio event loop
    asyncio.run(main())













