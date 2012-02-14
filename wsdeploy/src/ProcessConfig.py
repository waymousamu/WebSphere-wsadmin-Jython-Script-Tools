import re
import sys
#from xml.dom import javadom
from org.apache.log4j import *
from java.io import FileInputStream
from javax.xml.transform.stream import StreamSource
from javax.xml.transform.stream import StreamResult
from javax.xml.parsers import DocumentBuilderFactory
from org.xml.sax import InputSource
from java.io import StringReader
factory = DocumentBuilderFactory.newInstance()
builder = factory.newDocumentBuilder()

class ProcessConfig:

    logger = Logger.getLogger("ProcessConfig")

    def readConfig(self, fh=None, xml=None):
        self.fh = fh
        self.xml = xml
        self.tree = None
        self.doc = None
        self.cellTree = None
        if self.fh != None:
            self.logger.info("readConfig: processing xml file")
            self.logger.debug("readConfig: file %s " % fh)
            input = FileInputStream(self.fh)
            fhtree = builder.parse(input)
            self.tree = fhtree.getDocumentElement()
            self.cellTree = fhtree.getElementById('Cell')
        elif self.xml != None:
            self.logger.info("readConfig: processing xml String")
            str = StringReader(xml)
            strstrm = InputSource(str)
            self.doc = builder.parse(strstrm)
            self.tree = self.doc.getDocumentElement()
            self.cellTree = self.doc.getElementById('Cell')
        else:
            self.logger.error("readConfig: You did not supply a valid xml file handle or xml string to the readConfig method.")
            raise ProcessConfigException("readConfig: You did not supply a valid xml file handle or xml string to the readConfig method.")
        self.logger.debug("readConfig: self.tree = %s" % (self.tree))
        self.treeDict = []
        self.logger.debug("readConfig: processing base tree elements")
        self.logger.debug("readConfig: self.tree: %s " % self.tree)
        self.walkXMLTree(self.tree, 0)
        self.logger.debug("readConfig: self.treeDict = %s" % (self.treeDict))
        return self.treeDict

    def walkXMLTree(self, node, level):
        self.node=node
        self.logger.debug("walkXMLTree: level=%s" % (level))
        if self.node.getNodeType() == 1:
            tag = self.node.getTagName()
            self.logger.debug("walkXMLTree: tag=%s " % tag)
            self.elementDict = {}
            if self.node.hasAttributes():
                self.attrDict = {}
                attr = self.node.getAttributes()
                self.logger.debug("walkXMLTree: attr=%s " % attr)
                self.logger.debug("walkXMLTree: length=%s " % attr.getLength())
                for i in range(attr.getLength()):
                    itemnode = attr.item(i)
                    self.logger.debug("walkXMLTree: attribute=%s, value=%s" % (itemnode.getNodeName(), itemnode.getNodeValue()))
                    self.logger.debug("updating the tmpDict")
                    self.attrDict[itemnode.getNodeName()] = itemnode.getNodeValue()
                self.logger.debug("walkXMLTree: self.attrDict= %s" % self.attrDict)
                if self.node.getParentNode().getNodeType() == 1:
                    self.parTag = self.node.getParentNode().getTagName()
                    self.logger.debug("walkXMLTree: self.parTag = %s" % self.parTag)
                    self.parAttr = self.node.getParentNode().getAttributes()
                    if self.parAttr.getNamedItem('name'):
                        self.scopeItem = self.parAttr.getNamedItem('name')
                        self.scopeTag = self.scopeItem.getNodeValue()
                        self.logger.debug("walkXMLTree: 'name' = %s" % self.scopeTag)
                    else:
                        self.logger.warn("walkXMLTree: No 'name' tag in element %s" % self.parTag)
                        self.parNode = self.node.getParentNode()
                        self.greatParNode = self.parNode.getParentNode()
                        self.greatParAttr = self.greatParNode.getAttributes()
                        self.scopeItem = self.greatParAttr.getNamedItem('name')
                        self.scopeTag = self.scopeItem.getNodeValue()
                        self.parTag = self.greatParNode.getTagName()
                        self.logger.debug("walkXMLTree: 'name' = %s" % self.scopeTag)
                    if self.parTag != 'env' and tag != 'dmgr':
                        self.attrDict['scope'] = ("/%s:%s/" % (self.parTag, self.scopeTag))
                    self.logger.debug("walkXMLTree: self.attrDict = %s" % self.attrDict)
                self.elementDict[tag] = self.attrDict
                self.treeDict.append(self.elementDict)
                self.logger.debug("walkXMLTree: self.treeDict = %s" % self.treeDict)
            if self.node.hasChildNodes():
                children = self.node.getChildNodes()
                self.logger.debug("walkXMLTree: %s children found" % children.getLength())
                for i in range(children.getLength()):
                    child = children.item(i)
                    self.logger.debug("walkXMLTree: child: %s" % child)
                    if child.getNodeType() < 2:
                        self.logger.debug("walkXMLTree: processing child %s " % child.getTagName())
                        self.walkXMLTree(child, level + 1)

        #self.parTag=parentTag
        #self.parAtt=parentAttr
        #if self.node.getParentNode().getNodeType() < 9:
        #    self.parTag = self.node.getParentNode()
        #    self.logger.debug("walkXMLTree: parTag = %s" % self.parTag)
        #    self.logger.debug("walkXMLTree: parTag node type = %s" % self.parTag.getNodeType())
        #    if self.parTag.getAttributes():
        #        self.parAtt = self.parTag.getAttributes()
        #        self.logger.debug("walkXMLTree: parAtt = %s" % (self.parAtt))
        #
        #else:
        #    self.logger.debug("walkXMLTree: this is the root tag.")
        #isChildTag = isChild
        #self.logger.debug("walkXMLTree: isChildTag = %s" % (isChildTag))
        #if self.node.hasChildNodes():
        #    children = self.node.getChildNodes()
        #    self.logger.debug("walkXMLTree: %s children found" % children.getLength())
        #    for i in range(children.getLength()):
        #        child = children.item(i)
        #        self.logger.debug("walkXMLTree: child: %s" % child)
        #        if child.getNodeType() < 2:
        #            self.logger.debug("walkXMLTree: processing child %s " % child.getTagName())
        #            self.walkXMLTree(child, level + 1, self.node.getTagName(), self.node.getAttributes(), 0)
        #else:
        #    if isChild == 0:
        #        self.tmpList = []
        #        self.logger.debug("walkXMLTree: adding child attrs to parent node")
        #        if self.node.hasAttributes():
        #            attr = self.node.getAttributes()
        #            self.logger.debug("walkXMLTree: attr=%s " % attr)
        #            self.logger.debug("walkXMLTree: length=%s " % attr.getLength())
        #            for i in range(attr.getLength()):
        #                itemnode = attr.item(i)
        #                self.logger.debug("walkXMLTree: attribute=%s, value=%s" % (itemnode.getNodeName(), itemnode.getNodeValue()))
        #                self.tmpList.append("%s %s" % (itemnode.getNodeName(), itemnode.getNodeValue()))
        #        self.logger.debug("walkXMLTree: tmpList= %s" % self.tmpList)
        #        parDict = {}
        #        parDict[tag] = self.tmpList
        #        self.logger.debug("walkXMLTree: parDict = %s " % parDict)
        #        self.treeDict[self.parTag] = parDict

class ProcessConfigException(Exception):
    """ General exception method for class. """
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return repr(self.val)
