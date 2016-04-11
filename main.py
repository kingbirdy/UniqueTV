import block
import lib.vlc as vlc
import time
import os
import random

def playMedia(file):
    media = instance.media_new("file:///" + os.path.normpath(file))
    player.set_media(media)
    player.play()
    time.sleep(3)
    while player.is_playing():
        time.sleep(0.1)

#gets a random file from the given path
def getRandomFile(path):
    rand = random.randint(0, os.listdir(path).__len__() - 1)
    file = os.listdir(path)[rand]
    filepath = os.path.join(path, file)
    return filepath

blocks = block.parseBlocks("test/blocks.xml")

instance = vlc.Instance()
player = instance.media_player_new()

b = block.getActiveBlock(blocks)
while True:
    file = b.getFile()
    print "Playing %s " % file
    b.contents[0].addPlayed(file)
    time.sleep(4)
    #playMedia(file)