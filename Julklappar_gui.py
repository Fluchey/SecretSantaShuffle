import threading, time, random, smtplib, ssl
from tkinter import *
from tkinter import ttk, filedialog, messagebox

def setStatus(msg):
    _status_msg.set(msg)

def addParticipant():
    next_row = len(_all_participants)

    participant_mail = Entry(_participants_mailframe)
    participant_mail.grid(row=next_row, column=0, sticky=(W))

    participant_name = Entry(_participants_mailframe)
    participant_name.grid(row=next_row, column=1, sticky=(W))

    _all_participants.append((participant_mail, participant_name))

    setStatus("New field added")

def sendMail():
    if len(_all_participants) <= 1:
        setStatus("Add at least two participants!")
        return

    p_dict = {}

    for mail, name in _all_participants:
        p_dict[mail.get()] = name.get()
    
    list_to_shuffle = list(p_dict.keys())
    ref_list = list_to_shuffle[:]

    while checkUnique(list_to_shuffle, ref_list):
        random.shuffle(list_to_shuffle)

    for giver, taker in zip(list_to_shuffle, ref_list):
        print(giver, "ger till", taker)
        return
    try:
        port = 465
        printDebug("ASD")
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(_sender_mail, _sender_mailpassword)

            for giver, taker in zip(list_to_shuffle, ref_list):
                msg = 'Subject: {}\n\n{}'.format("Din julklappsperson", "Grattis du ska ge en present till " + p_dict[taker])
                server.sendmail("hemligajulafton@gmail.com", giver, msg)
    except Exception as e:
        print(e)
        setStatus(e)


def checkUnique(list1, list2):
    for p1, p2 in zip(list1, list2):
        if p1 == p2:
            return True
    return False

def addDebug():
    _sender_mail.set("hemligajulafton@gmail.com")
    _sender_mailpassword.set("secretSanta")

    for i in range(3):
        addParticipant()

    _all_participants[0][0].insert(0, "anton.fluch@gmail.com")
    _all_participants[0][1].insert(0, "AntonGmail")
    _all_participants[1][0].insert(0, "anton.fluch@hotmail.com")
    _all_participants[1][1].insert(0, "AntonHotmail")

def printDebug(*msg):
    print(msg)

if __name__ == "__main__":
    # LIST TO HOLD ALL PARTICIPANTS
    _all_participants = []

    _root = Tk()
    _root.title('HemligaTomten')

    _mainframe = ttk.Frame(_root, padding='5 5 5 5')
    _mainframe.grid(row=0, column=0, sticky=(E, W, N, S))

    _sender_mailframe = ttk.LabelFrame(_mainframe, text='Santas mail credentials', padding='5 5 5 5')
    _sender_mailframe.grid(row=0, column=0, sticky=(E, W, S, N)) 
    _sender_mailframe.columnconfigure(0, weight=1)
    _sender_mailframe.rowconfigure(0, weight=1)

    _sender_mail = StringVar()
    _sender_mail_entry = ttk.Entry(_sender_mailframe, width=40, textvariable=_sender_mail)
    _sender_mail_entry.grid(row=0, column=0, sticky=(E, W, S, N), padx=5)

    _sender_mailpassword = StringVar()
    _sender_mailpassword_entry = ttk.Entry(_sender_mailframe, show="*",  width=40, textvariable=_sender_mailpassword)
    _sender_mailpassword_entry.grid(row=0, column=1, sticky=(E, W, S, N), padx=5)

    _participants_mailframe = ttk.LabelFrame(_mainframe, text='Participants e-mail and name', padding='5 5 5 5')
    _participants_mailframe.grid(row=1, column=0, sticky=(E, W, S, N))
    _participants_mailframe.columnconfigure(0, weight=1)
    _participants_mailframe.rowconfigure(0, weight=1)

    _add_participant_button = Button(_participants_mailframe, text='Add', command=addParticipant, height=1, width=1)
    _add_participant_button.grid(row=0, column=3, sticky=(W, N))

    _send_mail_button = Button(_participants_mailframe, text='Send mail', command=sendMail, height=1)
    _send_mail_button.grid(row=len(_all_participants) + 1, column=3, sticky=(W, N))

    _status_frame = ttk.Frame(_root, relief='sunken', padding='2 2 2 2')
    _status_frame.grid(row=1, column=0, sticky=(E, W, S))
    _status_msg = StringVar()
    _status_msg.set('Press the ADD button to enter participant')
    _status = ttk.Label(_status_frame, textvariable=_status_msg, anchor=W)
    _status.grid(row=0, column=0, sticky=(E, W))

    addDebug()
    
    _root.mainloop()
