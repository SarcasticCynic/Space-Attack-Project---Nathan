import enum

class Contact():
    def __init__(self, x, y, attrlist,):
        self.x_hysteresis = [x]
        self.y_hysteresis = [y]
        self.attributes = {}
        self.attrlist = attrlist

class SensorArray:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SensorArray, cls).__new__(cls)
            cls.contacts = {}
        return cls.instance

    def addContact(self, x, y, ref, attrlist) :
        self.contacts[id(ref)] = Contact(x, y, attrlist)

    def updateContact(self, x, y, ref):
        self.contacts[id(ref)].x_hysteresis.append(x)
        self.contacts[id(ref)].y_hysteresis.append(y)

    def ridContact(self, ref):
        del self.contacts[id(ref)]
