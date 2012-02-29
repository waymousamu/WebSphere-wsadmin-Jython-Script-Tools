# Author: Raja Tatapudi
#-------------------------------------------------------------
# Jython Script to create SMBC Application resources :
# JDBC Datasources, JMS Queues & Topics, Connection factories,
# Service Interface Bus etc
#-------------------------------------------------------------

import sys
from java.lang import Integer
from java.lang import String

def wsadminToList(inStr):
    outList=[]
    if (len(inStr)>0 and inStr[0]=='[' and inStr[-1]==']'):
            tmpList = inStr[1:-1].split() #splits space-separated lists,
    else:
            tmpList = inStr.split("\n")   #splits for Windows or Linux
    for item in tmpList:
            item = item.rstrip();         #removes any Windows "\r"
            if (len(item)>0):
                    outList.append(item)
    return outList
#endDef

#-----------------
# Util Definitions
#-----------------

#---------------------
# Read a property file
#---------------------
def loadProperties ( propFileName ):
        from java.io import FileInputStream
        from java.util import Properties

        fileprop = Properties(  )

        fileHandler = open(propFileName)
        fileContents = fileHandler.readlines()
        fileprop = {}
        for line in fileContents:
                line = line.strip()
                if(len(line)==0 or line[0:1]=="#"): continue
                lineIndex = line.find("=")
                fileprop[line[0:lineIndex]] = line[lineIndex+1:]
        #endFor (read of propertyFile=fileStream into variable=fileprop)
        fileHandler.close()

        return fileprop
#endDef

#----------------------------------------
# Get Datasource Custom Proeperties List
#----------------------------------------
def getDSCustomPropsList ( ds ):
        print "getDSCustomPropList"
        global AdminConfig
        print "line 26"
        customProps = AdminConfig.showAttribute(ds, "propertySet" )
        print "line 28"
        propsList = AdminConfig.showAttribute(customProps, "resourceProperties" )
        print "line 30"
        print "propsList="+propsList
        props = wsadminToList(propsList)
        for prop in props:
                print "line 35"
                print "prop = "+prop
                propName = AdminConfig.showAttribute(prop, "name" )
                print "propName was "+propName
        #endFor
        return props
#endDef

#---------------------------------
# Set Datasource Custom Proeperty
#---------------------------------
def setDSCustomProperty ( propList, name, value ):
    print "setDSCustomProperty"
    for prop in propList:
        propName = AdminConfig.showAttribute(prop, "name" )
        if (propName == name):
                AdminConfig.modify(prop, [["value", value]] )
                AdminConfig.save()
                break
        #endIf
    #endFor
#endDef

