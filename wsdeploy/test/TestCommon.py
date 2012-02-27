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
                 {'JavaVirtualMachine': {'scope': '/Server:srv01/', 'genericJvmArguments': '-DQ5INSTANCEID=1 -DQ5PINTRANSACTIONS=true -DSTPBULKSIZE=100 -DQ5CACHEFILTER=com.dovetailsys.shared.util.CacheFilter -DQ5CACHEOBJECTS=1024 -Dcom.dovetailsystems.q5.useLOBs=No -Dperform.bic.lookup=yes -Dperform.iban.validation=no -DQ5TRANSACTION_TIMEOUT=600 -DDEFAULT_GATEWAY_ROOT=/gateway -Dcom.ibm.CORBA.iiop.noLocalCopies=true -Xnoclassgc', 'maximumHeapSize': '2048', 'initialHeapSize': '1024'}},
                 {'EJBCache': {'cleanupInterval': '0', 'scope': '/Server:srv01/', 'cacheSize': '2000'}},
                 {'JDBCProvider': {'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar', 'name': 'XADPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.xa.client.OracleXADataSource', 'scope': '/Cell:cell01/', 'description': 'XADPSJDBCProvider', 'providerType': 'Oracle JDBC Driver (XA)', 'xa': 'true'}},
                 {'DataSource': {'name': 'Q5DataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5DataSource', 'xaRecoveryAuthAlias': 'node01/dps_oracle_alias', 'authDataAlias': 'node01/dps_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XADPSJDBCProvider/'}},
                 {'J2EEResourceProperty': {'name': 'useRRASetEquals', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.String', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnection', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryCount', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Integer', 'value': '5', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryInterval', 'scope': '/DataSource:Q5DataSource/', 'type': 'java.lang.Long', 'value': '5', 'required': 'false'}},
                 {'ConnectionPool': {'connectionTimeout': '300', 'maxConnections': '200', 'scope': '/DataSource:Q5DataSource/', 'testConnectionInterval': '3', 'minConnections': '10', 'testConnection': 'true'}},
                 {'DataSource': {'name': 'Q5HistDataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '600', 'providerType': 'Oracle JDBC Driver (XA)', 'jndiName': 'weblogic.jdbc.jts.Q5HistDataSource', 'xaRecoveryAuthAlias': 'node01/dps_oracle_alias', 'authDataAlias': 'node01/dps_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:XADPSJDBCProvider/'}},
                 {'J2EEResourceProperty': {'name': 'useRRASetEquals', 'scope': '/DataSource:Q5HistDataSource/', 'type': 'java.lang.String', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5HistDataSource/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnection', 'scope': '/DataSource:Q5HistDataSource/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryCount', 'scope': '/DataSource:Q5HistDataSource/', 'type': 'java.lang.Integer', 'value': '5', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryInterval', 'scope': '/DataSource:Q5HistDataSource/', 'type': 'java.lang.Long', 'value': '5', 'required': 'false'}},
                 {'ConnectionPool': {'connectionTimeout': '300', 'maxConnections': '200', 'scope': '/DataSource:Q5HistDataSource/', 'testConnectionInterval': '3', 'minConnections': '10', 'testConnection': 'true'}},
                 {'JDBCProvider': {'classpath': '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar', 'name': 'DPSJDBCProvider', 'implementationClassName': 'oracle.jdbc.pool.OracleConnectionPoolDataSource', 'scope': '/Cell:cell01/', 'description': 'DPSJDBCProvider', 'providerType': 'Oracle JDBC Driver', 'xa': 'false'}},
                 {'DataSource': {'name': 'Q5DDLDataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '10', 'providerType': 'Oracle JDBC Driver', 'jndiName': 'weblogic.jdbc.jts.Q5DDLDataSource', 'xaRecoveryAuthAlias': 'node01/dps_oracle_alias', 'authDataAlias': 'node01/dps_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:DPSJDBCProvider/'}},
                 {'J2EEResourceProperty': {'name': 'useRRASetEquals', 'scope': '/DataSource:Q5DDLDataSource/', 'type': 'java.lang.String', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5DDLDataSource/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnection', 'scope': '/DataSource:Q5DDLDataSource/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryCount', 'scope': '/DataSource:Q5DDLDataSource/', 'type': 'java.lang.Integer', 'value': '5', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryInterval', 'scope': '/DataSource:Q5DDLDataSource/', 'type': 'java.lang.Long', 'value': '5', 'required': 'false'}},
                 {'ConnectionPool': {'connectionTimeout': '300', 'maxConnections': '200', 'scope': '/DataSource:Q5DDLDataSource/', 'testConnectionInterval': '3', 'minConnections': '10', 'testConnection': 'true'}},
                 {'DataSource': {'name': 'Q5HistDDLDataSource', 'datasourceHelperClassname': 'com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper', 'statementCacheSize': '10', 'providerType': 'Oracle JDBC Driver', 'jndiName': 'weblogic.jdbc.jts.Q5HistDDLDataSource', 'xaRecoveryAuthAlias': 'node01/dps_oracle_alias', 'authDataAlias': 'node01/dps_oracle_alias', 'description': 'Q5DataSource', 'scope': '/JDBCProvider:DPSJDBCProvider/'}},
                 {'J2EEResourceProperty': {'name': 'useRRASetEquals', 'scope': '/DataSource:Q5HistDDLDataSource/', 'type': 'java.lang.String', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'transactionBranchesLooselyCoupled', 'scope': '/DataSource:Q5HistDDLDataSource/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnection', 'scope': '/DataSource:Q5HistDDLDataSource/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryCount', 'scope': '/DataSource:Q5HistDDLDataSource/', 'type': 'java.lang.Integer', 'value': '5', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'validateNewConnectionRetryInterval', 'scope': '/DataSource:Q5HistDDLDataSource/', 'type': 'java.lang.Long', 'value': '5', 'required': 'false'}},
                 {'ConnectionPool': {'connectionTimeout': '300', 'maxConnections': '200', 'scope': '/DataSource:Q5HistDDLDataSource/', 'testConnectionInterval': '3', 'minConnections': '10', 'testConnection': 'true'}},
                 {'MQQueueConnectionFactory': {'transportType': 'BINDINGS_THEN_CLIENT', 'port': '1414', 'name': 'QCF1', 'scope': '/Cell:cell01/', 'host': 'localhost', 'channel': 'CH1', 'queueManager': 'QM1', 'jndiName': 'jms/QCF1'}},
                 {'connectionPool': {'maxConnections': '200', 'scope': '/MQQueueConnectionFactory:QCF1/'}},
                 {'sessionPool': {'scope': '/MQQueueConnectionFactory:QCF1/', 'minConnections': '0'}},
                 {'MQQueue': {'name': 'AccountingHVMessageSendQueue', 'baseQueueName': 'AccountingHVMessageSendQueue', 'serverConnectionChannelName': 'CH1', 'baseQueueManagerName': 'QM1', 'jndiName': 'dovetail/jms/AccountingHVMessageSendQueue', 'queueManagerHost': 'localhost', 'persistence': 'PERSISTENT', 'scope': '/Cell:cell01/', 'queueManagerPort': '1414'}},
                 {'SIBus': {'name': 'DovetailSIBus', 'scope': '/Cell:cell01/'}},
                 {'SIBusMember': {'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01'}},
                 {'SIBTopicSpace': {'identifier': 'CacheUpdateTopic', 'scope': '/SIBus:DovetailSIBus/', 'topicAccessCheckRequired': 'false', 'node': 'node01', 'server': 'srv01'}},
                 {'SIBQueue': {'identifier': 'AsyncActionQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'IntFilterReleasePaymentsQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'EBACreditTransferSendQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'EBADirectDebitSendQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'EBADirectDebitB2BSendQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'CustomerAndAccountReceiveQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'OFCLVRequestMessageSendQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'OFCLVResponseMessageReceiveQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'OFCHVRequestMessageSendQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'OFCHVResponseMessageReceiveQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'GFCHVRequestMessageSendQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'GFCHVResponseMessageReceiveQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'GFCLVResponseMessageReceiveQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'AccountingNotificationQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'AdvisingNotificationQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'DDAExternalLookupRequestQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'DDAExternalLookupResponseQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'AccountingLVMessageSendQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'SIBQueue': {'identifier': 'AccountingHVMessageSendQueue', 'scope': '/SIBus:DovetailSIBus/', 'node': 'node01', 'server': 'srv01', 'topicAccessCheckRequired': 'false'}},
                 {'J2CActivationSpec': {'destinationJndiName': 'dovetail/jms/CacheUpdateTopic', 'name': 'CacheUpdateTopic', 'scope': '/Cell:cell01/', 'jndiName': 'jms/CacheUpdateTopic'}},
                 {'J2EEResourceProperty': {'name': 'busName', 'scope': '/J2CActivationSpec:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'destinationType', 'scope': '/J2CActivationSpec:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'javax.jms.Topic', 'required': 'true'}},
                 {'J2EEResourceProperty': {'name': 'alwaysActivateAllMDBs', 'scope': '/J2CActivationSpec:CacheUpdateTopic/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2CActivationSpec': {'destinationJndiName': 'dovetail/jms/AsyncActionQueue', 'name': 'AsyncActionMDBeanActivation', 'scope': '/Cell:cell01/', 'jndiName': 'jms/AsyncActionQueue'}},
                 {'J2EEResourceProperty': {'name': 'busName', 'scope': '/J2CActivationSpec:AsyncActionMDBeanActivation/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'destinationType', 'scope': '/J2CActivationSpec:AsyncActionMDBeanActivation/', 'type': 'java.lang.String', 'value': 'javax.jms.Queue', 'required': 'true'}},
                 {'J2EEResourceProperty': {'name': 'alwaysActivateAllMDBs', 'scope': '/J2CActivationSpec:AsyncActionMDBeanActivation/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2CActivationSpec': {'destinationJndiName': 'dovetail/jms/AsyncActionQueue', 'name': 'IntFilterMDBeanActivation', 'scope': '/Cell:cell01/', 'jndiName': 'jms/IntFilterReleasePaymentsQueue'}},
                 {'J2EEResourceProperty': {'name': 'busName', 'scope': '/J2CActivationSpec:IntFilterMDBeanActivation/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'destinationType', 'scope': '/J2CActivationSpec:IntFilterMDBeanActivation/', 'type': 'java.lang.String', 'value': 'javax.jms.Queue', 'required': 'true'}},
                 {'J2EEResourceProperty': {'name': 'alwaysActivateAllMDBs', 'scope': '/J2CActivationSpec:IntFilterMDBeanActivation/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2CActivationSpec': {'destinationJndiName': 'dovetail/jms/ATRMatchPaymentsQueue', 'name': 'ATRMatchingMDBeanActivation', 'scope': '/Cell:cell01/', 'jndiName': 'jms/ATRMatchPaymentsQueue'}},
                 {'J2EEResourceProperty': {'name': 'busName', 'scope': '/J2CActivationSpec:ATRMatchingMDBeanActivation/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'destinationType', 'scope': '/J2CActivationSpec:ATRMatchingMDBeanActivation/', 'type': 'java.lang.String', 'value': 'javax.jms.Queue', 'required': 'true'}},
                 {'J2EEResourceProperty': {'name': 'alwaysActivateAllMDBs', 'scope': '/J2CActivationSpec:ATRMatchingMDBeanActivation/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2CActivationSpec': {'destinationJndiName': 'dovetail/jms/ReportGenerationMessageQueue', 'name': 'ReportGenerationMessageBeanActivation', 'scope': '/Cell:cell01/', 'jndiName': 'jms/ReportGenerationMessageQueue'}},
                 {'J2EEResourceProperty': {'name': 'busName', 'scope': '/J2CActivationSpec:ReportGenerationMessageBeanActivation/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'destinationType', 'scope': '/J2CActivationSpec:ReportGenerationMessageBeanActivation/', 'type': 'java.lang.String', 'value': 'javax.jms.Queue', 'required': 'true'}},
                 {'J2EEResourceProperty': {'name': 'alwaysActivateAllMDBs', 'scope': '/J2CActivationSpec:ReportGenerationMessageBeanActivation/', 'type': 'java.lang.Boolean', 'value': 'true', 'required': 'false'}},
                 {'J2CAdminObject': {'name': 'CacheUpdateTopic', 'scope': '/Cell:cell01/', 'jndiName': 'dovetail/jms/CacheUpdateTopic'}},
                 {'J2EEResourceProperty': {'name': 'BusName', 'scope': '/J2CAdminObject:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'TopicName', 'scope': '/J2CAdminObject:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'CacheUpdateTopic'}},
                 {'J2EEResourceProperty': {'name': 'TopicSpace', 'scope': '/J2CAdminObject:CacheUpdateTopic/', 'type': 'java.lang.String', 'value': 'CacheUpdateTopic'}},
                 {'J2CConnectionFactory': {'name': 'DovetailJMSXAQueueConnectionFactory', 'authDataAlias': 'evps-waymouthsNode/swaymouth', 'scope': '/Cell:cell01/', 'xaRecoveryAuthAlias': 'evps-waymouthsNode/swaymouth', 'jndiName': 'dovetail/jms/XAQueueConnectionFactory'}},
                 {'J2EEResourceProperty': {'name': 'BusName', 'scope': '/J2CConnectionFactory:DovetailJMSXAQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'TargetType', 'scope': '/J2CConnectionFactory:DovetailJMSXAQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'BusMember', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'TargetSignificance', 'scope': '/J2CConnectionFactory:DovetailJMSXAQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'Preferred', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'ConnectionProximity', 'scope': '/J2CConnectionFactory:DovetailJMSXAQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'Bus', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'ProviderEndpoints', 'scope': '/J2CConnectionFactory:DovetailJMSXAQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'localhost:8102:BootstrapBasicMessaging', 'required': 'false'}},
                 {'connectionPool': {'maxConnections': '100', 'scope': '/J2CConnectionFactory:DovetailJMSXAQueueConnectionFactory/'}},
                 {'J2CConnectionFactory': {'name': 'DovetailJMSQueueConnectionFactory', 'authDataAlias': 'evps-waymouthsNode/swaymouth', 'scope': '/Cell:cell01/', 'jndiName': 'dovetail/jms/QueueConnectionFactory'}},
                 {'J2EEResourceProperty': {'name': 'BusName', 'scope': '/J2CConnectionFactory:DovetailJMSQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'TargetType', 'scope': '/J2CConnectionFactory:DovetailJMSQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'BusMember', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'TargetSignificance', 'scope': '/J2CConnectionFactory:DovetailJMSQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'Preferred', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'ConnectionProximity', 'scope': '/J2CConnectionFactory:DovetailJMSQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'Bus', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'ProviderEndpoints', 'scope': '/J2CConnectionFactory:DovetailJMSQueueConnectionFactory/', 'type': 'java.lang.String', 'value': 'localhost:8102:BootstrapBasicMessaging', 'required': 'false'}},
                 {'connectionPool': {'maxConnections': '100', 'scope': '/J2CConnectionFactory:DovetailJMSQueueConnectionFactory/'}},
                 {'J2CConnectionFactory': {'name': 'DovetailJMSXATopicConnectionFactory', 'authDataAlias': 'evps-waymouthsNode/swaymouth', 'scope': '/Cell:cell01/', 'xaRecoveryAuthAlias': 'evps-waymouthsNode/swaymouth', 'jndiName': 'dovetail/jms/XATopicConnectionFactory'}},
                 {'J2EEResourceProperty': {'name': 'BusName', 'scope': '/J2CConnectionFactory:DovetailJMSXATopicConnectionFactory/', 'type': 'java.lang.String', 'value': 'DovetailSIBus'}},
                 {'J2EEResourceProperty': {'name': 'TargetType', 'scope': '/J2CConnectionFactory:DovetailJMSXATopicConnectionFactory/', 'type': 'java.lang.String', 'value': 'BusMember', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'TargetSignificance', 'scope': '/J2CConnectionFactory:DovetailJMSXATopicConnectionFactory/', 'type': 'java.lang.String', 'value': 'Preferred', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'ConnectionProximity', 'scope': '/J2CConnectionFactory:DovetailJMSXATopicConnectionFactory/', 'type': 'java.lang.String', 'value': 'Bus', 'required': 'false'}},
                 {'J2EEResourceProperty': {'name': 'ProviderEndpoints', 'scope': '/J2CConnectionFactory:DovetailJMSXATopicConnectionFactory/', 'type': 'java.lang.String', 'value': 'localhost:8102:BootstrapBasicMessaging', 'required': 'false'}},
                 {'connectionPool': {'maxConnections': '100', 'scope': '/J2CConnectionFactory:DovetailJMSXATopicConnectionFactory/'}}
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