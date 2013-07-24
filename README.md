DenverNews.bundle
=================

Plex Media Center Plugin offering Denver news channels for live streaming.  2 of the channels (2 and 31) even loop their most recent news broadcast continuously when they are not broadcasting live.

All Denver channels are offered except for KCNC (CBS) Channel 4 since they do not offer live news video.  This includes:

* KWGN Channel 2 (WB2)
* KMGH Channel 7 (ABC)
* KUSA Channel 9 (NBC)
* KDVR Channel 31 (FOX)

This quite hoestly is my first Plex Plugin because I cut the cable and missed my local news.  This satisfies obtaining my news and makes getting local news pretty easy.  This by no means is a clean implementation of a Plex Plugin, but it works.  Pull requests are most certainly welcome.

The plugin uses the MP4/IOS M3U8 streams and hence works great on those devices as well as the Safari web browser.  Other web browsers do not appear to work very well at this time since they do not appear to support the HLS streaming (Google this issue on the Plex forums for more info).  It also works well with the Apple TV using PlexConnect, Plex desktop client, and XBMC.  Also, at this stage, the plugin reads the M3U8 and pulls the one with the highest bitrate.  It would be nice to have code that can dynamically select it based upon your bandwidth or other algorithm.

This plugin (after getting cleaned up) could potentially be the basis for a Local Live News plugin for many other cities.  AS I said, this can use a lot of work and being a Java developer, my Python skillz can use a lot of work. ;-)

Enjoy!