#---------------------------------------
# Create Oracle XA DataSource Properties
#---------------------------------------
def utilCreateOracleXA_DS_Properties ( parent ):
	print "CreateOracleXA_DS_Properties"
	propsSet = AdminConfig.create("J2EEResourcePropertySet", parent, [], "propertySet" )

        utilCreateCustomProperty(propsSet, "driverType", "java.lang.String", "", "The type of the driver. The possible values are: thin, oci8.", "false" )
        utilCreateCustomProperty(propsSet, "TNSEntryName", "java.lang.String", "", "The entry name which is used for the Oracle OCI driver.", "false" )
        utilCreateCustomProperty(propsSet, "networkProtocol", "java.lang.String", "", "Whether to use TCP/IP or IPC or any other protocol", "false" )
        utilCreateCustomProperty(propsSet, "databaseName", "java.lang.String", "", "The database name. For example, enter sample to make your Data Source point to sample.  used for thin driver setup", "false" )
        utilCreateCustomProperty(propsSet, "serverName", "java.lang.String", "", "The name of the server. used for thin driver setup", "false" )
        utilCreateCustomProperty(propsSet, "portNumber", "java.lang.Integer", "1521", "The TCP/IP port number where the jdbc driver resides. used for thin driver setup", "false" )
        utilCreateCustomProperty(propsSet, "dataSourceName", "java.lang.String", "", "The name of the Data Source.", "false" )
        utilCreateCustomProperty(propsSet, "useRRASetEquals", "java.lang.Boolean", "true", "Avoid thread deadlocks while getting the data source connection pool", "true" )
        utilCreateCustomProperty(propsSet, "URL", "java.lang.String", "", "This is a required property. The URL indicating the database from which the Data Source will obtain connections, such as 'jdbc:oracle:thin:@localhost:1521:sample' for thin driver and 'jdbc:oracle:oci8:@sample' for thick driver.", "true" )
        utilCreateCustomProperty(propsSet, "loginTimeout", "java.lang.Integer", "", "The maximum time to attempt to connect a database. If this value is non-zero, attempt to connect to the database will timeout when this specified value is reached.", "false" )
        utilCreateCustomProperty(propsSet, "description", "java.lang.String", "", "The description of this datasource.", "false" )
        utilCreateCustomProperty(propsSet, "enableMultithreadedAccessDetection", "java.lang.Boolean", "false", "Indicates whether or not to detect multithreaded access to a Connection and its corresponding Statements, ResultSets, and MetaDatas.", "false" )
        utilCreateCustomProperty(propsSet, "transactionBranchesLooselyCoupled", "java.lang.Boolean", "false", "This property is introduced as a result of Oraclebug 2511780, Oracle Patch for 2511780 must be installed before setting this property to true, failure to do that would cause a program error.  Please check the WebSphere readme file for more info .", "false" )
        utilCreateCustomProperty(propsSet, "preTestSQLString", "java.lang.String", "SELECT 1 FROM DUAL", "This SQL statement is used for pre-test connection function. For example, SELECT 1 FROM [TESTTABLE]. If pre-test connection is enabled in j2c.properties, this SQL statement will be executed to the connection to make sure the connection is good. If you leave this field blank, the default SQL statement, SELECT 1 FROM TABLE1, will be used at runtime. This will slow down the execution because of the exception handling if table TABLE1 is not defined in the database. Users are recommended to provide their own SQL statement to improve the performance.", "false" )
        utilCreateCustomProperty(propsSet, "oracle9iLogTraceLevel", "java.lang.String", "2", "Oracle9i and prior: The oracle9iLogTraceLevel specifies which message levels will be logged .Default is 2.  Possible values from highest to lowest 3, 2, 1", "false" )
#endDef

def utilCreateCustomProperty ( parent, myName, myType, myValue, myDesc, myRequired ):
	name = ["name", myName]
        type = ["type", myType]
        value = ["value", myValue]
        description = ["description", myDesc]
        required = ["required", myRequired]

	prop = [name, type, value, description, required]

        AdminConfig.create("J2EEResourceProperty", parent, prop )
        AdminConfig.save()
#endDef
#----------------------------------------------------------------------------------------------------

#-----------------------
#  Setting JVM arguments
#-----------------------

# Setting scope
parentNode = AdminConfig.getid("/Cell:"+'evps-waymouthsCell'+"/Node:"+'evps-waymouthsNode'+"/Server:"+'server1')

# Setting JVM Scope
jvm = AdminConfig.list("JavaVirtualMachine", parentNode )

# Collect old JVM args if any ...
oldArgs = AdminConfig.showAttribute(jvm, "genericJvmArguments" )

# Collect old classpath if any ...
oldClasspath = AdminConfig.showAttribute(jvm, "classpath")

JVM_ARGS = "-DQ5INSTANCEID=1 -DQ5PINTRANSACTIONS=true -DSTPBULKSIZE=100 -DQ5CACHEFILTER=com.dovetailsys.shared.util.CacheFilter -DQ5CACHEOBJECTS=1024 -Dcom.dovetailsystems.q5.useLOBs=No -Dperform.bic.lookup=yes -Dperform.iban.validation=no -DQ5TRANSACTION_TIMEOUT=600 -DDEFAULT_GATEWAY_ROOT=/gateway -Dcom.ibm.CORBA.iiop.noLocalCopies=true -Xnoclassgc -XX:MaxPermSize=128m"

print "-\}  Setting JVM ARGS....."+JVM_ARGS

# Modify the JVM arguments
AdminConfig.modify(jvm, [["genericJvmArguments", oldArgs+" "+JVM_ARGS], ["classpath", 'C:/development/hsbc84x/builds/config'], ["initialHeapSize", 512], ["maximumHeapSize", 784]])

