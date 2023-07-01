import zmq, time
from constPS import * #-
from threading import Thread

context = zmq.Context()
p = "tcp://"+ HOST +":"+ PORT
p2 = "tcp://"+ HOST +":"+ PORT2
s = context.socket(zmq.SUB)
pub = context.socket(zmq.PUB)

def topic_connection(topic):
        s.connect(p2)
        s.setsockopt_string(zmq.SUBSCRIBE, topic)
        pub.connect(p)

def get_msg():
        while True:
                group_msg = s.recv()
                print (bytes.decode(group_msg))

def send_msg(topic, user):
        while True:
                msg = input()
                msg = str.encode(topic + " " + user + " " + msg)
                pub.send(msg)
                time.sleep(0.5)

print("Username:")
user = str(input())
print ("1 for topic, 2 for direct message")
top_or_dir = None
while top_or_dir not in [1, 2]:
        top_or_dir = int(input())
if top_or_dir == 1:
        print("Topic name:")
        topic = str(input())
        topic_connection(topic)
        gt = Thread(target=get_msg)
        snd = Thread(target=send_msg, args=(topic, user,))
        gt.start()
        snd.start()
else:
        topic_connection(user)
        print("Name to send:")
        name = str(input())
        gt = Thread(target=get_msg)
        snd = Thread(target=send_msg, args=(name, user,))
        gt.start()
        snd.start()





