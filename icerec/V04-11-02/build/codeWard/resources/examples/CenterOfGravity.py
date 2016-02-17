#!/usr/bin/env python
def main(options, inputFiles, n=None, outputLevel=2):
    from I3Tray import I3Tray
    from icecube import icetray, dataio, dataclasses, phys_services
    from icecube.codeWard.modules.CenterOfGravity import CenterOfGravity
    from icecube.codeWard.modules.MinimumCharge import MinimumCharge

    gcdfile = [options.gcdfile]
    outfile = options.output

    # Instantiate a tray
    tray = I3Tray()

    tray.AddModule( 'I3Reader', 'Reader', FilenameList = gcdfile + inputFiles)
    
    #AddModule works on P-frame standard, specify if you want differently
    tray.AddModule(lambda f:f['I3EventHeader'].sub_event_stream == 'InIceSplit',"select")
    
    #Module that throws away Q-frames that now don't have a P-frame
    tray.AddModule("I3OrphanQDropper", "QDropper")

    #Module that requires minimal total charge of 100PE
    #tray.AddModule(MinimumCharge, "mimimumcharge")
    
    
    tray.AddModule(CenterOfGravity,"PE")
    
    #Module that throws away Q-frames that now don't have a P-frame
    tray.AddModule("I3OrphanQDropper", "QDropper2")

    #tray.AddModule('Dump','Dumper')
    
    #tray.AddModule('Keep','keeper',
    #               Keys = ['Track','InIcePulses'])
    
    tray.AddModule( 'I3Writer', 'Writer', 
                    Filename = outfile,
                    #DropOrphanStreams = [ icetray.I3Frame.Physics ],
                    streams = [icetray.I3Frame.Geometry, icetray.I3Frame.Calibration ,icetray.I3Frame.DAQ, icetray.I3Frame.Physics],
    )
    

    if options.book:
        
        keys = ["Track"]

        from icecube.tableio import I3TableWriter
        from icecube.rootwriter import I3ROOTTableService
        assert "root" in options.book.lower(), "Idiot, write ROOT correctly"
        
        table_service = I3ROOTTableService(outfile.replace(".i3",'').replace('.bz2','')+'.'+options.book.lower())
            
        tray.AddModule(I3TableWriter, "table_writer",
                       TableService = table_service,
                       SubEventStream = ['InIceSplit'],
                       Keys = keys)
            

    # Execute the Tray
    if n is None:
        tray.Execute()
    else:
        tray.Execute(n)
    tray.Finish()


if __name__ == "__main__":
    import sys
    import os.path
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-i', '--inputfile', default='./Level2_IC86.2013_data_Run00122474_Subrun00000055.i3.bz2',
                      dest='inputfile', help='Manually specify the inputfile to be used.   For data, you should generate a GCD first')
    parser.add_option('-g', '--gcdfile', default='./Level2_IC86.2013_data_Run00122474_0601_0_14_GCD.i3.gz',
                      dest='gcdfile', help='Manually specify the GCD file to be used.   For data, you should generate a GCD first')
    parser.add_option("-o", "--output", action="store", type="string", dest = 'output', default="output.i3.bz2", help="Output file name", metavar="BASENAME")
    parser.add_option("-n", "--number", action="store", type="int", dest="n", default=None, help="Number of frames to process", metavar="N")
    parser.add_option("-b", "--book", type="string", dest = 'book', default=None,help = 'write ROOT or root if you want a ROOT output too')

    (options, args) = parser.parse_args()

    assert os.path.exists(options.gcdfile), " - GCD file %s not found!"%options.gcdfile
    #assert options.output," - Output file not specified!"
    assert options.inputfile," - Input file not specified!"

    inputFiles = [options.inputfile]

    if len(inputFiles) > 0:
        main(options, inputFiles, n=options.n)
