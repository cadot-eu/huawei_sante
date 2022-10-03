# ouvrir image
import numpy as np
import xml.dom.minidom
import xml.etree.ElementTree as ET
import os
import glob
from PIL import Image
# on prend le fichier image.png ou le dernier fichier image enregistré dans /sdcard/Pictures/Screenshots
if os.path.exists("image.png") == True:
    im = Image.open('image.png')
elif os.path.exists("/storage/emulated/0/Pictures/Screenshots") == True:
    list_of_files = glob.glob('/storage/emulated/0/Pictures/Screenshots/*.png')
    im = Image.open(max(list_of_files, key=os.path.getmtime))
else:
    print("pas d'image")
    quit()

basemin = int(input('min bpm [74]?: ') or "74")
basemax = int(input('max bpm [162]?: ') or "162")

# coupe image
graf = im.crop((110, 326, 2234, 866))
graf.save('crop.png')
# boucle sur la largeur de l'image
result = []
for x in range(graf.size[0]):
    trouve = 0
    # boucle sur la hauteur de l'image
    for y in range(graf.size[1]):
        # récupère la couleur du pixel
        cpixel = graf.load()[x, y]
        # compare color of pixel
        if cpixel == (232, 70, 93):
            valy = int(graf.size[1]-y)
            result.append(valy)
            trouve = 1
            break
    if trouve == 0:
        result.append(result[x-1])
# debug
min = min(result)
max = max(result)
# print('min:'+str(min))
# print('max:'+str(max))
# print(len(result))
# print(graf.size[0])
# -------------------- dessin des points sur le graphique -------------------- #
# i = 0
# for pt in result:
#     graf.putpixel((i, y-pt), (255, 255, 255))
#     i = i+1
# graf.show()
# graf.save('result.png')
# calcul facteur
resamp = max-min
# print('max:'+str(max))
# print('min:'+str(min))
vraiamp = basemax-basemin
facteur = resamp/vraiamp
# print('vraiamp:'+str(vraiamp))
# print('resamp:'+str(resamp))
# print('facteur:'+str(facteur))
corr = []
for pt in result:
    corr.append(int((pt-min)/facteur)+basemin)
print(glob.glob(
    '/storage/emulated/0/Download/Tracks/Export/*.tcx'))
print(xml.dom.minidom.parse(max(list_of_files, key=os.path.getmtime)))
if os.path.exists("course.tcx") == True:
    xdom = xml.dom.minidom.parse("course.tcx")
elif os.path.exists("/storage/emulated/0/Download/Tracks/Export") == True:
    list_of_files = glob.glob(
        '/storage/emulated/0/Download/Tracks/Export/*.tcx')
    xdom = xml.dom.minidom.parse(max(list_of_files, key=os.path.getmtime))
else:
    print("pas de tcx")
    quit()
xdom = xml.dom.minidom.parse("course.tcx")
xdoc = xdom.documentElement
xdoc.setAttribute("xmlns:ns5",
                  "http://www.garmin.com/xmlschemas/ActivityGoals/v1")
xdoc.setAttribute(
    "xmlns:ns3", "http://www.garmin.com/xmlschemas/ActivityExtension/v2")
xdoc.setAttribute(
    "xmlns:ns2", "http://www.garmin.com/xmlschemas/UserProfile/v2")
xdoc.setAttribute(
    "xmlns", "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")
xdoc.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
xdoc.setAttribute(
    "xmlns:ns4", "http://www.garmin.com/xmlschemas/ProfileExtension/v1")
xdoc.setAttribute("creator", "cadot.eu")
xdoc.getElementsByTagName('Activities')[0].getElementsByTagName(
    'Activity')[0].setAttribute('Sport', 'Running')
lap = xdoc.getElementsByTagName('Activities')[0].getElementsByTagName(
    'Activity')[0].getElementsByTagName('Lap')[0]
nodes = lap.getElementsByTagName("CumulativeClimb")
for node in nodes:
    node.parentNode.removeChild(node)
nodes = lap.getElementsByTagName("CumulativeDecrease")
for node in nodes:
    node.parentNode.removeChild(node)

tracks = lap.getElementsByTagName('Trackpoint')

i = 0
for track in tracks:
    # print(corr[int(i)])
    node = xdom.createElement("HeartRateBpm")
    subnode = xdom.createElement("Value")
    subnode.appendChild(xdom.createTextNode(str(corr[int(i)])))
    node.appendChild(subnode)
    track.appendChild(node)
    i = i+(len(result)/len(tracks))
open("nouveau.tcx", "w").write(xdom.toxml())
