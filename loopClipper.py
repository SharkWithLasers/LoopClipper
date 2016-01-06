import glob
import os
import shutil
import subprocess
import sys

EXTENSION = '.png'
PREFIX = 'tempImage-'
IMAGE_FILE_REGEX = PREFIX + '*' + EXTENSION
IMAGE_FILE_PATH = PREFIX + '%03d' + EXTENSION
FFMPEG_PATH = 'ffmpeg'

def loopClip(fileName, start, end, outputFileName):
    try:
        createForwardImageSequence(fileName, start, end)
        createReverseImageSequence()
        createClipsFromImages()
    finally:
        subprocess.call('rm %s' % IMAGE_FILE_REGEX, shell=True)

def createForwardImageSequence(fileName, start, end):
    subprocess.call([FFMPEG_PATH, 
        '-i', fileName,
        '-f', 'image2',
        '-q:v', '0',
        '-ss', start, '-to', end, 
        IMAGE_FILE_PATH])

def createReverseImageSequence():
    fileNames = glob.glob(IMAGE_FILE_REGEX)
    numFiles = len(fileNames)

    prefixLength= len(PREFIX)

    for fileName in fileNames:
        frameNumString = fileName[prefixLength:(prefixLength+3)]
        frameNum = int(frameNumString)
        if (frameNum == 1 or frameNum == numFiles):
            continue

        newFrameNum = numFiles - frameNum + numFiles
        newFrameNumString = str(newFrameNum).zfill(3)
        newFileName = PREFIX + newFrameNumString + EXTENSION

        shutil.copy(fileName, newFileName)


def createClipsFromImages():
    subprocess.call([FFMPEG_PATH,
        '-i', IMAGE_FILE_PATH,
        '-b:v', '1M', 
        '-c:v', 'libvpx', 
        '-an', 
        '-crf', '10',
        outputFileName])
        

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise ValueError('There should be 4 args passed into script (fileName start end outputFileName)')

    fileName = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    outputFileName = sys.argv[4]

    loopClip(fileName, start, end, outputFileName)
