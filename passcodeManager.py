import datetime
import random
import send_mail

class CodeEntry():
    def __init__(self, passcode, timeLimit) -> None:
        self.passcode = passcode
        self.timeLimit =timeLimit

class CodeEntries():
    def __init__(self) -> None:
        self.entries = {}

    def add(self, id, passcode, timeLimit):
        self.entries[id]=CodeEntry(passcode, timeLimit)
        return

    def get(self, id):
        if id in self.entries:
            return self.entries[id]
        return CodeEntry(None, None)

    def remove(self, id):
        if id in self.entries:
            del self.entries[id]
        return
    
    def issue(self, id):
        newPasscode = str(random.randint(1,999999))
        timeLimit = datetime.datetime.now()+datetime.timedelta(minutes=5)
        self.entries[id]=CodeEntry(newPasscode, timeLimit)
        send_mail.send_passcode(newPasscode,id)
        return timeLimit

    