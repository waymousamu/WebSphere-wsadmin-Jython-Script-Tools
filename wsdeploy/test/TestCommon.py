CONFDICT_ND = [{'env': {'name': 'mp66'}},
               {'Cell': {'name': 'CCITstLP0ECell001'}},
               {'dmgr': {'port': '10878', 'host': '10.152.30.16'}},
               {'ServerCluster': {'name': 'CLTLPOEAts001', 'scope': '/Cell:CCITstLP0ECell001/'}},
               {'ClusterMember': {'scope': '/ServerCluster:CLTLPOEAts001/', 'memberName': 'X-CMTLPOEAtsSrv001', 'nodeName': 'X-CCITstLP0ENode001'}},
               {'ClusterMember': {'scope': '/ServerCluster:CLTLPOEAts001/', 'memberName': 'X-CMTLPOEAtsSrv002', 'nodeName': 'X-CCITstLP0ENode002'}},
               ]

CONFXML_ND = """
            <env name="mp66">
                <Cell name="CCITstLP0ECell001">
                    <dmgr host="10.152.30.16" port="10878"/>
                    <ServerCluster name="CLTLPOEAts001">
                        <ClusterMember memberName="X-CMTLPOEAtsSrv001" nodeName="X-CCITstLP0ENode001"/>
                        <ClusterMember memberName="X-CMTLPOEAtsSrv002" nodeName="X-CCITstLP0ENode002"/>
                    </ServerCluster>
                </Cell>
            </env>
            """
