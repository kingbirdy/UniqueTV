import xml.dom.minidom
import datetime
import os
import random

dayMap = {'U':0,"M":1,"T":2,"W":3,"R":4,"F":5,"S":6}

DOMTree = xml.dom.minidom.parse("test/blocks.xml")
collection = DOMTree.documentElement
blocks = collection.getElementsByTagName("block")

class block:
    name = ""
    priority = ""
    contents = []
    start = datetime.timedelta()
    end = datetime.timedelta()
    def __init__(self, name, priority, contents, start, end):
        self.name=  name
        self.priority = priority
        self.contents = contents
        self.start = start
        self.end = end

    #returns a file path to be played, chosen from a random content
    def getFile(self):
        rand = random.randint(0, self.contents.__len__() - 1)
        return self.contents[rand].getFile()

class content:
    global orders
    orders = {"random":0, "r":0, "sequential":1, "s":1}
    order = 0
    paths = []
    files = []
    played = []
    def __init__(self, order, paths):
        self.order = orders[order]
        self.paths = paths
        for path in self.paths:
            self.buildFiles(path)

    def buildFiles(self, path):
        for root, dirs, files in os.walk(path):
            for file in files:
                self.files.append(os.path.join(root, file))

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

class file:
    path = ""
    def __init__(self, path, genre="", minduration="0", maxduration="0"):
        self.path = path

def parseBlocks(file):
    DOMTree = xml.dom.minidom.parse(file)
    collection = DOMTree.documentElement
    xmlblocks = collection.getElementsByTagName("block")
    blocks = []

    for xmlblock in xmlblocks:
        #block defaults
        name, priority, start, end = "Block",0,"U0000","S2359"
        #change defaults, if values exist
        if xmlblock.hasAttribute("name"):
            name = xmlblock.getAttribute("name")
        if xmlblock.hasAttribute("priority"):
            priority = xmlblock.getAttribute("priority")
        if xmlblock.hasAttribute("starttime"):
            start = xmlblock.getAttribute("starttime")
        if xmlblock.hasAttribute("endtime"):
            end = xmlblock.getAttribute("endtime")

        #create timedeltas from beginning of week for block start and end times
        startday = dayMap[start[0]]
        starttime = int(start[1:])
        endday = dayMap[end[0]]
        endtime = int(end[1:])
        start = datetime.timedelta(days=startday, hours=starttime/100, minutes=starttime%100)
        end = datetime.timedelta(days=endday, hours=endtime/100, minutes=endtime%100)

        xmlcontents = xmlblock.getElementsByTagName("content")
        contents = []
        for xmlc in xmlcontents:
            order = "random"
            if xmlc.hasAttribute("order"):
                order = xmlc.getAttribute("order")
            #parse files into an array
            xmlfiles = xmlc.getElementsByTagName("file")
            files = []
            for xf in xmlfiles:
                files.append(xf.getAttribute("path"))
            #add a new content to the contents array with previously parsed rules and files
            contents.append(content(order, files))
        blocks.append(block(name, priority, contents, start, end))

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
        if (block.start.days <= currentday <= block.end.days and (currenttime >= block.start.seconds if currentday == block.start.days else True) and ((currenttime <= block.end.seconds if currentday == block.end.days else True))):
            if currentday == block.end.days and currenttime > block.end.time:
                continue
            if activeblock is None or activeblock.priority < block.priority:
                activeblock = block
    return activeblock