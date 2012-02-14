import os
import sys
from org.apache.log4j import Logger
from java.lang.management import ManagementFactory

sys.modules['AdminConfig'] = AdminConfig
sys.modules['AdminControl'] = AdminControl
sys.modules['AdminApp'] = AdminApp
sys.modules['AdminTask'] = AdminTask
sys.modules['Help'] = Help

'''set up the paths, create the tmp working directory and make a props dictionary'''
pidname=ManagementFactory.getRuntimeMXBean().getName()
pidlist=pidname.split('@')
pid=pidlist[0]
currentWorkingDirectory=os.getcwd()
#print currentWorkingDirectory
binPath=currentWorkingDirectory + os.sep + "bin"
confPath=currentWorkingDirectory + os.sep + "conf"
logPath=currentWorkingDirectory + os.sep + "log"
tmpPath=currentWorkingDirectory + os.sep + "tmp" + os.sep + pid
libPath=currentWorkingDirectory + os.sep + "lib"
jythonpath=libPath + os.sep + "jython" + os.sep + "Lib"
srcPath=currentWorkingDirectory + os.sep + "src"
testPath=currentWorkingDirectory + os.sep + "test"
sys.path.append(binPath)
sys.path.append(confPath)
sys.path.append(logPath)
sys.path.append(tmpPath)
sys.path.append(libPath)
sys.path.append(jythonpath)
sys.path.append(srcPath)
sys.path.append(testPath)
#print sys.path
props = {}
props['binPath'] = binPath
props['confPath'] = confPath
props['logPath'] = logPath
props['tmpPath'] = tmpPath
props['libPath'] = libPath
props['jythonpath'] = jythonpath
props['srcPath'] = srcPath
props['testPath'] = testPath
#print props
from optparse import OptionParser

'''import the wsdeploy modules'''
from ProcessConfig import *
from ProcessCommands import *
from Install import *

class WsDeploy:

    def __init__(self, env=None, action=None):
        self.env = env
        self.action = action
        print ("Running wsdeploy on environment %s in %s mode." % (self.env, self.action))
        self.xml = props['confPath'] + os.sep + env + ".xml"
        self.conf = ProcessConfig()
        self.com = ProcessCommands()
        self.com.generateCommands(self.conf.readConfig(fh=self.xml), self.action)

if __name__ == '__main__' or __name__ == 'main':
    env = None
    action = None
    if len(sys.argv) == 2:
        env = sys.argv[1]
    if len(sys.argv) == 3:
        env = sys.argv[1]
        action = sys.argv[2]
    else:
        action = 'R'
    if env == None:
        print "Please supply an environment argument for this script."
        sys.exit(1)
    else:
        wsd = WsDeploy(env=env, action=action)