AdminConfig.save()

newJVMArgs = AdminConfig.showAttribute(jvm, "genericJvmArguments")
print "-\}  JVM ARGS:    ->  "+newJVMArgs

#------------------------------------------------------------
#  Setting max-beans-in-free-pool, initial-beans-in-free-pool
#------------------------------------------------------------

# Collect old JVM args if any ...
oldArgs = AdminConfig.showAttribute(jvm, "genericJvmArguments" )

ejb_JVM_ARGS = "-Dcom.ibm.websphere.ejbcontainer.poolSize=" + 'DPSApp' + "#ExtentCache_MDBEAN.jar#ExtentCacheMDBean=1,5 -Dcom.ibm.websphere.ejbcontainer.poolSize=" + 'DPSApp' + "#ExtentCache_MDBEAN.jar#AsyncActionMDBean=5,100 -Dcom.ibm.websphere.ejbcontainer.poolSize=" + 'DPSApp' + "#ADVISINGEJB.jar#ReportGenerationMessageBean=1,5 -Dcom.ibm.websphere.ejbcontainer.poolSize="+'DPSApp'+"#ATRMATCHINGEJB.jar#ATRMatchingMDBean=1,5 -Dcom.ibm.websphere.ejbcontainer.poolSize=" + 'DPSApp' + "#INTERNALFILTEREJB.jar#IntFilterReleasePaymentsMD=1,5"

print "-\}  Setting EJB Container JVM ARGS....."+ejb_JVM_ARGS

# Modify the JVM arguments
AdminConfig.modify(jvm, [["genericJvmArguments", oldArgs+" "+ejb_JVM_ARGS], ["classpath", 'C:/development/hsbc84x/builds/config'], ["initialHeapSize", 512], ["maximumHeapSize", 784]])

AdminConfig.save()

newejb_JVMArgs = AdminConfig.showAttribute(jvm, "genericJvmArguments")
print "-\}  JVM ARGS:    ->  "+newejb_JVMArgs

#--------------------------------------------------
#  Setting max-beans-in-cahce, idle-timeout-seconds
#--------------------------------------------------

ejbContainer = AdminConfig.list('EJBContainer', parentNode)
print ejbContainer
AdminConfig.modify(ejbContainer, [['cacheSettings', [['cacheSize', 2000], ['cleanupInterval', 0]]]])

#-----------------------
#  For Creating J2C User
#-----------------------
dbUser = 'swaymouth'
dbPassword = 'secret'

node = AdminControl.getNode()
userAlias = node+"/"+dbUser

domain = AdminConfig.getid("/Cell:"+'evps-waymouthsCell'+"/Security:/")
print "-\}  Security Domain   ->  "+domain

alias = ["alias", userAlias]
userid = ["userId", dbUser]
password = ["password", dbPassword]
jaasAttrs = [alias, userid, password]
dataSourceComponentMngAuthAlias = AdminConfig.create("JAASAuthData", domain, jaasAttrs)

print "-\}  Saving Changes"
AdminConfig.save()

#----------------------------
#  For Creating JDBCProviders
#----------------------------
global oracleXAProvider
global oracleNonXAProvider

xaJdbcName = ["name", "XADPSJDBCProvider"]
xaJdbcDesc = ["description", "XA enabled JDBC Provider for DPS"]
xaProvider = ["providerType", "Oracle JDBC Driver"]
classpath = ["classpath", 'c:/ibm/websphere7'+"/lib/ext"]
xaImplClass = ["implementationClassName", "oracle.jdbc.xa.client.OracleXADataSource"]

print "-\}       Start!!!  XADPSJDBCProvider"
print "-\}"
print "-\}"
print "-\}       parent="+parentNode

jdbcXAAttrs = [xaJdbcName, xaJdbcDesc, xaProvider, classpath, xaImplClass]

oracleXAProvider = AdminConfig.create("JDBCProvider", parentNode, jdbcXAAttrs )
print "-\}  Saving XA Provider"
AdminConfig.save()

nonXAJdbcName = ["name", "DPSJDBCProvider"]
nonXAJdbcDesc = ["description", "Non-XA JDBC provider for DPS"]
nonXAProvider = ["providerType", "Oracle JDBC Driver"]
nonXAImplClass = ["implementationClassName", "oracle.jdbc.pool.OracleConnectionPoolDataSource"]

