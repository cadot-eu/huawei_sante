import xml.dom.minidom

xdom = xml.dom.minidom.parse("ancien.tcx")
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


node = xdom.createElement("Calories")
node.appendChild(xdom.createTextNode('10'))
lap.insertBefore(node, lap.getElementsByTagName('Track')[0])


node = xdom.createElement("MaximumHeartRateBpm")
subnode = xdom.createElement("Value")
subnode.appendChild(xdom.createTextNode('10'))
node.appendChild(subnode)
lap.insertBefore(node, lap.getElementsByTagName('Track')[0])

node = xdom.createElement("Intensity")
node.appendChild(xdom.createTextNode('Active'))
lap.insertBefore(node, lap.getElementsByTagName('Track')[0])


node = xdom.createElement("TriggerMethod")
node.appendChild(xdom.createTextNode('Manual'))
lap.insertBefore(node, lap.getElementsByTagName('Track')[0])


tracks = lap.getElementsByTagName('Trackpoint')

for track in tracks:
    node = xdom.createElement("HeartRateBpm")
    subnode = xdom.createElement("Value")
    subnode.appendChild(xdom.createTextNode('100'))
    node.appendChild(subnode)
    track.appendChild(node)

open("nouveau.tcx", "w").write(xdom.toxml())
