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
#print props

'''import the wsdeploy modules'''
from ProcessConfig import *
from ProcessCommands import *
from Install import *

'''exec the test data'''
execfile(testPath + os.sep + "TestCommon.py")

class TestProcessCommandsBASE(unittest.TestCase):

    logger = Logger.getLogger("Test")

    def setUp(self):
        self.cg = ProcessCommands()
        self.itemDict = CONFDICT_BASE
        self.srv = AdminConfig.getid('/Server:srv01/')
        self.pe = AdminConfig.list('ProcessExecution', self.srv)
        AdminConfig.modify(self.pe, [['runAsUser', 'websphere']])
        AdminConfig.modify(self.pe, [['runAsGroup', 'websphere']])

    def tearDown(self):
        self.cg = None
        self.cmdList = None
        self.itemDict = None
        self.srv=None
        self.pe=None
        self.datasource = AdminConfig.getid('/DataSource:Q5DataSource/')
        if self.datasource != "":
            AdminConfig.remove(self.datasource)
        self.jdbcprov = AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')
        if self.jdbcprov != "":
            AdminConfig.remove(self.jdbcprov)
        self.jassauthList = AdminConfig.list('JAASAuthData').split('\r\n')
        for item in self.jassauthList:
            if item != '':
                if AdminConfig.showAttribute(item, 'alias') == 'local_oracle_alias':
                    AdminConfig.remove(item)

    def testNoCommandsException(self):
        self.logger.debug("TestCommandGeneratorBASE:testNoCommandsException")
        cmdDict = None
        try:
            self.cg.generateCommands(cmdDict)
        except Exception:
            pass
        else:
            fail("Expected an Exception")

    def testBogusKeyException(self):
        self.logger.debug("TestCommandGeneratorBASE:testBogusKeyException")
        cmdDict = {'boguskey': 'bogusvalue'}
        try:
            self.cg.generateCommands(cmdDict)
        except Exception:
            pass
        else:
            fail("Expected an Exception")

    def testCellCheck(self):
        self.logger.debug("TestCommandGeneratorBASE:testCellCheck")
        try:
            self.cg.generateCommands(cmdList=[{'Cell': {'name': 'HP8200SWaymouthNode01Cell'}}])
        except Exception:
            pass
        else:
            fail("Expected an Exception")

    def testBogusScope(self):
        self.logger.debug("TestCommandGeneratorBASE:testBogusScope")
        try:
            self.cg.generateCommands(cmdList=[{'ProcessExecution': {'runAsUser': 'wasadmin', 'runAsGroup': 'wasadmin', 'scope': '/Server:BogusServer1/'}}])
        except Exception:
            pass
        else:
            fail("Expected an Exception")

    def testProcessConfigItemCreate(self):
        self.logger.debug("TestCommandGeneratorBASE:testProcessConfigItemCreate")
        self.cg.generateCommands(cmdList=[{'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}], action='W')
        self.jdbcprov = AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')
        self.implementationClassName=AdminConfig.showAttribute(self.jdbcprov, 'implementationClassName')
        self.assertEqual(self.implementationClassName, 'oracle.jdbc.xa.client.OracleXADataSource')

    def testProcessConfigItemModify(self):
        self.logger.debug("TestCommandGeneratorBASE:testProcessConfigItemModify")
        self.cg.generateCommands(cmdList=[{'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}], action='W')
        self.cg.generateCommands(cmdList=[{'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'false', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}], action='W')
        self.jdbcprov = AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')
        self.implementationClassName=AdminConfig.showAttribute(self.jdbcprov, 'xa')
        self.assertEqual(self.implementationClassName, 'false')

    def testProcessConfigItemRead(self):
        self.logger.debug("TestCommandGeneratorBASE:testProcessConfigItemRead")
        pass

    def testProcessNestedAttributeModify(self):
        self.logger.debug("TestCommandGeneratorBASE:testProcessNestedAttributeModify")
        self.cg.generateCommands(cmdList=[{'ProcessExecution': {'runAsUser': 'wasadmin', 'runAsGroup': 'wasadmin', 'scope': '/Server:srv01/'}}], action='W')
        self.srv = AdminConfig.getid('/Server:srv01/')
        self.pe = AdminConfig.list('ProcessExecution', self.srv)
        self.runAsUser=AdminConfig.showAttribute(self.pe, 'runAsUser')
        self.runAsGroup=AdminConfig.showAttribute(self.pe, 'runAsGroup')
        self.assertEqual(self.runAsUser, 'wasadmin')
        self.assertEqual(self.runAsGroup, 'wasadmin')

    def testProcessNestedAttributeRead(self):
        self.logger.debug("TestCommandGeneratorBASE:testProcessNestedAttributeRead")
        self.cg.generateCommands(cmdList=[{'JavaVirtualMachine': {'scope': '/Server:srv01/', 'genericJvmArguments': '-Dlog4j.root=WAS_HOME', 'maximumHeapSize': '512', 'initialHeapSize': '256'}}], action='R')
        self.srv = AdminConfig.getid('/Server:srv01/')
        self.jvm = AdminConfig.list('JavaVirtualMachine', self.srv)
        self.maximumHeapSize=AdminConfig.showAttribute(self.jvm, 'maximumHeapSize')
        self.initialHeapSize=AdminConfig.showAttribute(self.jvm, 'initialHeapSize')
        self.assertEqual(self.maximumHeapSize, '0')
        self.assertEqual(self.initialHeapSize, '0')

    def testProcessPropertySetModify(self):
        self.logger.debug("TestCommandGeneratorBASE:testProcessPropertySetModify")
        self.cg.generateCommands(cmdList=[{'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}], action='W')
        self.cg.generateCommands(cmdList=[{'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'authDataAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XAEVPSJDBCProvider/'}}], action='W')
        self.cg.generateCommands(cmdList=[{'J2EEResourceProperty': {'name': 'useRRASetEquals', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.String', 'value': 'true', 'required': 'false'}}, {'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true'}}], action='W')
        self.datasource = AdminConfig.getid('/DataSource:Q5DataSource/')
        self.j2eerespropList = AdminConfig.list('J2EEResourceProperty', self.datasource).split('\r\n')
        for item in self.j2eerespropList:
            if AdminConfig.showAttribute(item, 'name') == 'useRRASetEquals':
                self.assertEqual(AdminConfig.showAttribute(item, 'value'), 'true')
            if AdminConfig.showAttribute(item, 'name') == 'transactionBranchesLooselyCoupled':
                self.assertEqual(AdminConfig.showAttribute(item, 'value'), 'true')

    def testProcessPropertySetRead(self):
        self.logger.debug("TestCommandGeneratorBASE:testProcessPropertySetRead")
        self.cg.generateCommands(cmdList=[{'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}], action='W')
        self.cg.generateCommands(cmdList=[{'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'authDataAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XAEVPSJDBCProvider/'}}], action='W')
        self.cg.generateCommands(cmdList=[{'ConnectionPool': {'maxConnections': '1000', 'scope': '/DataSource:Q5DataSource/', 'testConnectionInterval': '3', 'minConnections': '5', 'testConnection': 'true'}}])
        self.datasource = AdminConfig.getid('/DataSource:Q5DataSource/')
        self.connectionpool = AdminConfig.list('ConnectionPool', self.datasource)
        self.maxConnections=AdminConfig.showAttribute(self.connectionpool, 'maxConnections')
        self.minConnections=AdminConfig.showAttribute(self.connectionpool, 'minConnections')
        self.testConnectionInterval=AdminConfig.showAttribute(self.connectionpool, 'testConnectionInterval')
        self.testConnection=AdminConfig.showAttribute(self.connectionpool, 'testConnection')
        self.assertEqual(self.maxConnections, '10')
        self.assertEqual(self.minConnections, '1')
        self.assertEqual(self.testConnectionInterval, '0')
        self.assertEqual(self.testConnection, 'false')

    def testJAASAuthCreate(self):
        self.logger.debug("TestCommandGeneratorBASE:testJAASAuthCreate")
        self.cg.generateCommands(cmdList=[{'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'swaymouth', 'password': 'secret', 'scope': '/Security:/'}}], action='W')
        self.jassauthList = AdminConfig.list('JAASAuthData').split('\r\n')
        for item in self.jassauthList:
            if AdminConfig.showAttribute(item, 'alias') == 'local_oracle_alias':
                self.assertEqual(AdminConfig.showAttribute(item, 'userId'), 'swaymouth')

    def testJAASAuthModify(self):
        self.logger.debug("TestCommandGeneratorBASE:testJAASAuthModify")
        self.cg.generateCommands(cmdList=[{'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'swaymouth', 'password': 'secret', 'scope': '/Security:/'}}], action='W')
        self.cg.generateCommands(cmdList=[{'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'testuser', 'password': 'secret', 'scope': '/Security:/'}}], action='W')
        self.jassauthList = AdminConfig.list('JAASAuthData').split('\r\n')
        for item in self.jassauthList:
            if AdminConfig.showAttribute(item, 'alias') == 'local_oracle_alias':
                self.assertEqual(AdminConfig.showAttribute(item, 'userId'), 'testuser')

    def testJAASAuthRead(self):
        self.logger.debug("TestCommandGeneratorBASE:testJAASAuthRead")
        self.cg.generateCommands(cmdList=[{'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'swaymouth', 'password': 'secret', 'scope': '/Security:/'}}], action='W')
        self.cg.generateCommands(cmdList=[{'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'testuser', 'password': 'secret', 'scope': '/Security:/'}}])
        self.jassauthList = AdminConfig.list('JAASAuthData').split('\r\n')
        for item in self.jassauthList:
            if AdminConfig.showAttribute(item, 'alias') == 'local_oracle_alias':
                self.assertEqual(AdminConfig.showAttribute(item, 'userId'), 'swaymouth')

if __name__ == '__main__' or __name__ == 'main':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessCommandsBASE)
    unittest.TextTestRunner(verbosity=2).run(suite)
