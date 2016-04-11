import xml.dom.minidom
import datetime
import os
import random
import lib.vlc as vlc

dayMap = {'U':0,"M":1,"T":2,"W":3,"R":4,"F":5,"S":6}

DOMTree = xml.dom.minidom.parse("test/blocks.xml")
collection = DOMTree.documentElement
blocks = collection.getElementsByTagName("block")

class block:
    def __init__(self):
        self.name = ""
        self.priority = 0
        self.contents = []
        self.start = datetime.timedelta()
        self.end = datetime.timedelta()

    #returns a file path to be played, chosen from a random content
    def getFile(self):
        rand = random.randint(0, self.contents.__len__() - 1)
        return self.contents[rand].getFile()

class content:
    global orders
    orders = {"random":0, "r":0, "sequential":1, "s":1}
    def __init__(self, order, pathfiles):
        self.pathfiles = []
        self.files = []
        self.played = []
        self.order = orders[order]
        self.pathfiles = pathfiles
        for tvf in self.pathfiles:
            self.buildFiles(tvf)

    def buildFiles(self, tvf):
        i = vlc.Instance()
        for root, dirs, files in os.walk(tvf.path):
            files = [ fi for fi in files if fi.endswith(('.mkv', '.mp4')) ]
            for file in files:
                f = os.path.join(root, file)
                m = i.media_new(f)
                m.parse()
                duration = m.get_duration() / 1000 #convert from ms to seconds
                #check if file is within duration bounds
                if (tvf.maxduration is 0 or duration <= tvf.maxduration) and (tvf.minduration is 0 or duration >= tvf.minduration):
                    self.files.append(f)
        i.release()

    def addPlayed(self, file):
        self.played.append(file)

    def getFile(self, recursion=0):
        if self.order is orders["random"]:
            filepath = self.files[random.randint(0, len(self.files)-1)]
            if (filepath in self.played):
                #if every file has been played, reset played and return a random file
                if (recursion > 50):
                    self.played=[]
                    return self.getFile()
                return self.getFile(recursion=recursion+1)
            return filepath
        elif (self.order is orders["sequential"]):
            if len(self.played) is len(self.files):
                self.played = []
            return self.files[len(self.played)]
        return None

class tvfile:
    def __init__(self):
        self.path = ""
        self.minduration = 0
        self.maxduration = 0

    def __str__(self):
        return self.path

def parseBlocks(file):
    DOMTree = xml.dom.minidom.parse(file)
    collection = DOMTree.documentElement
    xmlblocks = collection.getElementsByTagName("block")
    blocks = []

    for xmlblock in xmlblocks:
        #create block, set name and priority
        b = block()
        if xmlblock.hasAttribute("name"):
            b.name = xmlblock.getAttribute("name")
        if xmlblock.hasAttribute("priority"):
            b.priority = int(xmlblock.getAttribute("priority"))

        #set default start and end times, then get value if it exists
        start, end = "U0000","S2359"
        if xmlblock.hasAttribute("starttime"):
            start = xmlblock.getAttribute("starttime")
        if xmlblock.hasAttribute("endtime"):
            end = xmlblock.getAttribute("endtime")

        #create timedeltas from beginning of week for block start and end times
        startday = dayMap[start[0]]
        starttime = int(start[1:])
        endday = dayMap[end[0]]
        endtime = int(end[1:])
        b.start = datetime.timedelta(days=startday, hours=starttime/100, minutes=starttime%100)
        b.end = datetime.timedelta(days=endday, hours=endtime/100, minutes=endtime%100)

        #load contents
        xmlcontents = xmlblock.getElementsByTagName("content")
        contents = []
        for xmlc in xmlcontents:
            order = (xmlc.getAttribute("order") if xmlc.hasAttribute("order") else "random")
            #parse files into an array
            xmlfiles = xmlc.getElementsByTagName("file")
            files = []
            for xf in xmlfiles:
                f = tvfile()
                f.path = xf.getAttribute("path")
                if xf.hasAttribute("minduration"):
                    f.minduration = int(xf.getAttribute("minduration"))
                if xf.hasAttribute("maxduration"):
                    f.maxduration = int(xf.getAttribute("maxduration"))
                files.append(f)
            #add a new content to the contents array with order and files
            contents.append(content(order, files))
        b.contents = contents
        blocks.append(b)

    return blocks

"""
Returns the block with the highest priority and that is currently within
it's time window in the given array of blocks. On tie, defaults to the
block that came first.
"""
def getActiveBlock(blocks):
    currentday = (datetime.date.weekday(datetime.datetime.today()) + 1) % 7
    #gets current time in seconds, to compare with start and end times
    currenttime = datetime.datetime.today().hour * 3600 + datetime.datetime.today().minute * 60
    activeblock = None
    for block in blocks:
        if block.start.days < currentday < block.end.days or (currentday is block.start.days and currenttime >= block.start.seconds) or (currentday is block.end.days and currenttime <= block.end.seconds):
            if activeblock is None or activeblock.priority < block.priority:
                activeblock = block
    return activeblock