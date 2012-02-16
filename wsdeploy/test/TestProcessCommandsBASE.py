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
        self.itemList = CONFDICT_BASE
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
        self.mqcf = AdminConfig.getid('/MQQueueConnectionFactory:QCF1/')
        if self.mqcf != "":
            AdminConfig.remove(self.mqcf)
        self.sib = AdminConfig.getid('/SIBus:DovetailSIBus/')
        if self.sib != "":
            AdminConfig.remove(self.sib)

    def testNoCommandsException(self):
        cmdList = None
        try:
            self.cg.generateCommands(cmdList)
        except ProcessCommandException:
            pass
        else:
            self.assertEquals(0,1, "This should have thrown an exception.")

    def testCellCheckException(self):
        try:
            self.cg.generateCommands(cmdList=[{'Cell': {'name': 'HP8200SWaymouthNode01Cell'}}])
        except ProcessCommandException:
            pass
        else:
            self.assertEquals(0,1, "This should have thrown an exception.")

    def testBogusScopeException(self):
        try:
            self.cg.validateScope(valueDict={'runAsUser': 'wasadmin', 'runAsGroup': 'wasadmin', 'scope': '/Server:BogusScope01/'}, method='testBogusScope')
        except ProcessCommandException:
            pass
        else:
            self.assertEquals(0,1, "This should have thrown an exception.")

    def testGenerateCommandsBadKeyException(self):
        try:
            self.cg.generateCommands(cmdList=[{'BogusKey': {'attr': 'value'}}])
        except ProcessCommandException:
            pass
        else:
            self.assertEquals(0,1, "This should have thrown an exception.")

    def testGenerateCommands(self):
        '''This verifies that the configuration list contains valid dictionaries'''
        try:
            self.cg.generateCommands(cmdList=self.itemList, action='W')
        except ProcessCommandException:
            self.assertEquals(0,1, "This should not have thrown an exception.")
        else:
            pass

    def testGenerateCommandsException(self):
        '''This verifies that an exception is created when the generateCommand method is run in read only mode and objects do not yet exist'''
        try:
            self.cg.generateCommands(cmdList=self.itemList)
        except ProcessCommandException:
            pass
        else:
            self.assertEquals(0,1, "This should not have thrown an exception.")


    def testProcessConfigItemCreate(self):
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}, action='W')
        self.jdbcprov = AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')
        self.implementationClassName=AdminConfig.showAttribute(self.jdbcprov, 'implementationClassName')
        self.assertEqual(self.implementationClassName, 'oracle.jdbc.xa.client.OracleXADataSource')

    def testProcessConfigItemModify(self):
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}, action='W')
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'false', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}, action='W')
        self.jdbcprov = AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')
        self.implementationClassName=AdminConfig.showAttribute(self.jdbcprov, 'xa')
        self.assertEqual(self.implementationClassName, 'false')

    def testProcessConfigItemRead(self):
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}, action='W')
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'false', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}})
        self.jdbcprov = AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')
        self.implementationClassName=AdminConfig.showAttribute(self.jdbcprov, 'xa')
        self.assertEqual(self.implementationClassName, 'true')
        pass

    def testProcessNestedAttributeModify(self):
        self.cg.processNestedAttribute(cmdDict={'ProcessExecution': {'runAsUser': 'wasadmin', 'runAsGroup': 'wasadmin', 'scope': '/Server:srv01/'}}, action='W')
        self.srv = AdminConfig.getid('/Server:srv01/')
        self.pe = AdminConfig.list('ProcessExecution', self.srv)
        self.runAsUser=AdminConfig.showAttribute(self.pe, 'runAsUser')
        self.runAsGroup=AdminConfig.showAttribute(self.pe, 'runAsGroup')
        self.assertEqual(self.runAsUser, 'wasadmin')
        self.assertEqual(self.runAsGroup, 'wasadmin')

    def testProcessNestedAttributeRead(self):
        self.cg.processNestedAttribute(cmdDict={'JavaVirtualMachine': {'scope': '/Server:srv01/', 'genericJvmArguments': '-Dlog4j.root=WAS_HOME', 'maximumHeapSize': '512', 'initialHeapSize': '256'}}, action='R')
        self.srv = AdminConfig.getid('/Server:srv01/')
        self.jvm = AdminConfig.list('JavaVirtualMachine', self.srv)
        self.maximumHeapSize=AdminConfig.showAttribute(self.jvm, 'maximumHeapSize')
        self.initialHeapSize=AdminConfig.showAttribute(self.jvm, 'initialHeapSize')
        self.assertEqual(self.maximumHeapSize, '0')
        self.assertEqual(self.initialHeapSize, '0')

    def testProcessPropertySetCreate(self):
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}, action='W')
        self.cg.processConfigItem(cmdDict={'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'authDataAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XAEVPSJDBCProvider/'}}, action='W')
        self.cg.processPropertySet(cmdDict={'J2EEResourceProperty': {'name': 'useRRASetEquals', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.String', 'value': 'true', 'required': 'false'}}, action='W')
        self.datasource = AdminConfig.getid('/DataSource:Q5DataSource/')
        self.j2eerespropList = AdminConfig.list('J2EEResourceProperty', self.datasource).split('\r\n')
        for item in self.j2eerespropList:
            if AdminConfig.showAttribute(item, 'name') == 'useRRASetEquals':
                self.assertEqual(AdminConfig.showAttribute(item, 'value'), 'true')

    def testProcessPropertySetModify(self):
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}, action='W')
        self.cg.processConfigItem(cmdDict={'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'authDataAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XAEVPSJDBCProvider/'}}, action='W')
        self.cg.processPropertySet(cmdDict={'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true'}}, action='W')
        self.datasource = AdminConfig.getid('/DataSource:Q5DataSource/')
        self.j2eerespropList = AdminConfig.list('J2EEResourceProperty', self.datasource).split('\r\n')
        for item in self.j2eerespropList:
            if AdminConfig.showAttribute(item, 'name') == 'transactionBranchesLooselyCoupled':
                self.assertEqual(AdminConfig.showAttribute(item, 'value'), 'true')

    def testProcessPropertySetRead(self):
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}}, action='W')
        self.cg.processConfigItem(cmdDict={'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'authDataAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XAEVPSJDBCProvider/'}}, action='W')
        self.cg.processPropertySet(cmdDict={'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true'}})
        self.datasource = AdminConfig.getid('/DataSource:Q5DataSource/')
        self.j2eerespropList = AdminConfig.list('J2EEResourceProperty', self.datasource).split('\r\n')
        for item in self.j2eerespropList:
            if AdminConfig.showAttribute(item, 'name') == 'transactionBranchesLooselyCoupled':
                self.assertEqual(AdminConfig.showAttribute(item, 'value'), 'false')

    def testProcessSecrurityCreate(self):
        self.cg.processSecurity(cmdDict={'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'swaymouth', 'password': 'secret', 'scope': '/Cell:cell01/'}}, action='W')
        self.jassauthList = AdminConfig.list('JAASAuthData').split('\r\n')
        for item in self.jassauthList:
            if AdminConfig.showAttribute(item, 'alias') == 'local_oracle_alias':
                self.assertEqual(AdminConfig.showAttribute(item, 'userId'), 'swaymouth')

    def testProcessSecrurityModify(self):
        self.cg.processSecurity(cmdDict={'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'swaymouth', 'password': 'secret', 'scope': '/Cell:cell01/'}}, action='W')
        self.cg.processSecurity(cmdDict={'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'testuser', 'password': 'secret', 'scope': '/Cell:cell01/'}}, action='W')
        self.jassauthList = AdminConfig.list('JAASAuthData').split('\r\n')
        for item in self.jassauthList:
            if AdminConfig.showAttribute(item, 'alias') == 'local_oracle_alias':
                self.assertEqual(AdminConfig.showAttribute(item, 'userId'), 'testuser')

    def testProcessSecrurityRead(self):
        self.cg.processSecurity(cmdDict={'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'swaymouth', 'password': 'secret', 'scope': '/Cell:cell01/'}}, action='W')
        self.cg.processSecurity(cmdDict={'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'testuser', 'password': 'secret', 'scope': '/Cell:cell01/'}})
        self.jassauthList = AdminConfig.list('JAASAuthData').split('\r\n')
        for item in self.jassauthList:
            if AdminConfig.showAttribute(item, 'alias') == 'local_oracle_alias':
                self.assertEqual(AdminConfig.showAttribute(item, 'userId'), 'swaymouth')

    def testMQQCFCreate(self):
        self.cg.processConfigItem(cmdDict={'MQQueueConnectionFactory': {'transportType': 'BINDINGS_THEN_CLIENT', 'port': '1415', 'name': 'QCF1', 'scope': '/Cell:cell01/', 'host': 'localhost', 'channel': 'CH1', 'queueManager': 'QMGR1', 'jndiName': 'jms/QCF1'}}, action='W')
        self.mqcf = AdminConfig.getid('/MQQueueConnectionFactory:QCF1/')
        self.jndiName=AdminConfig.showAttribute(self.mqcf, 'jndiName')
        self.assertEqual(self.jndiName, 'jms/QCF1')

    def testMQQCFModify(self):
        self.cg.processConfigItem(cmdDict={'MQQueueConnectionFactory': {'transportType': 'BINDINGS_THEN_CLIENT', 'port': '1415', 'name': 'QCF1', 'scope': '/Cell:cell01/', 'host': 'localhost', 'channel': 'CH1', 'queueManager': 'QMGR1', 'jndiName': 'jms/QCF1'}}, action='W')
        self.cg.processConfigItem(cmdDict={'MQQueueConnectionFactory': {'transportType': 'BINDINGS_THEN_CLIENT', 'port': '1415', 'name': 'QCF1', 'scope': '/Cell:cell01/', 'host': 'localhost', 'channel': 'CH1', 'queueManager': 'QMGR1', 'jndiName': 'jms/BogusName'}}, action='W')
        self.mqcf = AdminConfig.getid('/MQQueueConnectionFactory:QCF1/')
        self.jndiName=AdminConfig.showAttribute(self.mqcf, 'jndiName')
        self.assertEqual(self.jndiName, 'jms/BogusName')

    def testMQQCFRead(self):
        self.cg.processConfigItem(cmdDict={'MQQueueConnectionFactory': {'transportType': 'BINDINGS_THEN_CLIENT', 'port': '1415', 'name': 'QCF1', 'scope': '/Cell:cell01/', 'host': 'localhost', 'channel': 'CH1', 'queueManager': 'QMGR1', 'jndiName': 'jms/QCF1'}}, action='W')
        self.cg.processConfigItem(cmdDict={'MQQueueConnectionFactory': {'transportType': 'BINDINGS_THEN_CLIENT', 'port': '1415', 'name': 'QCF1', 'scope': '/Cell:cell01/', 'host': 'localhost', 'channel': 'CH1', 'queueManager': 'QMGR1', 'jndiName': 'jms/BogusName'}})
        self.mqcf = AdminConfig.getid('/MQQueueConnectionFactory:QCF1/')
        self.jndiName=AdminConfig.showAttribute(self.mqcf, 'jndiName')
        self.assertEqual(self.jndiName, 'jms/QCF1')

    def testMQQCreate(self):
        self.cg.processConfigItem(cmdDict={'MQQueue' : {'name' : 'AccountingHVMessageSendQueue', 'jndiName' : 'dovetail/jms/AccountingHVMessageSendQueue', 'persistence' : 'PERSISTENT', 'baseQueueName' : 'AccountingHVMessageSendQueue', 'baseQueueManagerName' : 'QMGR1', 'queueManagerHost' : 'localhost', 'queueManagerPort' : '1415', 'serverConnectionChannelName' : 'CH1', 'scope': '/Cell:cell01/'}}, action='W')
        self.mqq = AdminConfig.getid('/MQQueue:AccountingHVMessageSendQueue/')
        self.jndiName=AdminConfig.showAttribute(self.mqq, 'jndiName')
        self.assertEqual(self.jndiName, 'dovetail/jms/AccountingHVMessageSendQueue')

    def testMQQModify(self):
        self.cg.processConfigItem(cmdDict={'MQQueue' : {'name' : 'AccountingHVMessageSendQueue', 'jndiName' : 'dovetail/jms/AccountingHVMessageSendQueue', 'persistence' : 'PERSISTENT', 'baseQueueName' : 'AccountingHVMessageSendQueue', 'baseQueueManagerName' : 'QMGR1', 'queueManagerHost' : 'localhost', 'queueManagerPort' : '1415', 'serverConnectionChannelName' : 'CH1', 'scope': '/Cell:cell01/'}}, action='W')
        self.cg.processConfigItem(cmdDict={'MQQueue' : {'name' : 'AccountingHVMessageSendQueue', 'jndiName' : 'jms/Bogus', 'persistence' : 'PERSISTENT', 'baseQueueName' : 'AccountingHVMessageSendQueue', 'baseQueueManagerName' : 'QMGR1', 'queueManagerHost' : 'localhost', 'queueManagerPort' : '1415', 'serverConnectionChannelName' : 'CH1', 'scope': '/Cell:cell01/'}}, action='W')
        self.mqq = AdminConfig.getid('/MQQueue:AccountingHVMessageSendQueue/')
        self.jndiName=AdminConfig.showAttribute(self.mqq, 'jndiName')
        self.assertEqual(self.jndiName, 'jms/Bogus')

    def testMQQRead(self):
        self.cg.processConfigItem(cmdDict={'MQQueue' : {'name' : 'AccountingHVMessageSendQueue', 'jndiName' : 'dovetail/jms/AccountingHVMessageSendQueue', 'persistence' : 'PERSISTENT', 'baseQueueName' : 'AccountingHVMessageSendQueue', 'baseQueueManagerName' : 'QMGR1', 'queueManagerHost' : 'localhost', 'queueManagerPort' : '1415', 'serverConnectionChannelName' : 'CH1', 'scope': '/Cell:cell01/'}}, action='W')
        self.cg.processConfigItem(cmdDict={'MQQueue' : {'name' : 'AccountingHVMessageSendQueue', 'jndiName' : 'jms/Bogus', 'persistence' : 'PERSISTENT', 'baseQueueName' : 'AccountingHVMessageSendQueue', 'baseQueueManagerName' : 'QMGR1', 'queueManagerHost' : 'localhost', 'queueManagerPort' : '1415', 'serverConnectionChannelName' : 'CH1', 'scope': '/Cell:cell01/'}})
        self.mqq = AdminConfig.getid('/MQQueue:AccountingHVMessageSendQueue/')
        self.jndiName=AdminConfig.showAttribute(self.mqq, 'jndiName')
        self.assertEqual(self.jndiName, 'dovetail/jms/AccountingHVMessageSendQueue')

    def testSIBCreate(self):
        self.cg.processAdminTask(cmdDict={'SIBus' : {'name' : 'DovetailSIBus', 'scope' : '/Cell:cell01'}}, action='W')
        self.sib = AdminConfig.getid('/SIBus:DovetailSIBus/')
        self.name=AdminConfig.showAttribute(self.sib, 'name')
        self.assertEqual(self.name, 'DovetailSIBus')

    def testSIBModify(self):
        self.cg.processAdminTask(cmdDict={'SIBus' : {'name' : 'DovetailSIBus', 'scope' : '/Cell:cell01', 'description' : 'Description1'}}, action='W')
        self.cg.processAdminTask(cmdDict={'SIBus' : {'name' : 'DovetailSIBus', 'scope' : '/Cell:cell01', 'description' : 'Description2'}}, action='W')
        self.sib = AdminConfig.getid('/SIBus:DovetailSIBus/')
        self.description=AdminConfig.showAttribute(self.sib, 'description')
        self.assertEqual(self.description, 'Description2')

    def testSIBRead(self):
        self.cg.processAdminTask(cmdDict={'SIBus' : {'name' : 'DovetailSIBus', 'scope' : '/Cell:cell01', 'description' : 'Description1'}}, action='W')
        self.cg.processAdminTask(cmdDict={'SIBus' : {'name' : 'DovetailSIBus', 'scope' : '/Cell:cell01', 'description' : 'Description2'}})
        self.sib = AdminConfig.getid('/SIBus:DovetailSIBus/')
        self.description=AdminConfig.showAttribute(self.sib, 'description')
        self.assertEqual(self.description, 'Description1')

    def testSIBBusMemberCreate(self):
        self.cg.processAdminTask(cmdDict={'SIBus' : {'name' : 'DovetailSIBus', 'scope' : '/Cell:cell01', 'description' : 'Description1'}}, action='W')
        self.cg.processAdminTask(cmdDict={'SIBusMember' : {'scope' : '/SIBus:DovetailSIBus/', 'server' : 'srv01', 'node' : 'node01'}}, action='W')
        self.sib = AdminConfig.getid('/SIBus:DovetailSIBus/')
        self.name=AdminConfig.showAttribute(self.sib, 'name')
        self.assertEqual(self.name, 'DovetailSIBus')

    def testSIBTopicSpaceCreate(self):
        self.cg.processAdminTask(cmdDict={'SIBus' : {'name' : 'DovetailSIBus', 'scope' : '/Cell:cell01', 'description' : 'Description1'}}, action='W')
        self.cg.processAdminTask(cmdDict={'SIBusMember' : {'scope' : '/SIBus:DovetailSIBus/', 'server' : 'srv01', 'node' : 'node01'}}, action='W')
        self.cg.processAdminTask(cmdDict={'SIBTopicSpace': {'identifier': 'CacheUpdateTopic', 'scope': '/SIBus:DovetailSIBus/', 'topicAccessCheckRequired': 'false'}}, action='W')
        self.sib = AdminConfig.getid('/SIBus:DovetailSIBus/')
        self.name=AdminConfig.showAttribute(self.sib, 'name')
        self.assertEqual(self.name, 'DovetailSIBus')

    def testJDBCProviderCreate(self):
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar', 'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true'}}, action='W')
        self.jdbcprov = AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')
        self.implementationClassName=AdminConfig.showAttribute(self.jdbcprov, 'implementationClassName')
        self.assertEqual(self.implementationClassName, 'oracle.jdbc.xa.client.OracleXADataSource')

    def testDataSourceCreate(self):
        self.cg.processConfigItem(cmdDict={'JDBCProvider': {'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar', 'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true'}}, action='W')
        self.cg.processConfigItem(cmdDict={'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'authDataAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XAEVPSJDBCProvider/'}}, action='W')
        self.jdbcprov = AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')
        self.implementationClassName=AdminConfig.showAttribute(self.jdbcprov, 'implementationClassName')
        self.assertEqual(self.implementationClassName, 'oracle.jdbc.xa.client.OracleXADataSource')

if __name__ == '__main__' or __name__ == 'main':

    #test suite that runs individual tests: use this for speed and enable only the tests you are develop[ing for.
    suite = unittest.TestSuite()
    #suite.addTest(TestProcessCommandsBASE('testSIBCreate'))
    #suite.addTest(TestProcessCommandsBASE('testSIBModify'))
    #suite.addTest(TestProcessCommandsBASE('testSIBRead'))
    suite.addTest(TestProcessCommandsBASE('testGenerateCommands'))
    suite.addTest(TestProcessCommandsBASE('testGenerateCommandsException'))
    unittest.TextTestRunner(verbosity=2).run(suite)

    #Test suite to run everything.  Use this to sanity check all tests.
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestProcessCommandsBASE)
    #unittest.TextTestRunner(verbosity=2).run(suite)
