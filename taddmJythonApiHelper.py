'''
Created on Aug 17, 2013

@author: moellerm
'''

import sys 
import java
import traceback
#import urllib
#import urllib2
import getopt
from getopt import GetoptError
import string
import os
import re
from xml.sax import *
import jarray

#import org.apache.log4j.xml.DOMConfigurator
from org.apache.log4j import *
from org.apache.log4j.xml import *

from java.lang import System
from java.lang import Class
from java.util    import HashMap
from java.lang import Boolean
from java.lang import Long
from java.io import File
from java.io import FileInputStream
from java.util import Properties


True = Boolean(1)
False = Boolean(0)


from com.collation.proxy.api.client import *
from com.collation.proxy.api.client.ApiException import *    

from com.collation.proxy.api.util import *      ##ModelObjectFactory
from com.ibm.cdb.api import *           ##ApiFactory


from com.collation.platform.model import  *
from com.collation.platform.model.topology.meta import  *
from com.collation.platform.model.discovery.agent import SensorConfiguration
from com.collation.platform.model.discovery.template import Template
from com.collation.platform.model.topology.sys import  *

###############################################################################
###############################################################################

##########################################
def getClassNames(modelObject):
    className = str(modelObject.__class__.canonicalName)
    longClass = className[0:len(className)-4]
    c = re.split("\.",longClass)
    shortClass = c[len(c)-1]
    
    return longClass, shortClass


def promptUser(question):
    global log
    doit = "" 
    deleteAll = False
    while not doit in ["y","n"]:
        answer = raw_input("\n" + question + " ? y(es)/a(ll)/n(o) ")
        if str(answer).lower() == "a":
            doit = "y" 
            deleteAll = True
            answer = "y"
        if not str(answer) == "":
            doit = string.lower(answer[0])
    if doit == "y":
        log.info("User confirmed action")
        return True, deleteAll
    elif doit == "n":
        log.info("User rejected action")
        return False, deleteAll




#class taddmJythonApiHelper():
#############################################################################
def getProgramName():
    global prog
    dirname, progname = os.path.split(sys.argv[0])    
    prog,ext = string.split(progname, ".",1)
    return prog,ext


#############################################################################
def getCollHome():
    global coll_home
    coll_home = System.getProperty("com.collation.home")
    return coll_home

#############################################################################
def connectToTaddm(host,port,user,password):
    global log

    if host == None:
        host = "localhost"
    if port == None:
        port = -1
    if user == None:
        user = "administrator"        
        
    #############################
    #  connect to TADDM
    #############################
    global api
    log.debug("Connecting to: " + str(host) + " on port " + str(port) )
    conn = ApiFactory.getInstance().getApiConnection(host, port, None, False)
    log.debug("Establishing session for user: " + str(user))
    sess = ApiFactory.getInstance().getSession(conn, user, password, ApiSession.DEFAULT_VERSION);
    api = sess.createCMDBApi()
    log.debug("Created api: " + str(api))

    return api

#######################################################################
def setupLog4jLogging(trace=False,debug=False):
    global log
    coll_home = getCollHome()
    prog,ext = getProgramName()
    #Load properties file in java.util.Properties
    propsFileName = coll_home+"/etc/collation.properties"
    inStream = FileInputStream(propsFileName)
    propFile = Properties()
    propFile.load(inStream) 
 
    # set properties for using the default TADDM log4j.xml file for logging
    if System.getProperty("com.collation.log.level") == None:
        System.setProperty("com.collation.log.level",propFile.getProperty("com.collation.log.level"))
    if System.getProperty("com.collation.log.filesize") == None:
        System.setProperty("com.collation.log.filesize",propFile.getProperty("com.collation.log.filesize"))
    if System.getProperty("com.collation.log.filecount") == None:
        System.setProperty("com.collation.log.filecount",propFile.getProperty("com.collation.log.filecount"))
    if System.getProperty("com.collation.log4j.servicename") == None:
        System.setProperty("com.collation.log4j.servicename","-" + prog)
    #if System.getProperty("groupMover.file.name") == None:    
    #    System.setProperty("groupMover.file.name",prog+".log")
    #if System.getProperty("com.collation.log.file.name") == None:    
    #    System.setProperty("com.collation.log.file.name",prog+".log")
        

    #Start logging
    
    # is a dedicated log4j.xml file provided (name is <prog>.xml
    log4jFile = []
    log4jFile.append("./"+prog+".xml")
    log4jFile.append(coll_home+"/etc/"+prog+".xml")
    log4jFile.append(coll_home+"/etc/log4j.xml")
    for logF in log4jFile: 
        if os.path.isfile(logF):
            log4j = logF
            break
    
    DOMConfigurator.configure(logF)
    log = Logger.getLogger("com.ibm.cdb.TivoliStdMsgLogger")

    layout = PatternLayout("%d{ISO8601} %X{service} [%t] %x %p %c{2} - %m\n")

    
    logfile = File(coll_home+"/log/"+prog+".log")
    
    fileAppender = FileAppender(layout, logfile.getAbsolutePath(), True);
    #log.removeAllAppenders();
    log.addAppender(fileAppender);
    if trace == True:
        consoleAppender = ConsoleAppender(layout,"System.out")
        log.addAppender(consoleAppender);
    



    if debug == True:
        loglevel = "DEBUG"
    else:
        loglevel = System.getProperty("com.collation.log.level")
        
    if loglevel == "INFO":
        log.setLevel(Level.INFO)
    elif loglevel == "DEBUG":
        log.setLevel(Level.DEBUG)
    elif loglevel == "TRACE":
        log.setLevel(Level.TRACE)
    elif loglevel == "ERROR":
        log.setLevel(Level.ERROR)



    return log




def init(trace=False,debug=False):
    global jython_home
    global python_home
    global log
    global prog
    
    coll_home = getCollHome()
    prog,ext = getProgramName()    
    #Load properties file in java.util.Properties
    propsFileName = coll_home+"/etc/collation.properties"
    inStream = FileInputStream(propsFileName)
    propFile = Properties()
    propFile.load(inStream) 
 
        
    System.setProperty("jython.home",coll_home + "/external/jython-2.1")
    System.setProperty("python.home",coll_home + "/external/jython-2.1")
    jython_home = System.getProperty("jython.home")


    log = setupLog4jLogging(trace,debug)
    
    return log, prog