print "-\}       Start!!!  DPSJDBCProvider"
print "-\}"
print "-\}"
print "-\}       parent="+parentNode

jdbcNonXAAttrs = [nonXAJdbcName, nonXAJdbcDesc, nonXAProvider, classpath, nonXAImplClass]

oracleNonXAProvider = AdminConfig.create("JDBCProvider", parentNode, jdbcNonXAAttrs )
print "-\}  Saving Non XA Provider"
AdminConfig.save()

print "-\}"
print "-\}"
print "-\}       Success!!!  created data source providers"

#--------------------------
#  For Creating DataSources
#=================================================================
# Create and configure a JDBC Data Source, and sets the JDBC user.
#=================================================================
dbHostName = 'localhost'
dbPort = '1521'
databaseName = 'XE'

#========== XA DATA SOURCE ( Q5DataSource )=============

print "-\}       Start!!!  createQ5Datasource"
print "-\}"
print "-\}"

dataSourceURL = "jdbc:oracle:thin:@"+dbHostName+":"+dbPort+":"+databaseName
dataSourceDriverType = "thin"
helperClass = 'Oracle11g'
print "-\}       Oracle Version !!! "+helperClass

if (helperClass == "Oracle11g"):
	helperClass = "com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper"
else:
	helperClass = "com.ibm.websphere.rsadapter.Oracle10gDataStoreHelper"

print "-\}       Oracle Version !!! "+helperClass

dataSourceName = "Q5DataSource"

dsName = ["name", dataSourceName]
dsDesc = ["description", dataSourceName]
jndiName = ["jndiName", "weblogic.jdbc.jts.Q5DataSource"]
authentication = ["authDataAlias", userAlias]
st_cachesize = ["statementCacheSize", "10"]
ds_hlpclass = ["datasourceHelperClassname", helperClass]
map_configAlias_attr=["mappingConfigAlias", "DefaultPrincipalMapping"]
map_attrs=[authentication, map_configAlias_attr]
mapping_attr=["mapping", map_attrs]

ds_attr = [dsName, dsDesc, jndiName, authentication, st_cachesize, ds_hlpclass, mapping_attr ]

newQ5DataSource = AdminConfig.create("DataSource", oracleXAProvider, ds_attr )
AdminConfig.save()
print "-\}       Modifying connection pool properties for !!! " + newQ5DataSource
AdminConfig.modify(AdminConfig.getid("/DataSource:"+dataSourceName+"/" ), [["connectionPool", [["connectionTimeout", 300], ["maxConnections", 200], ["minConnections", 10]]]] )
AdminConfig.save()
print "-\}       Connection pool properties modified for !!! " + newQ5DataSource
utilCreateOracleXA_DS_Properties(newQ5DataSource)
propsList = getDSCustomPropsList(newQ5DataSource)
setDSCustomProperty(propsList, "URL", dataSourceURL)
setDSCustomProperty(propsList, "driverType", dataSourceDriverType)

print "-\}"
print "-\}"
print "-\}       Success!!!  createQ5Datasource"

#========== XA DATA SOURCE ( Q5HistDataSource )=============

print "-\}       Start!!!  createQ5HistDataSource"
print "-\}"
print "-\}"

dataSourceName="Q5HistDataSource"

dsName = ["name", dataSourceName]
dsDesc = ["description", dataSourceName]
jndiName = ["jndiName", "weblogic.jdbc.jts.Q5HistDataSource"]
authentication = ["authDataAlias", userAlias]
st_cachesize = ["statementCacheSize", "10"]
ds_hlpclass = ["datasourceHelperClassname", helperClass]
map_configAlias_attr=["mappingConfigAlias", "DefaultPrincipalMapping"]
map_attrs=[authentication, map_configAlias_attr]
mapping_attr=["mapping", map_attrs]

ds_attr = [dsName, dsDesc, jndiName, authentication, st_cachesize, ds_hlpclass, mapping_attr ]

