# IceCube Software

This installation installs the necessary dependencies for the standard "offline" software provide by IceCube

## SVN
Downlad subversion:

```sh
sudo apt-get install subversion
```

## ROOT
Download ROOT: https://root.cern.ch//

## I3_PORTS: Tool Build System (only for local computer):
Tools are external packages that are required dependencies for IceCube Offline software packages. These are distributed as source and built on your local cluster using the Ports system. This will help you setup your toolset (often referred to as I3_PORTS).

add “export I3_PORTS=WHEREYOUWANTTOSAVEI3” to **~/.bashrc**

i.e.:
```sh
export I3_PORTS=$HOME/IceCube/i3/ports/ #in ~/.bashrc
``` 
If you have a map called “IceCube” in your home folder. But you can put it anywhere you want.
>i3/ports shouldn’t exist before following this installation

add 

```sh
export SVN=http://code.icecube.wisc.edu/svn #in ~/.bashrc
``` 

## Dependencies

Choose sh file for your environment in http://code.icecube.wisc.edu/icetray-dist/distros/

```sh
wget http://code.icecube.wisc.edu/icetray-dist/distros/Ubuntu.sh
source Ubuntu.sh
```

## Finalizing

Go to right directory: 

```sh
cd ~/IceCube/
svn co http://code.icecube.wisc.edu/icetray-dist/tools/DarwinPorts/trunk port_source
cd port_source
./i3-install.sh $I3_PORTS

rsync -vrlpt code.icecube.wisc.edu::Offline/test-data $I3_PORTS/
```

Look for newest release in offline-software: http://code.icecube.wisc.edu/svn/meta-projects/offline-software/releases/

```sh
mkdir offline
cd offline
mkdir *NEWESTVERSION*
cd *NEWESTVERSION*
svn co $SVN/meta-projects/offline-software/releases/NEWESTVERSION src
mkdir build
cd build
```
```sh
cmake ../src #IN ICECUBE CLUSTER
$I3_PORTS/bin/cmake ../src #ON LOCAL COMPUTER
```
```sh
make
make rsync
```
**Every time you log in:** in build/ directory: 
```sh
./env-shell.sh
```
