# jellyfin-transcoding-cleanup

Create ramdisk for transcode directory
/etc/fstab
```
tmpfs	/var/lib/jellyfin/transcodes	tmpfs	defaults,noatime,size=2g 0 0
```

Install dependency 
```
pip install asyncinotify
```
crontab -e
```
@reboot /jelly-clean/.env/bin/python /jelly-clean/jelly-clean.py
```
