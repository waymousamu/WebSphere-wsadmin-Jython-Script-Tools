Hello and welcome to the wsdeploy project.

This project is the result of the cumulative knowlege I have gained over the last 9 years of WebSphere Administration.

It's purpose is to provide a toolset for configuration management of WebSphere environments.

The basic design principle of the tool is that there are only three kinds of data type in a WebSsphere configuration xml file: 
the object, property sets and properties.

Each of these basic types can be created, deleted and modified using the AdminConfig.create or AdmiConfig.modify objects in the
WebSphere Jython libraries.  The implication of this is that you can do anything you like in the WebSphere configuration 
using just these two commands, nothing else.  The only requirement is that you privide the command with a properly formatted
string containing valid data.  As such, you can avoid having to write different bits of code to create different WebSphere 
configuration objects.  All you really need is a configuration file, a class to process that configuration file into a list of 
valid AdminConfig command strings, and a class to execute those commands in the sequence you want.

This means a bunch of things are possible:
*You can write different configuration file processors to suite the requirements of your client site, extending the basic xml one I have written
*You can write different command processors to support different version of WebSphere, extending the basic class tested against WebSphere 6.1
*When you need to change the logic of your script, you do so by changing the configuration file, not the classes themselves

The whole idea is that configuration files are the things that are complicated and these should be managed in a source control system.

the classes that actually do that work shouldn't need to change all that much to cater for new requirements.

The development principle is that this is a test driver project.  Unit tests are created for a sample environment which contains all sorts
of WebSphere objects, as well as tests for particular types of objects such as datasources, aliases and such like.

The operation principle is that a WebSphere administrator should be able to run this tool usiung a configuration file and produce a report
containing the differences between the target environment and the configuration file.  This is the default to read-only mode.  If the administrator
runs the tool in WRITE mode then the configuration values in the configuration file will be written to the remote WebSphere configuration.

The idea of this is that you can audit WebSphere environments for compliance to a particular configuration file, or just overwrite what's actually
deployed in WebSphere.  Good init?

QUICKSTART

1.  Copy the conf/sample.xml and rename it to something meaningful for your target environment, for example foo.xml.
2.  Edit the foo.xml configuration file and adjust the values.  Use ENTITY tags as variable to reduce typing and making updates easier.
3.  Edit the wsdeploy.sh or wsdeploy.bat to match the value of your local WebSphere installation.  The tool requires a WebSphere 
installation to work, although this can be a central server or your own workstation.
4.  Run the wsdeploy.sh or wsdeploy.bat file.  Format is as follows:

wsdeploy.bat <hostname> <port> <env> <action>

For example, to run the tool against the foo environment in read-only mode where the deployment manager is running on host bobroberts.com
with a soap port of 2089:

wsdeploy.bat bobroberts.com 2089 foo R

If the setup for the batch file is all correct then you should see the tool run and produce a list of things missing from the target
environment.  To update the target environment:

wsdeploy.bat bobroberts.com 2089 foo W

You should now see the tool run and it will report the create and updates it is making.  The updates are at attribute level so that the tool
should only change things that are actually different, not the entire parent object if it already exists.

UNIT TESTING and CONTRIBUTION

Unit test scripts are provided.  These test that the configuration file produces a useful list of commands, as well as exzecuting those commands on the remote system.

Please feel free to add your own unit tests.  Speak to me if you want to contribute and set up configuration for new types of WebSphere object.

FUTURE RELEASES

Now that I have the basic configuration stuff figured out there are two things I want to do next.

Firstly, I haven't added support for application deployment yet.  this will involve using the AdminApp commands and I need to figure out how I want 
to set it up in my xml configuration file.

Secondly, I want to create a class for exporting the configuration from an existing WebSphere target environment.  The idea is to interrogate
the environment and generate a configuration file that can be edited for reuse.  This is a cloning tool.  I have some good sample code 
I borrowed from an IBM java class that I want to use as a starting point.  It's probably more important to get this feature working first then 
worry about application deployment later so I'll start there.

WHO AM I?

Samuel Waymouth

Linked In Profile: http://www.linkedin.com/pub/sam-waymouth/1/135/6b6

