import os
import re
import argparse
from datetime import datetime


def parseArgs():
    parser = argparse.ArgumentParser(description="Fix time stamps")
    parser.add_argument("--dir", "-d", type=str, help="Directory to look in",
                        default=os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument("--extension", "-e", type=str, help="File type extension",
                        default=".mp4")
    args = parser.parse_args()
    return args


def getFiles(fDir, ext):
    """Get all the files in a directory that match the extension."""
    fileList = [x for x in os.listdir(fDir) if x.endswith(ext)]
    return fileList


def changeTime(fileList, fDir, ext):
    """Change the time stamp for a file.

    This assumes that the file names have the form
    WORD_DATE_TIME_WORD.extension
    DATE: yyyymmdd
    TIME: hhmmss
    We ignore the words on both ends.
    """

    pattern = re.compile(r"\w+_(\d+)_(\d+)_?(\w*)\{}".format(ext))
    formatStr = "%Y%m%d %H%M%S"
    
    for f in fileList:
        match = pattern.search(f)
        cDate = match.group(1)
        cTime = match.group(2)
        
        newTime = datetime.strptime("{} {}".format(cDate, cTime), formatStr)
        # print(newTime)
        cmd = "touch -d \"{}\" {}".format(str(newTime), os.path.join(fDir, f))
        print(cmd)
        os.system(cmd)


def main():
    args = parseArgs()

    curExt = args.extension
    fileList = getFiles(args.dir, curExt)
    
    changeTime(fileList, args.dir, curExt)


if __name__ == '__main__':
    main()
