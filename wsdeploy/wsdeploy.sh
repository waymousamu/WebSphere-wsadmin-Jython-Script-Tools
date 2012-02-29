#!/bin/sh
set -xv
WSDEPLOY_HOME=/opt/ibm/wsdeploy
WSDEPLOY_LIB=${WSDEPLOY_HOME}/lib
WSDEPLOY_CONF=${WSDEPLOY_HOME}/conf
WSDEPLOY_SRC=${WSDEPLOY_HOME}/src
WSADMIN_CLASSPATH=${WSDEPLOY_LIB}/log4j-1.2.15.jar:${WSDEPLOY_CONF}:${WSDEPLOY_LIB}/jython.jar
WAS_HOME=/opt/ibm/websphere7
WAS_HOST=altus3400.dovetail.net
WAS_PORT=8881
ENV=base02
ACTION=W
${WAS_HOME}/bin/wsadmin.sh -lang jython -host ${WAS_HOST} -port ${WAS_PORT} -wsadmin_classpath ${WSADMIN_CLASSPATH} -f ${WSDEPLOY_SRC}/wsdeploy.py ${ENV} ${ACTION}