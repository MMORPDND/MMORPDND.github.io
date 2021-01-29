#########################################################
# File: generateOverlays.py
# Date: 1/26/21
# Description: This file will take image layers that overlap
#              and create the corresponding html/css files
#              to make a selectable image.
#########################################################

import os
from os import listdir, path
from os.path import isfile, join
import datetime

# Define some initial file names.
imageFormat = '.jpg'
backgroundImageName = 'background' + imageFormat
htmlFileName = 'index.html'
htmlTemplateFileName = 'htmlTemplate.html'
cssFileName = 'css/overlay.css'
logFileName = 'overlayGenerator.log'
runPath = os.path.dirname(os.path.realpath(__file__))
hoverTag = '-s'
htmlPythonBegin = '<!-- PYTHON BEGIN -->'
htmlPythonEnd = '<!-- PYTHON END -->'

# Opens files to be used during program lifetime.
logFile = open(logFileName, "a")
cssFile = open(cssFileName, "w+")


def log(info, newline=True):
    """
    Writes something to the log file.
    :param newline: Determines if a newline character should be printed after the log line.
    :param info: The str to write to the file.
    :return: None
    """
    timeStamp = datetime.datetime.now()
    logFile.write(str(timeStamp))
    logFile.write(':   ')
    logFile.write(info)
    if newline:
        logFile.write('\n')


def htmlFileOK():
    """
    Checks the html file to see if it already contains the needed python tags.
    :return: true if both python tags are found.
    """
    indexFile = open(htmlFileName, 'r')
    indexList = indexFile.readlines()
    indexFile.close()
    foundBegin = False
    foundEnd = False
    for line in indexList:
        if htmlPythonBegin in line:
            foundBegin = True
        if htmlPythonEnd in line:
            foundEnd = True

    count1 = len(open(htmlFileName).readlines())
    count2 = len(open(htmlTemplateFileName).readlines())
    if foundBegin and foundEnd:
        if count1 == count2:
            return True
    else:
        return False


def createHTMLFromTemplate():
    """
    Creates the html file from the template file if the template file is found..
    :return: None
    """
    # Open the html template and read in the lines.
    if path.exists(htmlTemplateFileName):
        log('html template file found: ' + htmlTemplateFileName)
    else:
        log('html template file not found: ' + htmlTemplateFileName)
        return
    htmlTemplateFile = open(htmlTemplateFileName, 'r')
    filelines = htmlTemplateFile.readlines()
    htmlTemplateFile.close()

    file = open(htmlFileName, "w")
    for fileline in filelines:
        log('Writing line to ' + htmlFileName + ': ' + fileline, False)
        file.write(fileline)
    file.close()


def setup():
    """
    Sets up the program by checking if the css and html files exist.
    If the files do not exist it will create them.
    :return:
    """
    # Check if needed css file exist.
    if path.exists(cssFileName):
        log('File found: ' + cssFileName)
    elif not path.exists(cssFileName):
        log('File not found: ' + cssFileName)
        log('Creating file: ' + cssFileName)
        os.mkdir('css')
        file = open(cssFileName, "w+")
        file.close()

    # Check if needed html file exist.
    if path.exists(htmlFileName) and htmlFileOK():
        log('File found: ' + htmlFileName)
    elif not path.exists(htmlFileName):
        log('File not found or not OK: ' + htmlFileName)
        os.remove(htmlFileName)
        log('Creating file: ' + htmlFileName)
        file = open(htmlFileName, "w+")
        file.close()
        createHTMLFromTemplate()
    elif not htmlFileOK():
        log('File not OK: ' + htmlFileName)
        log('writing file: ' + htmlFileName)
        createHTMLFromTemplate()


def writeCSS(info):
    """
    writes some data to the css file
    :param info: The str to write to the file.
    :return: None
    """
    log('Writing the following to css file:')
    log(info)
    cssFile.write(info)


def writeHTML(info):
    """
    writes some data to the html file
    :param info: The str to write to the file.
    :return: None
    """
    htmlFileTemp = open(htmlFileName, 'r')
    fileLines = htmlFileTemp.readlines()
    htmlFileTemp.close()
    log('Writing the following to html file:')
    log(info)
    htmlFile = open(htmlFileName, "w")

    p1 = True
    p2 = p3 = p4 = False
    # This will go through each line of the file.
    # p1 represents the section before the begin marker.
    # p2 represents the section where the info is placed.
    # p3 represents the text after the info until the end footer marker.
    # p4 represents the rest of the file.
    # CAUTION: The order of these if statements is important!
    for fileline in fileLines:
        if p1:
            htmlFile.write(fileline)
        if p3:
            if htmlPythonEnd in fileline:
                p3 = False
                p4 = True
            else:
                htmlFile.write(fileline)
        if p2:
            htmlFile.write(info)
            htmlFile.write(fileline)
            p2 = False
            p3 = True
        if p4:
            htmlFile.write(fileline)
        if htmlPythonBegin in fileline:
            p1 = False
            p2 = True

    htmlFile.close()


setup()
filenames = [file for file in listdir(runPath) if isfile(join(runPath, file))]

# Sets up some needed CSS.
parentCSSText = '.parent {\n\tposition: relative;\n\ttop: 0;\n\tleft: 0;\n}\n'
backgroundCSSText = '.background {\n\tz-index: 1;\n\tposition: relative;\n\ttop: 0;\n\tleft: 0;\n}\n'
overlayCSSText = 'img.overlay {\n\tz-index: 2;\n\tposition: absolute;\n\ttop: 0;\n\tleft: 0;\n}\n'
glowCSSText = 'img.glow {\n\tz-index: 3;\n\tposition: absolute;\n\ttop: 0;\n\tleft: 0;\n\topacity: 0;\n}\n'
hoverCSSText = 'img.overlay:hover ~ img.glow {\n\topacity:1;\n}\n'
additionalCSSStyle = '.fit {\n\tmax-width: 100%;\n\tmax-height: 100%;\n\tmargin: auto;\n}\n'

# Writes the css styles to the css file.
writeCSS(parentCSSText)
writeCSS(backgroundCSSText)
writeCSS(overlayCSSText)
writeCSS(glowCSSText)
writeCSS(hoverCSSText)
writeCSS(additionalCSSStyle)

for file in filenames:
    if 'png' in file and not backgroundImageName in file:
        if hoverTag not in file:
            log('Image (' + imageFormat + ') found: ' + file)
            fileName = file.replace(imageFormat, '')
            overlayHTMLText = '\t\t<img class=\"overlay fit\" src=\"' + fileName + imageFormat + '\" />\n'
            writeHTML(overlayHTMLText)
        else:
            log('Image (' + imageFormat + ') found: ' + file)
            fileName = file.replace(imageFormat, '')
            glowHTMLText = '\t\t<img class=\"glow fit\" src=\"' + fileName + imageFormat + '\" />\n'
            writeHTML(glowHTMLText)

# We want the background image to be at the top of the list so we put this separate.
for file in filenames:
    if backgroundImageName in file:
        log('Background image found: ' + file)
        backgroundHTMLText = '\t\t<img class=\"background fit\" src=\"' + backgroundImageName + '\" />\n'
        writeHTML(backgroundHTMLText)

# Close down files.
log('Program terminating.\n')
cssFile.close()
logFile.close()
