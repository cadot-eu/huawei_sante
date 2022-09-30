# ouvrir image
import numpy as np
import xml.dom.minidom
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from PIL import Image
basemin = int(input('min bpm [74]? :') or "74")
basemax = int(input('max bpm ? [160]? :') or "160")
calories = int(input('calories ? [1]? :') or "1")
maintenant = datetime.now().strftime("%Y-%m-%d")
debutd = datetime.now().strftime("%H:%M:%S.000")
date = input(
    'date de la course ['+maintenant+']? ') or maintenant
debut = debutd
duree = (input('durée de la course en heure:mn [1:00]? :') or '1:00')+':00'
dateI = datetime.strptime(date, "%Y-%m-%d").date()
dureeI = datetime.strptime(duree, "%H:%M:%S").time()
id = date+'T'+debut+'Z'
im = Image.open('image.png')
# coupe image
graf = im.crop((110, 326, 2234, 866))
# graf.save('crop.png')
# boucle sur la largeur de l'image
result = []
for x in range(graf.size[0]):
    trouve = 0
    # boucle sur la hauteur de l'image
    for y in range(graf.size[1]):
        # récupère la couleur du pixel
        cpixel = graf.load()[x, y]
        # compare color of pixel
        if cpixel == (232, 70, 92):
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

xdom = xml.dom.minidom.parse("base.tcx")
xdoc = xdom.documentElement
xdoc.getElementsByTagName('Activities')[0].getElementsByTagName(
    'Activity')[0].getElementsByTagName('Id')[0].data = id

lap = xdoc.getElementsByTagName('Activities')[0].getElementsByTagName(
    'Activity')[0].getElementsByTagName('Lap')[0]
lap.setAttribute('StartTime', id)
totalseconds = int(dureeI.hour*3600+dureeI.minute*60+dureeI.second)
lap.getElementsByTagName('TotalTimeSeconds')[
    0].firstChild.data = totalseconds
# int(    str(len(result))[:1])  # premier chiffre du nombre de résultat
lap.getElementsByTagName('DistanceMeters')[
    0].firstChild.data = str(len(result))
lap.getElementsByTagName('Calories')[0].firstChild.data = calories

track = lap.appendChild(xdom.createElement('Track'))
i = 0
for r in result:
    # print(corr[int(i)])
    tp = xdom.createElement("Trackpoint")
    subnode = xdom.createElement("Time")
    subnode.appendChild(xdom.createTextNode(
        datetime.strftime(datetime.strptime(maintenant+' '+debutd, "%Y-%m-%d %H:%M:%S.000") +
                          timedelta(seconds=i), "%Y-%m-%dT%H:%M:%S.000Z")))
    tp.appendChild(subnode)
    subnode = xdom.createElement("Position")
    subnode2 = xdom.createElement("LatitudeDegrees")
    subnode2.appendChild(xdom.createTextNode("50.33550049706327"))
    subnode.appendChild(subnode2)
    subnode2 = xdom.createElement("LongitudeDegrees")
    subnode2.appendChild(xdom.createTextNode(
        str(i/1000000000000000+4.997818608037509)))
    subnode.appendChild(subnode2)
    tp.appendChild(subnode)
    # subnode = xdom.createElement("AltitudeMeters")
    # subnode.appendChild(xdom.createTextNode("0"))
    # tp.appendChild(subnode)
    subnode = xdom.createElement("HeartRateBpm")
    subnode2 = xdom.createElement("Value")
    subnode2.appendChild(xdom.createTextNode(str(corr[int(i)])))
    subnode.appendChild(subnode2)
    tp.appendChild(subnode)

    track.appendChild(tp)
    i = i+1
lap.appendChild(track)
open("nouveau.tcx", "w").write(xdom.toxml())

#  <Trackpoint>
#                 <Time>2022-09-26T12:18:25.000Z</Time>
#                 <Position>
#                     <LatitudeDegrees>50.33550049706327</LatitudeDegrees>
#                     <LongitudeDegrees>4.997818608037509</LongitudeDegrees>
#                 </Position>
#                 <AltitudeMeters>248.4</AltitudeMeters>
#                 <HeartRateBpm>
#                     <Value>126</Value>
#                 </HeartRateBpm>
#             </Trackpoint>
