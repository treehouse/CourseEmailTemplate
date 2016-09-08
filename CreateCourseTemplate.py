import os
import datetime
import numpy as np
import Image
from shutil import copyfile
from shutil import make_archive

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def saveImageIntoFolder(color, folder):
    ## Takes the black image, changes the color, and saves a new image
    im = Image.open('template/course-icon-black.png')
    data = np.array(im)

    r1, g1, b1 = 0, 0, 0 # Original value
    r2, g2, b2 = hex_to_rgb(color)

    red, green, blue = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:,:,:3][mask] = [r2, g2, b2]

    im = Image.fromarray(data)
    im.save(folder + '/course-icon.png')

def createNewHTMLFile(title, content, link, color, contentSize, folder):
    tTitle = '```Title```'
    tContent = '```Content```'
    tLink = '```Link```'
    tColor = '```Color```'
    tContentSize = '```CourseSize```'
    file = open("template/content-announcement.html")
    newLines = ""
    for line in file.readlines():
        line = line.replace(tTitle, title)
        line = line.replace(tContent, content)
        line = line.replace(tLink, link)
        line = line.replace(tColor, color)
        line = line.replace(tContentSize, contentSize)
        newLines += line

    file = open(folder + '/content-announcement.html', "w")
    file.write(newLines)

def copyOverEverythingElse(folder):
    for subdir, dirs, files in os.walk('./template'):
        for file in files:
            filepath = subdir + os.sep + file
            if not(filepath.endswith('course-icon-black.png') or filepath.endswith('content-announcement.html')):
                copyfile(filepath, './' + folder + '/' + file)

def callFns(title, content, link, contentSize, color):
    camelTitle = ''.join(x for x in title.title() if not x.isspace())
    folder = datetime.datetime.today().strftime('%Y%m%d') + '-' + camelTitle
    if not os.path.exists(folder):
        os.makedirs(folder)
    createNewHTMLFile(title, content, link, color, contentSize, folder)
    saveImageIntoFolder(color, folder)
    copyOverEverythingElse(folder)
    make_archive(folder, 'zip', folder)

callFns("Course Title",
        "*|IF:FNAME|*Hey *|FNAME|*, *|ELSE:|*Hi there, *|END:IF|*we've just added a new course to the Treehouse Library. "
             + "Course Description / Email Body",
        "Course Link",
        "Course Length (e.g. 4 Stages - 161 min)",
        '#4499aa') ## Topic Color