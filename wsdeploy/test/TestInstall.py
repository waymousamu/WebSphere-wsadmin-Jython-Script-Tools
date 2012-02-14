import os
import sys
import shutil
from org.apache.log4j import Logger
from java.lang.management import ManagementFactory
import unittest

#sys.modules['AdminConfig'] = AdminConfig
#sys.modules['AdminControl'] = AdminControl
#sys.modules['AdminApp'] = AdminApp
#sys.modules['AdminTask'] = AdminTask
#sys.modules['Help'] = Help

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

'''import the wsdeploy modules'''
from ProcessConfig import *
from CommandGenerator import *
from ProcessCommands import *
from Install import *

'''exec the test data'''
execfile("TestCommon.py")

class TestInstall(unittest.TestCase):
    logger = Logger.getLogger("Test")
    def setUp(self):
        self.ti = Install()
        self.installHome = "C:/ibm/websphere7_64"
        self.noInstallHome = "C:/ibm/websphere7_64_XX"
        self.mediaHome = "O:/Internal IT/Software – Public/IBM/was_nd_7/wintel64/disk1/WAS"

    def tearDown(self):
        if os.path.exists("%s/uninstall/uninstall.exe" % self.noInstallHome):
            self.logger.info("Cleaning up test WebSphere installation at: %s" % self.noInstallHome)
            os.system('%s/uninstall/uninstall -silent -OPT removeProfilesOnUninstall="true"' % self.noInstallHome)
            shutil.rmtree(self.noInstallHome)
        self.ti = None
        self.installHome = None
        self.noInstallHome = None
        self.mediaHome = None

    def testCheckExistingInstallDetected(self):
        '''testCheckExistingInstallDetected'''
        self.logger.info("TestInstall:testCheckExistingInstallDetected")
        self.isWebSphereInstalled = True
        self.assertEqual(self.isWebSphereInstalled, self.ti.isWebSphereInstalled(self.installHome))

    def testCheckNonExistingInstallDetected(self):
        '''testCheckNonExistingInstallDetected'''
        self.logger.info("TestInstall:testCheckNonExistingInstallDetected")
        self.isWebSphereInstalled = False
        self.assertEqual(self.isWebSphereInstalled, self.ti.isWebSphereInstalled(self.noInstallHome))

    def testNoInstallHomeException(self):
        '''testNoInstallHomeException'''
        self.logger.info("TestInstall:testNoInstallHomeException")
        try:
            self.ti.isWebSphereInstalled()
        except Exception:
            pass
        else:
            fail("Expected an Exception")

    def testNullInstallHomeDirException(self):
        '''testNullInstallHomeDirException'''
        self.logger.info("TestInstall:testNullInstallHomeDirException")
        try:
            self.ti.installWebSphereBase(mediaHome=self.mediaHome)
        except Exception:
            pass
        else:
            fail("Expected an Exception")

    def testNullMediaHomeDIR(self):
        '''testNullMediaHomeDIR'''
        self.logger.info("TestInstall:testNullMediaHomeDIR")
        try:
            self.ti.installWebSphereBase(installHome=self.installHome)
        except Exception:
            pass
        else:
            fail("Expected an Exception")

    def testInstallBase(self):
        '''testInstallBase'''
        self.logger.info("TestInstall:testInstallBase")
        self.isInstallSucess = True
        self.assertEquals(self.isInstallSucess, self.ti.installWebSphereBase(installHome=self.noInstallHome, mediaHome=self.mediaHome))
