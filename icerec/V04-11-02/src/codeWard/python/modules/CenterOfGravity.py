from icecube import icetray,dataio,dataclasses
import math

############################################
# Find Center of Gravity for two cascades  #
###########################################
class CenterOfGravity(icetray.I3Module):
    def __init__(self, ctx):
        icetray.I3Module.__init__(self,ctx)
        self.OMDict = {}
        self.AddOutBox("OutBox")

    def Configure(self):
        pass

    def Geometry(self,frame):
        assert 'I3Geometry' in frame, "Input your GCD as well!"
       
    def Physics(self, frame):
        self.OMDict.clear()
        pulse = frame['SplitInIcePulses']
        pulse = pulse.apply(frame)

        for OMKey, pulseInfo in pulse:
            for eachPulse in pulseInfo:
                self.OMDict[eachPulse.time] = {'DOM': OMKey, 'charge':eachPulse.charge}

        #sum all charges of all DOMs at all times
        totalCharge =  sum(map(lambda x: x['charge'], self.OMDict.values()))
        #require minimum of 100 PE charge on all DOMs
        if totalCharge > 100:
            first25, middle50, last25 = 0., 0., 0.
            #loop over all charges chronologically
            for time in sorted(self.OMDict):

                pos = frame['I3Geometry'].omgeo[self.OMDict[time]['DOM']]
                xpos,ypos,zpos = pos.position.x, pos.position.y, pos.position.z

                self.OMDict[time]['weightedPosition'] = [self.OMDict[time]['charge']*xpos,self.OMDict[time]['charge']*ypos,self.OMDict[time]['charge']*zpos]
                self.OMDict[time]['weightedTime'] = self.OMDict[time]['charge']*time
                
                if first25 < totalCharge/4:
                    first25 += self.OMDict[time]['charge']
                    self.OMDict[time]['period'] = 'first25'
                elif first25+middle50 < totalCharge/2:
                    middle50 += self.OMDict[time]['charge']
                    self.OMDict[time]['period'] = 'middle50'
                else:
                    last25 += self.OMDict[time]['charge']
                    self.OMDict[time]['period'] = 'last25'
            
            XPosFirst25 = sum(x['weightedPosition'][0] if x['period'] == 'first25' else 0 for x in self.OMDict.values())/first25
            YPosFirst25 = sum(x['weightedPosition'][1] if x['period'] == 'first25' else 0 for x in self.OMDict.values())/first25
            ZPosFirst25 = sum(x['weightedPosition'][2] if x['period'] == 'first25' else 0 for x in self.OMDict.values())/first25
            XPosLast25 = sum(x['weightedPosition'][0] if x['period'] == 'last25' else 0 for x in self.OMDict.values())/last25
            YPosLast25 = sum(x['weightedPosition'][1] if x['period'] == 'last25' else 0 for x in self.OMDict.values())/last25
            ZPosLast25 = sum(x['weightedPosition'][2] if x['period'] == 'last25' else 0 for x in self.OMDict.values())/last25
            TimeFirst25 = sum(x['weightedTime'] if x['period'] == 'first25' else 0 for x in self.OMDict.values())/first25
            TimeLast25 = sum(x['weightedTime'] if x['period'] == 'last25' else 0 for x in self.OMDict.values())/last25

            FirstParticle, SecondParticle = dataclasses.I3Particle(), dataclasses.I3Particle()
            
            FirstParticle.pos.x,FirstParticle.pos.y,FirstParticle.pos.z = XPosFirst25,YPosFirst25,ZPosFirst25
            FirstParticle.time = TimeFirst25
            SecondParticle.pos.x,SecondParticle.pos.y,SecondParticle.pos.z = XPosLast25,YPosLast25,ZPosLast25
            SecondParticle.time = TimeLast25

            frame['FirstParticle'] = FirstParticle
            frame['SecondParticle'] = SecondParticle
            
            Track = dataclasses.I3Particle()

            Track.pos.x, Track.pos.y, Track.pos.z =  XPosFirst25,YPosFirst25,ZPosFirst25
            Track.time = TimeFirst25

            #Track.dir = dataclasses.I3Direction(XPosLast25-XPosFirst25, YPosLast25-YPosFirst25, ZPosLast25-ZPosFirst25)
            dx, dy, dz = XPosLast25-XPosFirst25, YPosLast25-YPosFirst25, ZPosLast25-ZPosFirst25

            if dy < 0:
                phi_angle = -0.5*math.pi + math.asin( dx / math.sqrt(dx**2 + dy**2) )
            else:
                phi_angle = 0.5*math.pi + math.asin( dx / math.sqrt(dx**2 + dy**2) )
            Seed_Length = math.sqrt( (dx*dx) + (dy*dy) + (dz*dz) )
            theta_angle = math.acos(dz/Seed_Length)

            Track.dir = dataclasses.I3Direction()
            Track.dir.set_theta_phi(theta_angle,phi_angle)


            frame['Track'] = Track

            self.PushFrame(frame,"OutBox")

            return 1

        else:
            return 0
    