newQ5HistDataSource = AdminConfig.create("DataSource", oracleXAProvider, ds_attr )
AdminConfig.save()
print "-\}       Modifying connection pool properties for !!! " + newQ5HistDataSource
AdminConfig.modify(AdminConfig.getid("/DataSource:"+dataSourceName+"/" ), [["connectionPool", [["connectionTimeout", 300], ["maxConnections", 200], ["minConnections", 10]]]] )
AdminConfig.save()
print "-\}       Connection pool properties modified for !!! " + newQ5HistDataSource
utilCreateOracleXA_DS_Properties(newQ5HistDataSource)
propsList = getDSCustomPropsList(newQ5HistDataSource)
setDSCustomProperty(propsList, "URL", dataSourceURL)
setDSCustomProperty(propsList, "driverType", dataSourceDriverType)

print "-\}"
print "-\}"
print "-\}       Success!!!  createQ5HistDataSource"

#========== NON-XA DATA SOURCE ( Q5DDLDataSource )==========

print "-\}       Start!!!  createQ5DDLDataSource"
print "-\}"
print "-\}"

dataSourceName="Q5DDLDataSource"

dsName = ["name", dataSourceName]
dsDesc = ["description", dataSourceName]
jndiName = ["jndiName", "weblogic.jdbc.jts.Q5DDLDataSource"]
authentication = ["authDataAlias", userAlias]
st_cachesize = ["statementCacheSize", "10"]
ds_hlpclass = ["datasourceHelperClassname", helperClass]
map_configAlias_attr=["mappingConfigAlias", "DefaultPrincipalMapping"]
map_attrs=[authentication, map_configAlias_attr]
mapping_attr=["mapping", map_attrs]

ds_attr = [dsName, dsDesc, jndiName, authentication, st_cachesize, ds_hlpclass, mapping_attr ]

newQ5DDLDataSource = AdminConfig.create("DataSource", oracleNonXAProvider, ds_attr )
AdminConfig.save()
print "-\}       Modifying connection pool properties for !!! " + newQ5DDLDataSource
AdminConfig.modify(AdminConfig.getid("/DataSource:"+dataSourceName+"/" ), [["connectionPool", [["connectionTimeout", 300], ["maxConnections", 200], ["minConnections", 10]]]] )
AdminConfig.save()
print "-\}       Connection pool properties modified for !!! " + newQ5DDLDataSource
utilCreateOracleXA_DS_Properties(newQ5DDLDataSource)
propsList = getDSCustomPropsList(newQ5DDLDataSource)
setDSCustomProperty(propsList, "URL", dataSourceURL )
setDSCustomProperty(propsList, "driverType", dataSourceDriverType)

print "-\}"
print "-\}"
print "-\}       Success!!!  createQ5DDLDataSource"

#========== HISTORICAL NON-XA DATA SOURCE  ( Q5HistDDLDataSource )==========

print "-\}       Start!!!  createQ5HistDDLDataSource"
print "-\}"
print "-\}"

dataSourceName="Q5HistDDLDataSource"

dsName = ["name", dataSourceName]
dsDesc = ["description", dataSourceName]
jndiName = ["jndiName", "weblogic.jdbc.jts.Q5HistDDLDataSource"]
authentication = ["authDataAlias", userAlias]
st_cachesize = ["statementCacheSize", "10"]
ds_hlpclass = ["datasourceHelperClassname", helperClass]
map_configAlias_attr=["mappingConfigAlias", "DefaultPrincipalMapping"]
map_attrs=[authentication, map_configAlias_attr]
mapping_attr=["mapping", map_attrs]

ds_attr = [dsName, dsDesc, jndiName, authentication, st_cachesize, ds_hlpclass, mapping_attr ]

newQ5HistDDLDataSource = AdminConfig.create("DataSource", oracleNonXAProvider, ds_attr )
AdminConfig.save()
print "-\}       Modifying connection pool properties for !!! " + newQ5HistDDLDataSource
AdminConfig.modify(AdminConfig.getid("/DataSource:"+dataSourceName+"/" ), [["connectionPool", [["connectionTimeout", 300], ["maxConnections", 200], ["minConnections", 10]]]] )
AdminConfig.save()
print "-\}       Connection pool properties modified for !!! " + newQ5HistDDLDataSource
utilCreateOracleXA_DS_Properties(newQ5HistDDLDataSource)
propsList = getDSCustomPropsList(newQ5HistDDLDataSource)
setDSCustomProperty(propsList, "URL", dataSourceURL)
setDSCustomProperty(propsList, "driverType", dataSourceDriverType)

