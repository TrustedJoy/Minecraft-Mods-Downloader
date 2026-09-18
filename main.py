import asyncio
import sys
from downloadInterface import DownloadManager

if __name__ == '__main__':
    dm = DownloadManager()

    args = sys.argv

    try:
        onlyServer = int(args[4])

    except:
        onlyServer = True

    try:
        usingConnector = int(args[5])

    except:
        usingConnector = False

    asyncio.run(dm.parseFileAndDownload(file=args[1], gameVersion=args[2], loader=args[3], onlyServer=onlyServer, usingConnector=usingConnector))




