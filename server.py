import zmq, time
from threading import Thread
from constPS import * #-

context = zmq.Context()
p = "tcp://"+ HOST +":"+ PORT
p2 = "tcp://"+ HOST +":"+ PORT2

#uma porta eu bindei o de subscrição receber mensagens de qualquer cliente publisher conectado
sub = context.socket(zmq.SUB)
sub.bind(p)
sub.setsockopt_string(zmq.SUBSCRIBE, "")  #servidor recebe qualquer tópico

#a outra porta bindei o de publicação para enviar mensagens a qualquer cliente subscriber conectado
s = context.socket(zmq.PUB)
s.bind(p2)

class Messages:
        group_msg = None

        def __init__(self):
                super().__init__()

        def get_group_msg(self):
                return self.group_msg
        @classmethod
        def update_group_msg(cls, group_msg):
                cls.group_msg = group_msg

def get_msg():
        while True:
                Messages.update_group_msg(sub.recv())

def send_msg():
        while True:
                group_msg = Messages().get_group_msg()
                if group_msg is not None:
                        s.send(group_msg)
                        time.sleep(0.5)
                        Messages.update_group_msg(None)

gt_msg = Thread(target=get_msg)
snd = Thread(target=send_msg)
gt_msg.start()
snd.start()
