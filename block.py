import xml.dom.minidom

DOMTree = xml.dom.minidom.parse("test/blocks.xml")
collection = DOMTree.documentElement
blocks = collection.getElementsByTagName("block")

class block:
    name = ""
    priority = 0
    contents = []
    def __init__(self, name, priority, contents):
        self.name=  name
        self.priority = priority
        self.contents = contents

class content:
    rules = []
    paths = []
    def __init__(self, rules, paths):
        self.rules = rules
        self.paths = paths

def parseBlocks(file):
    DOMTree = xml.dom.minidom.parse(file)
    collection = DOMTree.documentElement
    xmlblocks = collection.getElementsByTagName("block")
    blocks = []

    for xmlblock in xmlblocks:
        name, priority, = "",""
        if xmlblock.hasAttribute("name"):
            name = xmlblock.getAttribute("name")
        if xmlblock.hasAttribute("priority"):
            priority = xmlblock.getAttribute("priority")
        xmlcontents = xmlblock.getElementsByTagName("content")
        contents = []

        for xmlc in xmlcontents:
            #parse rules into an array
            xmlrules = xmlc.getElementsByTagName("rule")
            rules = []
            for xr in xmlrules:
                rules.append(xr.firstChild.data)
            #parse files into an array
            xmlfiles = xmlc.getElementsByTagName("file")
            files = []
            for xf in xmlfiles:
                files.append(xf.getAttribute("path"))
            #add a new content to the contents array with previously parsed rules and files
            contents.append(content(rules, files))
        blocks.append(block(name, priority, contents))

    return blocks