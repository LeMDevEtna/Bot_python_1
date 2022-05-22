import fbchat 
from fbchat import Client, Message
from getpass import getpass
import re

fbchat._util.USER_AGENTS = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"]
fbchat._state.FB_DTSG_REGEX = re.compile(r'"name":"fb_dtsg","value":"(.*?)"') 
username = str(input("Username: ")) 
client = fbchat.Client('mohamed.950@hotmail.fr', 'Afhmi159!') 
no_of_friends = int(input("Number of friends: ")) 
for i in range(no_of_friends): 
    name = str(input("Name: ")) 
    
    friends = client.searchForUsers(name)#client.getUsers(name)  # return a list of names 
    friend = friends[0] 
    msg = str(input("Message: ")) 
    sent = client.send(Message(text=msg),
            thread_id=friend.uid)#self.send(Message(text=msg), thread_id=thread_id, thread_type=thread_type)#sendMessage(msg, thread_id=friend.uid)#client.send(friend.uid, msg) 
    if sent: 
        print("Message sent by bot momo for a test!") 