print "-\}"
print "-\}"
print "-\}       Success!!!  createQ5HistDDLDataSource"

#----------------------------------
#  Creating Service Integration Bus
#----------------------------------

siBusName = "DovetailSIBus"
siBusAttrs = ["-bus", siBusName, "-description", siBusName, "-secure", "FALSE"]

serviceIntegrationBus = AdminTask.createSIBus(siBusAttrs)
AdminConfig.save()

print "-\}"
print "-\}"
print "-\}       Success!!!  createSIBus:"+siBusName

#-----------------------------------------
#	 Adding Bus Members to created Bus
#-----------------------------------------

siBusMemberAttrs = ["-bus", siBusName, "-node", 'evps-waymouthsNode', "-server", 'server1']
AdminTask.addSIBusMember(siBusMemberAttrs)
AdminConfig.save() #save()
print "-\}"
print "-\}  New Member added to SIBus \[ "+siBusName+" \]"

#----------------------------------------
#	Queue Connection Factory Settings
#----------------------------------------
propFileName = 'C:/development/hsbc84x/websphere/evps'+"/properties/portdef.props";
props = loadProperties(propFileName)

sibEndPointAddress = props["SIB_ENDPOINT_ADDRESS"]
providerEndPoint = "localhost:"+sibEndPointAddress+":BootstrapBasicMessaging"

#-----------------------------------------------
#	Creating WAS XA Queue Connection Factory
#-----------------------------------------------
queueFactoryName = "DovetailJMSXAQueueConnectionFactory"
queueFactoryJndiName = "dovetail/jms/XAQueueConnectionFactory"

qcfAttrs = ["-name", queueFactoryName, "-jndiName", queueFactoryJndiName, "-busName", siBusName, "-type", "queue", "-targetType", "BusMember", "-targetSignificance", "Preferred", "-providerEndPoints", providerEndPoint, "-connectionProximity", "Bus", "-authDataAlias", userAlias, "-xaRecoveryAuthAlias", userAlias]
newWASXAQueueConnectionFactory = AdminTask.createSIBJMSConnectionFactory(parentNode, qcfAttrs)
AdminConfig.save() #save()

print "-\}  New WAS Queue Connection Factory: "+newWASXAQueueConnectionFactory+" created... "
print "-\}"

print "-\}  Modifying the Connection Pool Properties for Queue Connection Factory: "+newWASXAQueueConnectionFactory+" ... "
AdminConfig.modify(newWASXAQueueConnectionFactory, [["connectionPool", [["maxConnections", 100]]]] )
AdminConfig.save()
print "-\}  Connection Pool Properties for : "+newWASXAQueueConnectionFactory+" modified successfully... "

#-----------------------------------------------
#	Creating WAS Queue Connection Factory
#-----------------------------------------------
queueFactoryName = "DovetailJMSQueueConnectionFactory"
queueFactoryJndiName = "dovetail/jms/QueueConnectionFactory"

qcfAttrs = ["-name", queueFactoryName, "-jndiName", queueFactoryJndiName, "-busName", siBusName, "-type", "queue", "-targetType", "BusMember", "-targetSignificance", "Preferred", "-providerEndPoints", providerEndPoint, "-connectionProximity", "Bus", "-authDataAlias", userAlias]
newWASXAQueueConnectionFactory = AdminTask.createSIBJMSConnectionFactory(parentNode, qcfAttrs)
AdminConfig.save() #save()

print "-\}  New WAS Queue Connection Factory: "+newWASXAQueueConnectionFactory+" created... "
print "-\}"

print "-\}  Modifying the Connection Pool Properties for Queue Connection Factory: "+newWASXAQueueConnectionFactory+" ... "
AdminConfig.modify(newWASXAQueueConnectionFactory, [["connectionPool", [["maxConnections", 100]]]] )
AdminConfig.save()
print "-\}  Connection Pool Properties for : "+newWASXAQueueConnectionFactory+" modified successfully... "

