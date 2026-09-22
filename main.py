import asyncio
import sys
from shutil import make_archive

from downloadInterface import DownloadManager

if __name__ == '__main__':
    args = sys.argv

    gameVersion = args[2]
    loader = args[3]

    try:
        onlyServer = int(args[4])

    except:
        onlyServer = True

    try:
        usingConnector = int(args[5])

    except:
        usingConnector = False


    dm = DownloadManager(gameVersion=gameVersion, loader=loader, onlyServer=onlyServer, usingConnector=usingConnector)

    asyncio.run(dm.parseFileAndDownload(file=args[1]))




