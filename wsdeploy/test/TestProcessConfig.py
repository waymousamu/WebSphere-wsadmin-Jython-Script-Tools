import os
import sys
import shutil
from org.apache.log4j import Logger
from java.lang.management import ManagementFactory
import unittest

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
print props

'''import the wsdeploy modules'''
from ProcessConfig import *
#from CommandGenerator import *
from ProcessCommands import *
from Install import *

'''exec the test data'''
execfile(testPath + os.sep + "TestCommon.py")

class TestProcessConfigND(unittest.TestCase):

    logger = Logger.getLogger("Test")

    def setUp(self):
        os.makedirs(props['tmpPath'])
        self.pc = ProcessConfig()
        self.envname = "MP66"
        self.itemDict = CONFDICT_ND
        self.xml =  CONFXML_ND

    def tearDown(self):
        self.pc = None
        self.envname = None
        self.itemDict = None
        self.xml = None
        shutil.rmtree(props['tmpPath'])

    def testXMLReadConfig(self):
        self.assertEqual(self.itemDict, self.pc.readConfig(xml=self.xml))

    def testXMLFileReadConfig(self):
        fh = open(props['tmpPath'] + os.sep + 'env.xml','w')
        fh.write(self.xml)
        fh.close()
        #fh = open(props['tmpPath'] + os.sep + 'env.xml','r')
        fhStr = props['tmpPath'] + os.sep + 'env.xml'
        self.assertEqual(self.itemDict, self.pc.readConfig(fh=fhStr))
        fh.close()

    def testXMLReadException(self):
        xml = None
        try:
            self.pc.readConfig(xml=xml),
        except Exception:
            pass
        else:
            fail("Expected an Exception")

class TestProcessConfigBASE(unittest.TestCase):

    logger = Logger.getLogger("Test")

    def setUp(self):
        os.makedirs(props['tmpPath'])
        self.pc = ProcessConfig()
        self.envname = "MP66"
        self.itemDict = CONFDICT_BASE
        self.xml =  CONFXML_BASE

    def tearDown(self):
        self.pc = None
        self.envname = None
        self.itemDict = None
        self.xml = None
        shutil.rmtree(props['tmpPath'])

#    def testXMLReadConfig(self):
#        self.assertEqual(self.itemDict, self.pc.readConfig(xml=self.xml))

    def testXMLFileReadConfig(self):
        #fh = open(props['tmpPath'] + os.sep + 'env.xml','w')
        #fh.write(self.xml)
        #fh.close()
        #fh = open(props['tmpPath'] + os.sep + 'env.xml','r')
        #fhStr = props['tmpPath'] + os.sep + 'env.xml'
        #self.assertEqual(self.itemDict, self.pc.readConfig(fh=fhStr))
        #fh.close()
        fhStr = props['confPath'] + os.sep + 'sample.xml'
        self.assertEqual(self.itemDict, self.pc.readConfig(fh=fhStr))
        #fh.close()

    def testXMLReadException(self):
        xml = None
        try:
            self.pc.readConfig(xml=xml),
        except Exception:
            pass
        else:
            fail("Expected an Exception")

if __name__ == '__main__' or __name__ == 'main':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessConfigBASE)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessConfigND)
    #unittest.TextTestRunner(verbosity=2).run(suite)