#-----------------------------------------------
#	Creating WAS XA Topic Connection Factory
#-----------------------------------------------
topicFactoryName = "DovetailJMSXATopicConnectionFactory"
topicFactoryJndiName = "dovetail/jms/XATopicConnectionFactory"

qcfAttrs = ["-name", topicFactoryName, "-jndiName", topicFactoryJndiName, "-busName", siBusName, "-type", "topic", "-targetType", "BusMember", "-targetSignificance", "Preferred", "-providerEndPoints", providerEndPoint, "-connectionProximity", "Bus", "-authDataAlias", userAlias, "-xaRecoveryAuthAlias", userAlias]
newWASXATopicConnectionFactory = AdminTask.createSIBJMSConnectionFactory(parentNode, qcfAttrs)
AdminConfig.save() #save()

print "-\}  New WAS XA Topic Connection Factory: "+newWASXATopicConnectionFactory+" created... "
print "-\}"

print "-\}  Modifying the Connection Pool Properties for Topic Connection Factory: "+newWASXATopicConnectionFactory+" ... "
AdminConfig.modify(newWASXATopicConnectionFactory, [["connectionPool", [["maxConnections", 100]]]] )
AdminConfig.save()
print "-\}  Connection Pool Properties for : "+newWASXATopicConnectionFactory+" modified successfully... "

#------------------------------------------------------
#  For Creating SIB Queue Destinations & SIB JMS Queues
#------------------------------------------------------
filePath = 'C:/development/hsbc84x/HSBC/EVPS/config'+"/jmsqueues.txt"
fileData = open(filePath)

for line in fileData.readlines():
	queueName, jndiName = line.split(':')
	jndiName = jndiName.split('\n')
	print "-\}  Queue Name: "+queueName
	print "-\}  JNDI Name: "+jndiName[0]
    	# Creating SIBus Queue Destination
    	sibQDestAttrs = ["-bus", siBusName, "-type", "Queue", "-name", queueName, "-node", 'evps-waymouthsNode', "-server", 'server1']
    	newSIBusQDest = AdminTask.createSIBDestination( sibQDestAttrs )
    	print "-\}  New SIB Queue Destination "+newSIBusQDest
    	print "-\}"

    	# Creating Queue in JMS Default Messaging Provider
    	queueAttrs = ["-name", queueName, "-jndiName", jndiName[0], "-queueName", queueName, "-deliveryMode", "Application", "-busName", siBusName]
    	newWSJMSQueue = AdminTask.createSIBJMSQueue(parentNode, queueAttrs )
    	print "-\}  New WAS JMS Queue "+newWSJMSQueue
    	print "-\}"
	#endFor
fileData.close()
AdminConfig.save() #save()
print "-\}  SIB Queue Destinations, SIB JMS Queues created..."
print "-\}"

#-----------------------------------------------------
#  For Creating SIB Topic Destination & SIB JMS Topics
#-----------------------------------------------------
filePath = 'C:/development/hsbc84x/HSBC/EVPS/config'+"/jmstopics.txt"
fileData = open(filePath)

for line in fileData.readlines():
    	topicName, jndiName = line.split(':')
	jndiName = jndiName.split('\n')
	print "-\}  Topic Name: "+topicName
	print "-\}  JNDI Name: "+jndiName[0]
	# Creating SIBus Queue Destination
    	sibTDestAttrs = ["-bus", siBusName, "-type", "TopicSpace", "-name", topicName, "-node", 'evps-waymouthsNode', "-server", 'server1']
    	newSIBusTDest = AdminTask.createSIBDestination( sibTDestAttrs )
    	print "-\}  New SIB Topic Destination "+newSIBusTDest
    	print "-\}"

    	# Creating Topic in JMS Default Messaging Provider
    	topicAttrs = ["-name", topicName, "-jndiName", jndiName[0], "-topicSpace", topicName, "-topicName", topicName, "-deliveryMode", "Application", "-busName", siBusName]
    	newWSJMSTopic = AdminTask.createSIBJMSTopic(parentNode, topicAttrs )
    	print "-\}  New WAS JMS Topic "+newWSJMSTopic
    	print "-\}"
