from pathlib import Path
from asyncinotify import Inotify, Mask
import asyncio
import os

async def main():
    # Context manager to close the inotify handle after use
    with Inotify() as inotify:
        # Adding the watch can also be done outside of the context manager.
        # __enter__ doesn't actually do anything except return self.
        # This returns an asyncinotify.inotify.Watch instance
        #inotify.add_watch('/var/lib/jellyfin/transcodes', Mask.ACCESS | Mask.MODIFY | Mask.OPEN | Mask.CREATE | Mask.DELETE | Mask.ATTRIB | Mask.CLOSE | Mask.MOVE | Mask.ONLYDIR)
        inotify.add_watch('/var/lib/jellyfin/transcodes', Mask.CREATE | Mask.CLOSE)
	# Iterate events forever, yielding them one at a time
        async for event in inotify:
            # Events have a helpful __repr__.  They also have a reference to
            # their Watch instance.
            #print(event)
            if event.mask == Mask.CLOSE_NOWRITE:
                #print(event.path)
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
