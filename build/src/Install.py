import re
import sys
import os
from org.apache.log4j import *

class Install:

    logger = Logger.getLogger("Install")

    def isWebSphereInstalled(self, installHome=None):
        """isWebSphereInstalled(self, installHome):
        this function takes a single argument of a directory string.
        It returns True if the directory is found or False if it is not."""
        self.result = False
        self.logger.debug("isWebSphereInstalled: init self.result = %s " % self.result)
        if installHome == None:
            self.logger.error("isWebSphereInstalled: No installHome string was supplied to the function.")
            raise InstallException("No installHome string was supplied to the function.")
        self.installHome = installHome
        self.logger.debug("isWebSphereInstalled: init self.installHome = %s " % self.installHome)
        self.result = os.path.isdir(self.installHome)
        self.logger.debug("isWebSphereInstalled: OS path search result = %s " % self.result)
        self.command = self.installHome + "/bin/verifyinstallver.bat"
        self.logger.debug("isWebSphereInstalled: Command to run = %s " % self.command)
        self.commandResult = os.system(self.command)
        self.logger.debug("isWebSphereInstalled: Command run result = %s " % self.commandResult)
        if not self.commandResult:
            self.result = True
        self.logger.debug("isWebSphereInstalled: return = %s " % self.result)
        return self.result

    def installWebSphereBase(self, installHome=None, mediaHome=None):
        """installWebSphereBase(self, installHome=None, mediaHome=None):
        This function takes a single argument of a directory string.
        It returns true if the WebSphere installation was successful or False if it was not."""
        self.result = False
        self.logger.debug("installWebSphereBase: init self.result = %s " % self.result)
        if installHome == None:
            self.logger.error("installWebSphereBase: No installHome string was supplied to the function.")
            raise InstallException("No installHome string was supplied to the function.")
        if mediaHome == None:
            self.logger.error("installWebSphereBase: No mediaHome string was supplied to the function.")
            raise InstallException("No mediaHome string was supplied to the function.")
        self.installHome = installHome
        self.logger.debug("installWebSphereBase: init self.installHome = %s " % self.installHome)
        self.mediaHome = mediaHome
        self.logger.debug("installWebSphereBase: init self.mediaHome = %s " % self.mediaHome)
        self.options = ("-OPT feature=noFeature -OPT allowNonRootSilentInstall=true -OPT disableOSPrereqChecking=true -OPT disableNonBlockingPrereqChecking=true -OPT checkFilePermissions=true -OPT PROF_enableAdminSecurity=false -OPT silentInstallLicenseAcceptance=true -OPT installLocation=%s -OPT installType=installNew -OPT profileType=none -silent" % self.installHome)
        self.command = ('""%s/install.exe" %s"' % (self.mediaHome, self.options))
        self.logger.debug("installWebSphereBase: self.command = %s " % self.command)
        self.logger.info("installWebSphereBase: Installing WebSphere Binaries...")
        self.commandResult = os.system(self.command)
        self.logger.debug("installWebSphereBase: Command run result = %s " % self.commandResult)
        self.command = self.installHome + "/bin/verifyinstallver.bat"
        self.logger.debug("installWebSphereBase: self.command = %s " % self.command)
        self.logger.info("installWebSphereBase: Verifying Installation...")
        self.commandResult = os.system(self.command)
        self.logger.debug("installWebSphereBase: Command run result = %s " % self.commandResult)
        if not self.commandResult:
            self.result = True
        return self.result

class InstallException(Exception):
    """ General exception method for class. """
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return repr(self.val)
