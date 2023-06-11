from pathlib import Path
from asyncinotify import Inotify, Mask
import asyncio
import os

cache_dir='/var/lib/jellyfin/transcodes'
stream_cursor = {}

async def scroll_control():
    while True:
        files = os.listdir(cache_dir)
        for file in files:
            if file[-4:] != 'm3u8':
                if stream_cursor[file[:32]] > int(file.split('.')[0][32:]):
                    print("Dangling file - " + file)
                    os.remove(os.path.join(cache_dir,file))
        await asyncio.sleep(15)

async def main():
    with Inotify() as inotify:
        asyncio.create_task(scroll_control())
        # Adding the watch can also be done outside of the context manager.
        # __enter__ doesn't actually do anything except return self.
        # This returns an asyncinotify.inotify.Watch instance
        #inotify.add_watch('/var/lib/jellyfin/transcodes', Mask.ACCESS | Mask.MODIFY | Mask.OPEN | Mask.CREATE | Mask.DELETE | Mask.ATTRIB | Mask.CLOSE | Mask.MOVE | Mask.ONLYDIR)
        inotify.add_watch(cache_dir, Mask.CREATE | Mask.CLOSE)
        # Iterate events forever, yielding them one at a time
        async for event in inotify:
            # Events have a helpful __repr__.  They also have a reference to
            # their Watch instance.
            #print(event)
            if event.mask == Mask.CLOSE_NOWRITE:
                #print(event.path)
                file_name = str(event.name)
                stream_cursor[file_name[:32]] = int(file_name[32:-3])
                #print(stream_cursor)
                os.remove(event.path)
            # the contained path may or may not be valid UTF-8.  See the note
            # below
            #print(repr(event.path))


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
except KeyboardInterrupt:
    print('shutting down')
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
