import block
import lib.vlc as vlc
import time
import os

blocks = block.parseBlocks("test/blocks.xml")

path = os.path.abspath(blocks[0].contents[0].paths[0])
file = os.listdir(path)[0]
filepath = os.path.join(path, file)
print filepath

instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new("file:///" + os.path.normpath(filepath))
player.set_media(media)
player.play()

time.sleep(10)
while player.is_playing():
    time.sleep(10)