#endFor
fileData.close()
AdminConfig.save() #save()
print "-\}  SIB Topic Destinations, SIB JMS Topics created..."
print "-\}"

#---------------------------------------------------
#	Creating WAS Activation Specification Queues
#---------------------------------------------------

# Activation Specification for ExtentCacheMDBean
attrsList = ["-name", "ExtentCacheMDBeanActivation", "-jndiName", "jms/CacheUpdateTopic", "-busName", siBusName, "-destinationType", "Topic", "-destinationJndiName", "dovetail/jms/CacheUpdateTopic"]
newWASActivationSpecification = AdminTask.createSIBJMSActivationSpec(parentNode, attrsList)

AdminConfig.save() #save()

print "-\}  ExtentCacheMDBean Activation Specification : "+newWASActivationSpecification+" created... "
print "-\}"

# Activation Specification for AsyncActionMDBean - Queue
attrsList = ["-name", "AsyncActionMDBeanActivation", "-jndiName", "jms/AsyncActionQueue", "-busName", siBusName, "-destinationType", "Queue", "-destinationJndiName", "dovetail/jms/AsyncActionQueue"]
newWASActivationSpecification = AdminTask.createSIBJMSActivationSpec(parentNode, attrsList)

AdminConfig.save() #save()

print "-\}  AsyncActionMDBean Activation Specification : "+newWASActivationSpecification+" created... "
print "-\}"

# Activation Specification for IntFilterReleasePaymentsMDBean - Queue
attrsList = ["-name", "IntFilterMDBeanActivation", "-jndiName", "jms/IntFilterReleasePaymentsQueue", "-busName", siBusName, "-destinationType", "Queue", "-destinationJndiName", "dovetail/jms/AsyncActionQueue"]
newWASActivationSpecification = AdminTask.createSIBJMSActivationSpec(parentNode, attrsList )

# Activation Specification for ATRMatchingMDBean - Queue
attrsList = ["-name", "ATRMatchingMDBeanActivation", "-jndiName", "jms/ATRMatchPaymentsQueue", "-busName", siBusName, "-destinationType", "Queue", "-destinationJndiName", "dovetail/jms/ATRMatchPaymentsQueue"]
newWASActivationSpecification = AdminTask.createSIBJMSActivationSpec(parentNode, attrsList )

# Activation Specification for ReportGenerationMessageBean - Queue
attrsList = ["-name", "ReportGenerationMessageBeanActivation", "-jndiName", "jms/ReportGenerationMessageQueue", "-busName", siBusName, "-destinationType", "Queue", "-destinationJndiName", "dovetail/jms/ReportGenerationMessageQueue"]
newWASActivationSpecification = AdminTask.createSIBJMSActivationSpec(parentNode, attrsList )

# Save the Configuration
AdminConfig.save() #save()

# set up log tracing so it's not so noisy
# and set up PMI to troubleshoot any problems
# Works as of WebSphere 7
try:
    AdminServerManagement.configureTraceService("evps-waymouthsNode","server1","*=warning: com.dovetailsys.webapp.tags.VerifyPrivilegesTag=severe: org.apache.struts.config.impl.*=severe:com.dovetailsys.q5.DbAccess=severe:com.ibm.ws.webcontainer.WebContainer=off","SPECIFIED_FILE",[["enable", "true"], ["traceFormat", "LOG_ANALYZER"]])
    pmi=AdminConfig.list('PMIService',parentNode)
    AdminConfig.modify(pmi, [['enable', 'true'], ['statisticSet','all']])
    parentCell = AdminConfig.getid("/Cell:"+'evps-waymouthsCell')
    reqMetrics=AdminConfig.list('PMIRequestMetrics')
    AdminConfig.modify(reqMetrics, '[[traceLevel "PERF_DEBUG"] [armTransactionFactory ""] [dynamicEnable "true"] [enable "true"] [armType "ARM40"] [enableLog "true"] [enableARM "false"]]')
    AdminConfig.save()
except BSFError:
    print "Could not configure log levels, continuing."

print "-\}  IntFilterReleasePaymentsMDBean Activation Specification : "+newWASActivationSpecification+" created... "
print "-\}"