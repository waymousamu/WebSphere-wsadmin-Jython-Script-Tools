try:
    import AdminConfig
    import AdminControl
    import AdminApp
    import AdminTask
    import Help
except:
    pass

import re
import sys
from org.apache.log4j import *
class ProcessCommands:

    logger = Logger.getLogger("ProcessCommands")

    def generateCommands(self, cmdList=None, action=None):
        self.action = action
        self.cmdList = cmdList
        self.logger.info("generateCommands: processing command dictionary.")
        if self.cmdList == None:
            self.logger.error("generateCommands: No dictionary was passed to the generateCommands method")
            raise ProcessCommandException("No dictionary was passed to the generateCommands method")
        self.logger.debug("generateCommands: self.cmdDict = %s " % self.cmdList)
        cellList = []
        dmgrList = []
        #envList = []
        #clusterList = []
        #clusterMemberList = []
        #serverList = []
        tempCmdList = []
        clusterCmdList = []
        clusterMemberCmdlist = []

        for item in self.cmdList:
            self.cmdDict = item
            self.logger.debug("generateCommands: item = %s" % item)
            for k, v in self.cmdDict.items():
                self.logger.debug("generateCommands: k = %s" % k )
                self.logger.debug("generateCommands: v = %s" % v )
                if k == "Cell":
                    self.logger.debug("generateCommands: block = Cell")
                    if AdminControl.getCell() != v['name']:
                        self.logger.error("generateCommands: Cell name %s != %s.  You may have connected to the wrong WebSphere environment or the name of the cell in the configuration xml is not correct." % (AdminControl.getCell(),v['name']))
                        raise ProcessCommandException("Cell name %s != %s.  You may have connected to the wrong WebSphere environment or the name of the cell in the configuration xml is not correct." % (AdminControl.getCell(),v['name']))
                elif k == "ServerCluster":
                    self.logger.debug("generateCommands: block = ServerCluster")
                    scopeStr = ("AdminConfig.getid('%s')" % (v['scope']))
                    clusterStr = ("'[[name %s]]'" % (v['name']))
                    command = ("AdminConfig.create('%s', (%s), %s)" % (k, scopeStr, clusterStr))
                    self.logger.debug("generateCommands: command = %s " % command)
                    clusterCmdList.append(command)
                elif re.search("ClusterMember", k):
                    self.logger.debug("generateCommands: block = ClusterMember")
                    scopeStr = ("AdminConfig.getid('%s')" % (v['scope']))
                    nodeStr = ("AdminConfig.getid('/Node:%s/')" % (v['nodeName']))
                    clusterMemberName = ("[['memberName', '%s']]" % (v['memberName']))
                    command = ("AdminConfig.createClusterMember((%s), (%s), %s)" % (scopeStr, nodeStr, clusterMemberName))
                    self.logger.debug("generateCommands: command = %s " % command)
                    clusterMemberCmdlist.append(command)
                elif k == "Server":
                    self.logger.debug("generateCommands: block = Server")
                    self.processServer(k=k, v=v)
                elif k == "JDBCProvider":
                    self.logger.debug("generateCommands: block = JDBCProvider")
                    self.processConfigItem(k=k, v=v)
                elif k == "DataSource" or k == "MQQueueConnectionFactory" or k == 'MQQueue':
                    self.logger.debug("generateCommands: block = DataSource or MQQueueConnectionFactory")
                    t=None
                    if k == 'DataSource':
                        if v['providerType'] == 'Oracle JDBC Driver (XA)':
                            t = AdminConfig.listTemplates('DataSource', "Oracle JDBC Driver XA DataSource")
                        else:
                            t = AdminConfig.listTemplates('DataSource', "Oracle JDBC Driver DataSource")
                    elif k == 'MQQueueConnectionFactory':
                        t = AdminConfig.listTemplates('MQQueueConnectionFactory', 'First Example WMQ QueueConnectionFactory')
                        v['scope'] = ('%sJMSProvider:WebSphere MQ JMS Provider/' % v['scope'])
                    elif k == 'MQQueue':
                        t = AdminConfig.listTemplates('MQQueue', 'Example.JMS.WMQ.Q1')
                        v['scope'] = ('%sJMSProvider:WebSphere MQ JMS Provider/' % v['scope'])
                    self.processConfigItem(k=k, v=v, t=t)
                elif k == "J2EEResourceProperty":
                    self.logger.debug("generateCommands: block = J2EEResourceProperty")
                    self.processPropertySet(k=k, v=v)
                elif k == "JAASAuthData":
                    self.logger.debug("generateCommands: block = JAASAuthData")
                    self.processSecrurity(k=k, v=v)
                elif k == "ConnectionPool" or k == "connectionPool" or k == "sessionPool":
                    self.logger.debug("generateCommands: block = ConnectionPool")
                    self.processNestedAttribute(k=k, v=v)
                elif k == "JavaVirtualMachine" or k == "ProcessExecution":
                    self.logger.debug("generateCommands: block = JavaVirtualMachine or ProcessExecution")
                    self.processNestedAttribute(k=k, v=v)
                elif k == "env" or k == "Node" or k == 'dmgr' or k == 'JMSProvider':
                    self.logger.debug("generateCommands: block = env or Node or dmgr")
                    '''Ignore a tag'''
                    self.logger.info("generateCommands: ignoring tag %s" % k )
                else:
                    '''Throw an exception if the tag is unknown'''
                    self.logger.error("generateCommands: %s is an unknown key, it will be ignored." % k)
                    raise ProcessCommandException("%s is an unknown key, it will be ignored." % k)

    def processServer(self, k=None, v=None):
        self.logger.debug("processServer: key=%s, value=%s" % (k, v))
        if k and v != None:
            self.validateScope(v, 'processServer')
            srv = AdminConfig.getid(v['scope']+"%s:%s/" % (k, v['name']))
            self.logger.debug("processServer: srv=%s " % srv)
            if srv == "":
                self.logger.info("processServer: creating server %s" % v['name'])
            else:
                srvObj = AdminConfig.getObjectName(srv)
                self.logger.debug("processServer: srvObj %s" % srvObj)
                ptype = AdminControl.getAttribute(srvObj, 'processType')
                self.logger.debug("processServer: ptype %s" % ptype)
                if ptype != 'UnManagedProcess':
                    self.logger.info("processServer: This is a Network Deployment Profile so this command will run.")
                else:
                    self.logger.warn("processServer: This is not a Network Deployment Profile so this command won't be run.  Use the manageprofiles too to create servers." )
                    #raise ProcessCommandException("This is not a Network Deployment Profile so this command won't be run.  Use the manageprofiles too to create servers.")
                #end-if
            #end-if
        else:
            self.logger.error("processServer: key and value parameters were not suppled to the method.")
            raise ProcessCommandException("key and value parameters were not suppled to the method.")
        #end-if

    def processNestedAttribute(self, k=None, v=None):
        self.logger.debug("processNestedAttribute: key=%s, value=%s" % (k, v))
        if k and v != None:
            self.validateScope(v, 'processNestedAttribute')
            attribute = None
            if re.match("[a-z]", k):
                self.logger.debug("processNestedAttribute: %s is a nested property." % k)
                attribute=AdminConfig.showAttribute(AdminConfig.getid(v['scope']), k)
            else:
                attribute = AdminConfig.list('%s' % k, AdminConfig.getid(v['scope']))
                self.logger.debug("processNestedAttribute: %s is an object." % k)
            for (k2, v2) in v.items():
                if k2 != "scope":
                    actualValue=AdminConfig.showAttribute(attribute, k2)
                    if actualValue != v2:
                        if self.action == 'W':
                            self.logger.info("processNestedAttribute: modifying %s:%s=%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), k2, v2))
                            self.logger.debug("processNestedAttribute: command=AdminConfig.modify(attribute, [[%s, %s]])" % (k2, v2))
                            AdminConfig.modify(attribute, [[k2, v2]])
                        else:
                            self.logger.warn("processNestedAttribute: audit failure %s:%s, actual=%s config=%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), k2, actualValue, v2))
                        #end-if
                    else:
                        self.logger.debug("processNestedAttribute: ignoring %s:%s=%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), k2, v2))
                    #end-if
                #end-if
            #end-for
        else:
            self.logger.error("processNestedAttribute: key and value parameters were not suppled to the method.")
            raise ProcessCommandException("key and value parameters were not suppled to the method.")
        #end-if

    def processConfigItem(self, k=None, v=None, t=None):
        self.logger.debug("processConfigItem: key=%s, value=%s" % (k, v))
        if k and v != None:
            self.validateScope(v, 'processConfigItem')
            self.logger.debug("processConfigItem: scope=%s " % AdminConfig.getid(v['scope']))
            obj = AdminConfig.getid('%s%s:%s' % (v['scope'], k, v['name']))
            self.logger.debug("processConfigItem: obj=%s " % obj)
            if obj == "":
                attrList = []
                for key in v.keys():
                    if key != 'scope':
                        attrList.append([key, v[key]])
                    #end-if
                #end-for
                self.logger.debug("processConfigItem: attrList=%s" % attrList)
                if t == None:
                    if self.action == 'W':
                        self.logger.info("processConfigItem: creating %s:%s:%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), k, v['name']))
                        self.logger.debug("processConfigItem: command=AdminConfig.create(%s, %s, %s)" % (k, AdminConfig.getid(v['scope']), attrList))
                        AdminConfig.create(k, AdminConfig.getid(v['scope']), attrList)
                    #end-if
                else:
                    if self.action == 'W':
                        self.logger.info("processConfigItem: creating %s:%s:%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), k, v['name']))
                        self.logger.debug("processConfigItem: t=%s" % t)
                        self.logger.debug("processConfigItem: command=AdminConfig.createUsingTemplate(%s, %s, %s, %s)" % (k, AdminConfig.getid(v['scope']), attrList, t))
                        AdminConfig.createUsingTemplate(k, AdminConfig.getid(v['scope']), attrList, t)
                    #end-if
                #end-if
            #end-if
            else:
                self.logger.debug("processConfigItem: need to add the modify code here :-)")
                for key in v.keys():
                    if key != 'scope':
                        actual = AdminConfig.showAttribute(obj, key)
                        self.logger.debug("processConfigItem: attribute=%s, value=%s" % (key, actual))
                        if actual != v[key]:
                            if self.action == 'W':
                                self.logger.debug("processConfigItem: updating actual=%s to %s" % (actual,v[key]))
                                self.logger.debug("processConfigItem: command=AdminConfig.modify(%s, [['%s', '%s']])" % (obj, key, v[key]))
                                AdminConfig.modify(obj, [[key, v[key]]])
                            else:
                                self.logger.warn("processPropertySet: audit failure %s:%s, actual=%s config=%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), (AdminConfig.showAttribute(obj, 'name')), (AdminConfig.showAttribute(obj, key)), v[key]))
                            #end-if
                        #end-if
                    #end-if
                #end-for
            #end-if
        else:
            self.logger.error("processConfigItem: key and value parameters were not suppled to the method.")
            raise ProcessCommandException("key and value parameters were not suppled to the method.")
        #end-if

    def processPropertySet(self, k=None, v=None):
        '''Used to process property sets such as J2EEResourceProperties'''
        self.logger.debug("processPropertySet: key=%s, value=%s" % (k, v))
        if k and v != None:
            self.validateScope(v, 'processPropertySet')
            self.propSet=AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'propertySet')
            self.logger.debug("processPropertySet: propSet=%s " % self.propSet)
            self.propList = AdminConfig.list(k, AdminConfig.getid(v['scope'])).split('\r\n')
            for key in v.keys():
                if key == 'name':
                    self.logger.debug("processPropertySet: key=%s, value=%s" % (key, v[key]))
                    itemFound="1"
                    for item in self.propList:
                        self.logger.debug("processPropertySet: name=%s" % AdminConfig.showAttribute(item, 'name'))
                        if AdminConfig.showAttribute(item, 'name') == v[key]:
                            self.logger.debug("processPropertySet: actual name=%s, value=%s" % (AdminConfig.showAttribute(item, 'name'), AdminConfig.showAttribute(item, 'value')))
                            self.logger.debug("processPropertySet: config name=%s, value=%s" % (v['name'], v['value']))
                            if AdminConfig.showAttribute(item, 'value') != v['value']:
                                if self.action == 'W':
                                    self.logger.info("processPropertySet: modifying %s:%s:%s=%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), AdminConfig.showAttribute(item, 'name'), 'value', v['value']))
                                    self.logger.debug("processPropertySet: command=AdminConfig.modify(%s, [[%s, %s]])" % (item, 'value', v['value']))
                                    AdminConfig.modify(item, [['value', v['value']]])
                                else:
                                    self.logger.warn("processPropertySet: audit failure %s:%s, actual=%s config=%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), (AdminConfig.showAttribute(item, 'name')), AdminConfig.showAttribute(item, 'value'), v['value']))
                                #end-if
                            else:
                                self.logger.debug("processPropertySet: ignoring %s %s" % (AdminConfig.showAttribute(item, 'name'), AdminConfig.showAttribute(item, 'value')))
                            #end-if
                            itemFound = "0"
                            break
                        #end-if
                    #end-for
                    if itemFound == "1":
                        self.logger.info("processPropertySet: creating %s:%s:%s=%s" % (AdminConfig.showAttribute(AdminConfig.getid(v['scope']), 'name'), AdminConfig.showAttribute(item, 'name'), 'value', v['value']))
                        self.logger.debug("processPropertySet: command=AdminConfig.create(k, self.propSet, [['name', '%s'],['type', '%s'],['value', '%s'],['required', '%s'])" % (v[key], v['type'], v['value'], v['required']))
                        AdminConfig.create(k, self.propSet, [['name', v[key]],['type', v['type']],['value', v['value']],['required', v['required']]])
                    #end-if
                #end-if
            #end-for
        else:
            self.logger.error("processPropertySet: key and value parameters were not suppled to the method.")
            raise ProcessCommandException("key and value parameters were not suppled to the method.")
        #end-if

    def processSecrurity(self, k=None, v=None):
        '''Used to process security properties'''
        self.logger.debug("processSecrurity: key=%s, value=%s" % (k, v))
        if k and v != None:
            self.validateScope(v, 'processPropertySet')
            self.jaasAuthDataList = AdminConfig.list(k, AdminConfig.getid('%sSecurity:/' % v['scope'])).split('\r\n')
            self.logger.debug("processSecrurity: jaasAuthDataList=%s"% self.jaasAuthDataList)
            for key in v.keys():
                if key == 'alias':
                    self.logger.debug("processSecrurity: key=%s, value=%s" % (key, v[key]))
                    itemFound="1"
                    self.logger.debug("processSecrurity: items length is=%s" % len(self.jaasAuthDataList))
                    for item in self.jaasAuthDataList:
                        self.logger.debug("processSecrurity: item=%s" % item)
                        if item != "":
                            self.logger.debug("processSecrurity: name=%s" % AdminConfig.showAttribute(item, 'alias'))
                            if AdminConfig.showAttribute(item, 'alias') == v[key]:
                                self.logger.debug("processSecrurity: checking alias %s" % AdminConfig.showAttribute(item,'alias'))
                                for key in v.keys():
                                    if key != 'scope':
                                        self.logger.debug("processSecrurity: key=%s" % key)
                                        if AdminConfig.showAttribute(item, key) != v[key]:
                                            self.logger.debug("processSecrurity: alias:%s, key=%s, actual=%s, config=%s" % (AdminConfig.showAttribute(item,'alias'), key, AdminConfig.showAttribute(item, key), v[key]))
                                            if self.action == 'W':
                                                self.logger.info("processSecrurity: modifying %s:%s=%s" % (AdminConfig.showAttribute(item,'alias'), key, v[key]))
                                                self.logger.debug("processSecrurity: command=AdminConfig.modify(%s, [[%s, %s]])" % (AdminConfig.showAttribute(item,'alias'), key, v[key]))
                                                AdminConfig.modify(item, [[key, v[key]]])
                                            else:
                                                self.logger.warn("processSecrurity: audit failure %s:, actual=%s config=%s" % (AdminConfig.showAttribute(item,'alias'), AdminConfig.showAttribute(item, key), v[key]))
                                            #end-if
                                        #end-if
                                    #end-if
                                #end-for
                                itemFound = "0"
                                break
                            #end-if
                        #end-if
                    #end-for
                    if itemFound == "1":
                        self.logger.info("processSecrurity: creating %s:%s" % (k, v['alias']))
                        attrList = []
                        for key in v.keys():
                            if key != 'scope':
                                attrList.append([key, v[key]])
                        self.logger.debug("processSecrurity: command=AdminConfig.create(%s, %s, %s)" % (k, AdminConfig.getid('%sSecurity:/' % v['scope']), attrList))
                        AdminConfig.create(k, AdminConfig.getid('%sSecurity:/' % v['scope']), attrList)
                    #end-if
                #end-if
            #end-for
        else:
            self.logger.error("processPropertySet: key and value parameters were not suppled to the method.")
            raise ProcessCommandException("key and value parameters were not suppled to the method.")
        #end-if

    def validateScope(self, valueDict=None, method=None):
        self.valueDict=valueDict
        self.method=method
        self.scope = AdminConfig.getid(valueDict['scope'])
        if self.scope == "":
            self.logger.error("validateScope:%s Scope %s does not exist.  Check the scope in the configuration file." % (self.method, valueDict['scope']))
            raise ProcessCommandException("Scope %s does not exist.  Check the scope in the configuration file." % valueDict['scope'])

class ProcessCommandException(Exception):
    """ General exception method for class. """
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return repr(self.val)
