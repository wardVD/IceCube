from icecube import icetray, dataio, dataclasses
from I3Tray import *

tray = I3Tray()

gcdfile = "./GeoCalibDetectorStatus_2012.56063_V1_OctSnow.i3.gz"

tray.AddModule("I3Reader","reader",Filename=gcdfile)   #Use icetray-inspect

def MyModule(frame):
    i3geo = frame['I3Geometry']
    pos = i3geo.omgeo[icetray.OMKey(1,1,0)]
    xpos,ypos,zpos = pos.position.x, pos.position.y, pos.position.z
    frame['xPos'], frame['yPos'], frame['zPos'] = dataclasses.I3Double(xpos),dataclasses.I3Double(ypos),dataclasses.I3Double(zpos)

tray.AddModule(MyModule,"mijnModule", Streams=[icetray.I3Frame.Geometry])

tray.AddModule("Dump","dumper")

tray.AddModule("I3Writer","writer",Filename="./SamHeeftEenKleinePiemel.i3.gz")

tray.Execute()

tray.Finish()
