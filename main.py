import asyncio
import sys
from downloadInterface import DownloadManager

if __name__ == '__main__':
    dm = DownloadManager()

    args = sys.argv

    asyncio.run(dm.parseFileAndDownload(file=args[1], gameVersion=args[2], loader=args[3], onlyServer=int(args[4]), usingConnector=int(args[5])))