CONFDICT_BASE = [
                 {'env': {'name': 'altus3400_Base'}},
                 {'Cell': {'name': 'cell01'}},
                 {'JAASAuthData': {'password': '{xor}LDo8LTor', 'userId': 'swaymouth', 'alias': 'dps_oracle_alias', 'scope': '/Cell:cell01/'}},
                 {'dmgr': {'port': '8880', 'host': 'altus3400.dovetail.net'}}, {'Node': {'name': 'node01', 'scope': '/Cell:cell01/'}},
                 {'Server': {'name': 'srv01', 'scope': '/Node:node01/'}},
                 {'ProcessExecution': {'runAsUser': 'websphere', 'runAsGroup': 'websphere', 'scope': '/Server:srv01/'}},
                 {'JavaVirtualMachine': {'scope': '/Server:srv01/', 'genericJvmArguments': '-Xlp', 'maximumHeapSize': '2048', 'initialHeapSize': '1024'}},
                 {'JDBCProvider': {'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar', 'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true'}},
                 {'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'node01/dps_oracle_alias', 'authDataAlias': 'node01/dps_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XAEVPSJDBCProvider/'}},
                 {'J2EEResourceProperty': {'name': 'useRRASetEquals', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.String', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnection', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryCount', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Integer', 'value': '5'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryInterval', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Long', 'value': '5'}},
                 {'ConnectionPool': {'maxConnections': '1000', 'scope': '/DataSource:Q5DataSource/', 'testConnectionInterval': '3', 'minConnections': '5', 'testConnection': 'true'}},
                 {'MQQueueConnectionFactory': {'transportType': 'BINDINGS_THEN_CLIENT', 'port': '1414', 'name': 'QCF1', 'scope': '/Cell:cell01/', 'host': 'localhost', 'channel': 'CH1', 'queueManager': 'QM1', 'jndiName': 'jms/QCF1'}},
                 {'connectionPool': {'maxConnections': '200', 'scope': '/MQQueueConnectionFactory:QCF1/'}},
                 {'sessionPool': {'scope': '/MQQueueConnectionFactory:QCF1/', 'minConnections': '0'}},
                 {'MQQueue': {'name': 'AccountingHVMessageSendQueue', 'baseQueueName': 'AccountingHVMessageSendQueue', 'serverConnectionChannelName': 'CH1', 'baseQueueManagerName': 'QM1', 'jndiName': 'dovetail/jms/AccountingHVMessageSendQueue', 'queueManagerHost': 'localhost', 'persistence': 'PERSISTENT', 'scope': '/Cell:cell01/', 'queueManagerPort': '1414'}},
                 {'SIBus': {'name': 'DovetailSIBus', 'scope': '/Cell:cell01/'}},
                 {'SIBusMember': {'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01'}},
                 {'SIBTopicSpace': {'identifier': 'CacheUpdateTopic', 'scope': '/SIBus:DovetailSIBus/', 'topicAccessCheckRequired': 'false', 'node': 'node01', 'server': 'srv01'}},
                 {'J2CResourceAdapter': {'name': 'SIB JMS Resource Adapter', 'scope': '/Cell:cell01/'}},
                 {'J2CActivationSpec': {'destinationJndiName': 'dovetail/jms/CacheUpdateTopic', 'name': 'CacheUpdateTopic', 'scope': '/J2CResourceAdapter:SIB JMS Resource Adapter/', 'jndiName': 'jms/CacheUpdateTopic'}},
                 {'J2EEResourceProperty': {'name': 'busName', 'scope': '/J2CActivationSpec:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'destinationType', 'scope': '/J2CActivationSpec:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'javax.jms.Topic', 'required': 'true'}},
                 {'J2EEResourceProperty': {'name': 'alwaysActivateAllMDBs', 'scope': '/J2CActivationSpec:CacheUpdateTopic/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2CAdminObject': {'name': 'CacheUpdateTopic', 'scope': '/J2CResourceAdapter:SIB JMS Resource Adapter/', 'jndiName': 'dovetail/jms/CacheUpdateTopic'}},
                 {'J2EEResourceProperty': {'name': 'BusName', 'scope': '/J2CAdminObject:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'TopicName', 'scope': '/J2CAdminObject:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'CacheUpdateTopic'}},
                 {'J2EEResourceProperty': {'name': 'TopicSpace', 'scope': '/J2CAdminObject:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'CacheUpdateTopic'}}
                 ]

CONFXML_BASE = """
            <env name="local">
                <Cell name="HP8200SWaymouthNode01Cell">
                    <Security>
                        <JAASAuthData alias="local_oracle_alias" userId="swaymouth" password="secret"/>
                    </Security>
                    <dmgr host="localhost" port="8880"/>
                    <Node name="HP8200SWaymouthNode01">
                        <Server name="server1">
                            <JavaProcessDef>
                                <ProcessExecution runAsUser="wasadmin" runAsGroup="wasadmin"/>
                                <JavaVirtualMachine initialHeapSize="256" maximumHeapSize="512" genericJvmArguments="-Dlog4j.root=WAS_HOME"/>
                            </JavaProcessDef>
                        </Server>
                    </Node>
                    <JDBCProvider name="XAEVPSJDBCProvider" description="XAEVPSJDBCProvider" providerType="Oracle JDBC Driver (XA)" implementationClassName="oracle.jdbc.xa.client.OracleXADataSource" xa="true" classpath="${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar">
                        <DataSource name="Q5DataSource" jndiName="weblogic.jdbc.jts.Q5DataSource" description="Q5DataSource" providerType="Oracle JDBC Driver (XA)" authDataAlias="HP8200SWaymouthNode01/local_oracle_alias" xaRecoveryAuthAlias="HP8200SWaymouthNode01/local_oracle_alias" statementCacheSize="600" datasourceHelperClassname="com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper">
                            <J2EEResourcePropertySet>
                                <J2EEResourceProperty name="useRRASetEquals" type="java.lang.String" value="true" required="false"/>
                                <J2EEResourceProperty name="transactionBranchesLooselyCoupled" type="java.lang.Boolean" value="true"/>
                                <J2EEResourceProperty name="validateNewConnection" type="java.lang.Boolean" value="true"/>
                                <J2EEResourceProperty name="validateNewConnectionRetryCount" type="java.lang.Integer" value="5"/>
                                <J2EEResourceProperty name="validateNewConnectionRetryInterval" type="java.lang.Long" value="5"/>
                            </J2EEResourcePropertySet>
                            <ConnectionPool maxConnections="1000" minConnections="5" testConnection="true" testConnectionInterval="3"/>
                        </DataSource>
                    </JDBCProvider>
                    <MQQueueConnectionFactory name="QCF1" jndiName="jms/QCF1" queueManager="QMGR1" host="localhost" port="1415" channel="CH1" transportType="BINDINGS_THEN_CLIENT">
                        <J2EEResourcePropertySet>
                            <connectionPool maxConnections="200"/>
                            <sessionPool minConnections="0"/>
                        </J2EEResourcePropertySet>
                    </MQQueueConnectionFactory>
                    <MQQueue name="AccountingHVMessageSendQueue" jndiName="dovetail/jms/AccountingHVMessageSendQueue" persistence="PERSISTENT" baseQueueName="AccountingHVMessageSendQueue" baseQueueManagerName="QMGR1" queueManagerHost="localhost" queueManagerPort="1415" serverConnectionChannelName="CH1"/>
                    <SIBus name="DovetailSIBus">
                        <SIBusMember server="server1" node="HP8200SWaymouthNode01"/>
                        <SIBTopicSpace identifier="CacheUpdateTopic" topicAccessCheckRequired="false" />
                    </SIBus>
                </Cell>
            </env>
            """