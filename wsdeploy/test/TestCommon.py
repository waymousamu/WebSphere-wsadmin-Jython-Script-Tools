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
CMDLIST_ND = [["Cell", {"name": "CCITstLP0ECell001"}],
              ["dmgr", {"host": "10.152.30.16", "port": "10878"}],
              ["AdminConfig.create('ServerCluster', (AdminConfig.getid('/Cell:CCITstLP0ECell001/')), '[[name CLTLPOEAts001]]')",
              "AdminConfig.createClusterMember((AdminConfig.getid('/ServerCluster:CLTLPOEAts001/')), (AdminConfig.getid('/Node:X-CCITstLP0ENode001/')), [['memberName', 'X-CMTLPOEAtsSrv001']])",
              "AdminConfig.createClusterMember((AdminConfig.getid('/ServerCluster:CLTLPOEAts001/')), (AdminConfig.getid('/Node:X-CCITstLP0ENode002/')), [['memberName', 'X-CMTLPOEAtsSrv002']])"]
              ]

CONFDICT_BASE = [
                 {'env': {'name': 'local'}},
                 {'Cell': {'name': 'HP8200SWaymouthNode01Cell'}},
                 {'JAASAuthData': {'alias': 'local_oracle_alias', 'userId': 'swaymouth', 'password': 'secret', 'scope': '/Cell:HP8200SWaymouthNode01Cell/'}},
                 {'dmgr': {'port': '8880', 'host': 'localhost'}},
                 {'Node': {'scope': '/Cell:HP8200SWaymouthNode01Cell/', 'name': 'HP8200SWaymouthNode01'}},
                 {'Server': {'scope': '/Node:HP8200SWaymouthNode01/', 'name': 'server1'}},
                 {'ProcessExecution': {'runAsUser': 'wasadmin', 'runAsGroup': 'wasadmin', 'scope': '/Server:server1/'}},
                 {'JavaVirtualMachine': {'scope': '/Server:server1/', 'genericJvmArguments': '-Dlog4j.root=WAS_HOME', 'maximumHeapSize': '512', 'initialHeapSize': '256'}},
                 {'JDBCProvider': {'name': 'XAEVPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:HP8200SWaymouthNode01Cell/', 'description': 'XAEVPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true', 'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'}},
                 {'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'authDataAlias': 'HP8200SWaymouthNode01/local_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XAEVPSJDBCProvider/'}},
                 {'J2EEResourceProperty': {'name': 'useRRASetEquals', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.String', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnection', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryCount', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Integer', 'value': '5'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryInterval', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Long', 'value': '5'}},
                 {'ConnectionPool': {'maxConnections': '1000', 'scope': '/DataSource:Q5DataSource/', 'testConnectionInterval': '3', 'minConnections': '5', 'testConnection': 'true'}},
                 {'MQQueueConnectionFactory': {'transportType': 'BINDINGS_THEN_CLIENT', 'port': '1415', 'name': 'QCF1', 'scope': '/Cell:HP8200SWaymouthNode01Cell/', 'host': 'localhost', 'channel': 'CH1', 'queueManager': 'QMGR1', 'jndiName': 'jms/QCF1'}},
                 {'connectionPool': {'maxConnections': '200', 'scope': '/MQQueueConnectionFactory:QCF1/'}},
                 {'sessionPool': {'minConnections': '0', 'scope': '/MQQueueConnectionFactory:QCF1/'}},
                 {'MQQueue' : {'name' : 'AccountingHVMessageSendQueue', 'jndiName' : 'dovetail/jms/AccountingHVMessageSendQueue', 'persistence' : 'PERSISTENT', 'baseQueueName' : 'AccountingHVMessageSendQueue', 'baseQueueManagerName' : 'QMGR1', 'queueManagerHost' : 'localhost', 'queueManagerPort' : '1415', 'serverConnectionChannelName' : 'CH1', 'scope': '/Cell:HP8200SWaymouthNode01Cell/'}}
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
                </Cell>
            </env>
            """
CMDLIST_BASE = [["Cell", {"name": "HP8200SWaymouthNode01Cell"}],
                ["dmgr", {"host": "localhost", "port": "8880"}],
                ["AdminConfig.create('Server', (AdminConfig.getid('/Node:HP8200SWaymouthNode01/')), [['name', 'server1']])",
                 "AdmionConfig.modify('')"
                 "AdminConfig.create('JDBCProvider', (AdminConfig.getid('/Cell:HP8200SWaymouthNode01Cell/')), [['classpath', '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar'], ['implementationClassName', 'oracle.jdbc.xa.client.OracleXADataSource'], ['name', 'XAEVPSJDBCProvider'], ['description', 'XAEVPSJDBCProvider'], ['providerType', 'Oracle JDBC Driver (XA)'], ['xa', 'true']])",
                 "AdminConfig.create('DataSource', (AdminConfig.getid('/JDBCProvider:XAEVPSJDBCProvider/')), [['name', 'Q5DataSource'], ['datasourceHelperClassname', 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper'], ['statementCacheSize', '600'], ['providerType', 'Oracle JDBC Driver (XA)'], ['jndiName', 'weblogic.jdbc.jts.Q5DataSource'], ['xaRecoveryAuthAlias', 'HP8200SWaymouthNode01/local_oracle_alias'], ['authDataAlias', 'HP8200SWaymouthNode01/local_oracle_alias'], ['description', 'Q5DataSource']])"]
                ]