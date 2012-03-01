SET WSDEPLOY_HOME=C:/development/wsdeploy/wsdeploy
SET WSDEPLOY_LIB=%WSDEPLOY_HOME%/lib
SET WSDEPLOY_CONF=%WSDEPLOY_HOME%/conf
SET WSDEPLOY_SRC=%WSDEPLOY_HOME%/src
SET WAS_HOME=C:/ibm/websphere7_64
SET WAS_HOST=%1
SET WAS_PORT=%2
SET ENV=%3
SET ACTION=%4
%WAS_HOME%/bin/wsadmin.bat -lang jython -host %WAS_HOST% -port %WAS_PORT% -wsadmin_classpath "%WSDEPLOY_LIB%/log4j-1.2.15.jar;%WSDEPLOY_CONF%" -f %WSDEPLOY_SRC%/wsdeploy.py %ENV% %ACTION%