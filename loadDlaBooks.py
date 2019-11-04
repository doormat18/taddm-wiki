#!/usr/bin/env ../../bin/jython_coll_253

############### Begin Standard Header - Do not add comments here ###############
#
# File:	 %W%
# Version:  %I%
# Modified: %G% %U%
# Build:	%R% %L%
#
# Licensed Materials - Property of IBM
#
# Restricted Materials of IBM
#
# 5724-N55
#
# (C) COPYRIGHT IBM CORP. 2007.  All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
############################# End Standard Header ##############################

#
# It is assumed that this script is located in a directory
# which is not part of the standard TADDM directory structure.
# This minimizes the risk of removing the script inadvertantly as part of an upgrade.
#
# To launch the TADDM jython environment, the first line should point to the
# jython_coll script in the $COLLATION_HOME/bin directory.
# Use the relative location of the directory to initialize the environment.
#
# If for example, the script is stored in $COLLATION_HOME/usr/bin
# use the following path to launch the jython interpreter and initiate the TADDM environment
#	   ../../dist/bin/jython_coll_253
#
# If the script is stored in $COLLATION_HOME/bin
# use the following path to launch the jython interpreter and initiate the TADDM environment
#	   ./jython_coll_253
#
import sys
import traceback
import getopt
import os
import platform
import inspect
import socket
import string
from decimal import Decimal
#import csv
#import math
import datetime
from datetime import *
import time
from time import strftime, localtime
from math import *
import re
#import random
#from random import  *
#import threading
import hashlib
import array
from symbol import exec_stmt
from sensorhelper import coll_home
current_milli_time = lambda: int(round(time.time() * 1000))


import ftplib
from ftplib import *


import subprocess
from subprocess import Popen, PIPE
from getopt import GetoptError

from org.apache.log4j import *
from org.apache.log4j.xml import *

import java.lang
from java.lang import System
from java.io import File
from java.io import FileInputStream
from java.util import Properties
#from java.sql import DriverManager
#from java.sql import Statement
#from java.sql import SQLException
from java.security import *
'''
from com.collation.platform.model.topology import enums as enums
from com.collation.platform.model.topology.enums import *
'''
from random import *
from com.ibm.cdb.platform.ip import IPv4Utils
import com.collation.platform.model.discovery
from com.collation.platform.model.discovery import *
from com.collation.platform.model.discovery.scope import *
from com.ibm.cdb.topomgr import TopologyManagerFactory
from com.ibm.cdb.topomgr import TopomgrProps
from com.collation.proxy.api.util import ModelObjectFactory
from com.collation.proxy.api.util import ModelObjectFactory


from com.collation.platform.util import *




from java.lang import System
from java.lang import Class
from java.util	import HashMap
from java.lang import Boolean
from java.lang import Long
from java.io import File
from java.io import FileInputStream
from java.util import Properties




from com.collation.proxy.api.client import *
from com.collation.proxy.api.client.ApiException import *

from com.collation.proxy.api.util import *	  ##ModelObjectFactory
from com.ibm.cdb.api import *		   ##ApiFactory


from com.collation.platform.model import  *
from com.collation.platform.model.topology.meta import  *
from com.collation.platform.model.discovery.agent import SensorConfiguration
from com.collation.platform.model.discovery.template import Template
from com.collation.platform.model.topology.sys import  *
from com.collation.platform.model.discovery.profile import *

from com.collation.platform.model.topology.service import  *
from com.collation.platform.model.util.openid import OpenId
from com.collation.platform.model.util.einst import ExtendedInstanceData
from com.collation.platform.model.util.ea import ExtendedAttributesData

from com.collation.platform.model.topology.customCollection import *
from com.collation.platform.model.topology.simple import *

from com.collation.platform.model.discovery.auth import *
from com.collation.discover.manager import *
######################################################################################################
# enumerations
######################################################################################################
from com.collation.platform.model.topology.enums import  IpAddressTypeEnum

#collHome = System.getProperty("com.collation.home")
#newJythonHome = collHome + "osgi/plugins/com.ibm.cdb.core.jython253_2.5.3"
#if os.path.isdir(newJythonHome):
#	System.setProperty("jython.home",newJythonHome)
#	System.setProperty("python.home",newJythonHome)
#	jython_home = System.getProperty("jython.home")
#	sys.path.append(jython_home + "/Lib")

from com.ibm.cdb.platform.ip import IPv4Utils
from com.ibm.cdb.platform.ip import IPUtils
from com.ibm.cdb.util import IPAddressType
from com.ibm.cdb.util import IPFormatException




#######################################################################################################
#######################################################################################################
class Usage(Exception):
	def __init__(self, msg):
		if not msg == "help":
			log.error("\nINVOCATION ERROR:\t" + msg)
			print "\n" + 150*"!"
			print "\t" + msg
			print 150*"!" + "\n"
		show_help()

		raise SystemExit(0)


#######################################################################################################
#######################################################################################################
class Fatal(Exception):
	def __init__(self,msg=None):
		print 150*"*"
		print "AN ERROR OCCURED:"
		print msg
		print 150*"*"

		self.rc = 8
		self.msg = msg

		raise Quit(self.rc)


#######################################################################################################
#######################################################################################################
class Quit(Exception):
	def __init__(self,rc=0,msg=None):

		self.rc = rc
		self.msg = msg


#######################################################################################################
#######################################################################################################
class Exit(Exception):
	def __init__(self, rc=0,msg=None):

		self.msg = msg
		self.rc = rc

	def leave(self):
		raise SystemExit()

#######################################################################################################
#######################################################################################################
class SystemExit(Exception):
	def __init__(self, rc=0,msg=None):

		self.msg = msg
		self.rc = rc
		sys.exit()

#	def leave(self):
#		sys.exit()


##--------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------

###########################################################################
###########################################################################
def show_help():


	if "WINDOWS" in java.lang.System.getProperty("os.name").upper():
		ext1 = "bat"
	else:
		ext1 = ext


	delim = 3*" "
	l0 = delim  + "%-s"
	l1 = 10*" " + "%-30s%s"
	l2 = 15*" " + "%-50s%s"
	l3 = 20*" " + "%-30s%s"
	l4 = 70*" " + "%-10s%s"


	print l0 % ("The " + prog + " utility downloads DLA books from an ftp site, and loads component information represented in the books into the TADDM database.")
	print l0 % ("Custom properties can be specified in a properties file or provided as invocation arguments to control the behavior.")
	print ""
	print l0 % ("If generation of delta DLA books is enabled, the last processed DLA books are stored locally in the 'current' subdirectory ")
	print l0 % ("of the directory specified by the targetDirectory argument.")   
	print ""
	print l0 % ("Messages from the utility are logged in the " + coll_home +  os.sep + "log" + os.sep + prog + ".log file")
	print ""
	print l0 % ("INVOCATION:")
	print ""
	print l1 %  (prog + "." + ext1,"[ACTION OPTIONS] [FTP OPTIONS] [PROCESSING OPTIONS] [MISC OPTIONS]")
	print ""
	print l1 % ("[ACTION OPTIONS]","-" + inputOpts["action="][0] + "|--action <action>  -" + inputOpts["runType="][0] + "|--runType <runType>" )
	print ""
	print l2 % ("-" + inputOpts["action="][0] + ", --action  <action>", "action to perform. Valid actions are:")
	print l4 % ("load", "Downloads and processes DLA books, and loads the information into the TADDM database.")
	print l4 % ("list", "Lists the files hosted on the FTP site.")
	print l2 % ("-" + inputOpts["runType="][0] + ", --runType  <runType>", "Specifies whether to test or execute the operation. Valid runTypes are:")
	print l4 % ("test", "Performs all actions - except loading resource confifuration and relationship information into the TADDM database.")
	print l4 % ("doIt", "Performs all actions, including loading DLA book information into the TADDM database.")
	print " "
	print l1 % ("[FTP OPTIONS]","-" + inputOpts["ftpHost="][0] + "|--ftpHost <hostname>  -" + inputOpts["ftpPort="][0] + "|--ftpPort <portnumber>  -" + inputOpts["ftpUser="][0] + "|--ftpUser <username>  -" + inputOpts["ftpPassword="][0] + "|--ftpPassword <password> ")
	print l1 % ("","-" + inputOpts["ftpSourceDirectory="][0] + "|--ftpSourceDirectory <directory name>  -" + inputOpts["ftpDebugLevel="][0] + "|--ftpDebugLevel <debugLevel>  -" + inputOpts["removeSourceFiles"][0] + "|--removeSourceFiles " ) 
	print ""
	print l2 % ("-" + inputOpts["ftpHost="][0] + ", --ftpHost  <hostname>", "Hostname or IP Address of the FTP server where the DLA books are hosted")
	print l2 % ("-" + inputOpts["ftpPort="][0] + ", --ftpPort  <portNumber>", "Port number used to connect to the FTP server where the DLA books are hosted")
	print l2 % ("-" + inputOpts["ftpUser="][0] + ", --ftpUser  <hostname>", "User name used to authenticate with the FTP server")
	print l2 % ("-" + inputOpts["ftpPassword="][0] + ", --ftpPassword  <password>", "Password for the user used to access the FTP server")
	print l2 % ("-" + inputOpts["ftpSourceDirectory="][0] + ", --ftpSourceDirectory  <directory name>", "Path on the FTP server, relative to the user's home directory, from which DLA books are downloaded")	
	print l2 % ("-" + inputOpts["ftpRetries="][0] + ", --ftpRetries  <number-of-retries>", "Integer, used to control the amount of times the utility will attempt to connect to the FTP server")	
	print l2 % ("-" + inputOpts["ftpWaitTime="][0] + ", --ftpWaitTime  <number of seconds>", "Integer, number of seconds the utitility will wait between attempts to connect to the FTP server")	
	print l2 % ("-" + inputOpts["ftpDebugLevel="][0] + ", --ftpDebugLevel  <debugLevel>", "Integer, 0,1, or 2, used to control the level of logging information from the ftp transactions")	
	print l2 % ("-" + inputOpts["removeSourceFiles"][0] + ", --removeSourceFiles  True|False", "Controls whether source files on the FTP server are removed after they have been downloaded")	
	print " "
	targetFilenameFilterRegex
	print l1 % ("[PROCESSING OPTIONS]","-" + inputOpts["targetDirectory="][0] + "|--targetDirectory <directory name>  -" + inputOpts["targetFilenameFilterRegex="][0] + "|--targetFilenameFilterRegex <regEx>  -"  + inputOpts["targetFileMaxAgeDays="][0] + "|--targetFileMaxAgeDays <days> ")
	print l1 % ("","-" + inputOpts["enableBookDeltaProcessing"][0] + "|--enableBookDeltaProcessing  -" + inputOpts["deltaBookScriptLocation="][0] + "|--deltaBookScriptLocation <directory name>")
	print l1 % ("","-" + inputOpts["loadidmlOptions="][0] + "|--loadidmlOptions <options>  -" + inputOpts["locationTag="][0] + "|--locationTag <locatioNTag>  -" + inputOpts["keepWorkFiles"][0] + "|--keepWorkFiles -")  
	print ""
	print l2 % ("-" + inputOpts["targetDirectory="][0] + ", --targetDirectory  <directory name>", "Name of local directory to which DLA files are downloaded and processed")
	print l2 % ("-" + inputOpts["targetFilenameFilterRegex="][0] + ", --targetFilenameFilterRegex  <regEx>", "Regular MATCHING expression to filter files to be downloaded and processed")
	print l2 % ("-" + inputOpts["targetFileMaxAgeDays="][0] + ", --targetFileMaxAgeDays  <integer>", "Maximim age of DLA books to process (in days)")
	print l2 % ("-" + inputOpts["enableBookDeltaProcessing"][0] + ", --enableBookDeltaProcessing", "Enables delta processing of DLA books prior to updating CI information in the TADDM database")
	print l2 % ("-" + inputOpts["deltaBookScriptLocation="][0] + ", --deltaBookScriptLocation  <directory name>", "User name used to authenticate with the FTP server")
	print l2 % ("-" + inputOpts["loadidmlOptions="][0] + ", --loadidmlOptions  <options>", "Options, except for --locationTag/(-l), to be parsed to the loadidml utility")
	print l2 % ("-" + inputOpts["locationTag="][0] + ", --locationTag  <string>", "LocationTag to be assigned to all resources created by during loading of DLA books")
	print l2 % ("-" + inputOpts["keepWorkFiles"][0] + ", --keepWorkFiles  <options>", "Instructs the " + prog + " utility to remove downloaded and generated DLA books after processing")
	print " "
	print l1 % ("[MISC OPTIONS]","[-h|--help] [-d|--debug]")
	print ""
	print l2 % ("-" + inputOpts["debug"][0] + ", --debug","Echos debug messages to the console.")
	print l2 % ("-" + inputOpts["showInvocationOptions"][0] + ", --showInvocationOptions","Displays all invocation options in the console.")
	print l2 % ("-" + inputOpts["help"][0] + ", --help","Displays this help message.")
	print l2 % ("-" + inputOpts["quiet"][0] + ", --quiet","Suppress all output, except for help information, to the console.")
	print l2 % ("-" + inputOpts["suppressWarnings"][0] + ", --suppressWarnings","Prevents warning messages to be displayed on the console.")

	print " "
	print l0 % ("** Additional information regarding the supported arguments can be found in the associated properties file: ../etc/" + prog + ".properties")
	
	print " "
	print " "
	print l0 % ("EXAMPLES:")
	print ""
	print l1 % ("To assign default values for arguments that should be configured only once for your environment, update the relevant values in the ../etc/ " + prog + ".properties file","")
	print l3 % ("ftpHost = myFtpServer.mydomain.com","")
	print l3 % ("ftpPort = 21","")
	print l3 % ("ftpUser = taddmusr","")
	print l3 % ("ftpPassword = myPassword","")
	print l3 % ("enableBookDeltaProcessing = True","")
	print l3 % ("loadidmlOptions = -g -e","")
	print l3 % ("locationTag = MANAGEMENT","")
	print l3 % ("removeSourceFiles = True","")
	print l3 % ("keepWorkFiles = False","")
	print l2 % ("** Note that all boolean controls have a default value of False. ","")
	print l2 % ("** If the value set to True in the properties file, they cannot be overwritten by a command line argument","")
	print ""
	print l1 % ("To download DLA books to the default directory, populate the TADDM database, and remove the files on both the ftp site and locally:"," ")
	print l2 % (prog + "." + ext + " -" + inputOpts["action="][0] + " load -" + inputOpts["runType="][0] + " doit -" + inputOpts["removeSourceFiles"][0] + " -" + inputOpts["keepWorkFiles"][0],"")
	print ""
	print l1 % ("To download DLA books to the '../dla Books' directory, and generate delta books WITHOUT populating the TADDM database:","")
	print l2 % (prog + "." + ext + " -" + inputOpts["action="][0] + " load -"  + inputOpts["targetDirectory="][0] + " \"../dla Books\" -"  + inputOpts["enableBookDeltaProcessing"][0] + " -"  + inputOpts["deltaBookScriptLocation="][0] + " ../../tools/deltabooks -" + inputOpts["runType="][0] + " test","")
	print ""
	print l1 % ("To download DLA books to default directory, and populate the TADDM database while assigning a locationTag of MAINFRAME:","")
	print l2 % (prog + "." + ext + " -" + inputOpts["action="][0] + " load -"  + inputOpts["locationTag="][0] + " MANAGEMENT -" + inputOpts["runType="][0] + " doit","")
	print ""
	print l1 % ("To process only DLA books with a name that contains 'MQ':","")
	print l2 % (prog + "." + ext + " -" + inputOpts["action="][0] + " load -"  + inputOpts["targetFilenameFilterRegex="][0] + " \"(.*MQ.*)\" -" + inputOpts["runType="][0] + " doit","")
	
	raise SystemExit()


#################################################

################################################################################################
def init(trace=False,debug=False):

	global log, logfileName, prog, ext

	coll_home = getCollHome()
	prog,ext = getProgramName()
	#Load properties file in java.util.Properties
	propFileName = coll_home+"/etc/collation.properties"
	inStream = FileInputStream(propFileName)
	propFile = Properties()
	propFile.load(inStream)

	log, logfileName = setupLog4jLogging(trace,debug)

	return log, logfileName, prog


#############################################################################
def getProgramName():
	global prog
	dirname, progname = os.path.split(sys.argv[0])
	prog,ext = progname.split(".",1)
	return prog,ext


#############################################################################
def getCollHome():
	global coll_home
	coll_home = System.getProperty("com.collation.home")
	if coll_home[0] == "/" and "WINDOWS" in java.lang.System.getProperty('os.name').upper():
		coll_home = coll_home[1:]
	##coll_home = os.environ["COLLATION_HOME"]
	return coll_home


#############################################################################
def logit (level, message):
	#print level.upper() +  "logLevel:" + logLevel.upper() + " debug:" + str(debug) +  " quiet:" + str(quiet) +  " trace:" + str(trace) + ":   \t" +  message
	#print "???? " + level.upper() + "   " + logLevel
	if runType == "test":
		message = "TESTING: " + message

	if level.upper() == "INFO":
		#if string.upper(logLevel) in ["INFO","DEBUG","TRACE"]:
		log.info(message)
		if not quiet:
			print level.upper() + ":\t" +  message

	elif level.upper() in ["WARNING"]:
		if logLevel.upper() in ["INFO", "WARNING","ERROR","DEBUG","TRACE"]:
			log.info(message)
			if  not quiet and not suppressWarnings:
				print level.upper() + ":\t" +  message

	elif level.upper() == "ERROR":
		if logLevel.upper() in ["INFO","WARNING","ERROR","DEBUG","TRACE"]:
			log.error(message)
			if  not quiet:
				print level.upper() + ":\t" +  message

	elif level.upper() == "DEBUG":
		if logLevel.upper() in ["INFO", "WARNING","ERROR","DEBUG","TRACE"]:
			log.debug(message)
			if  not quiet and debug:
				print level.upper() + ":   \t" +  message
	else:
		print "Illegal log level '" + level.upper() + "'"
		raise Fatal
	
	return


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

	log.debug("Connecting to: " + str(host) + " on port " + str(port) )
	conn = ApiFactory.getInstance().getApiConnection(host, port, None, False)
	log.debug("Establishing session for user: " + str(user))
	sess = ApiFactory.getInstance().getSession(conn, user, password, ApiSession.DEFAULT_VERSION);
	api = sess.createCMDBApi()
	log.debug("Created CMDB api: " + str(api))
	#control = sess.createControlApi()
	#log.debug("Created Control api: " + str(api))

	return api


#######################################################################
def setupLog4jLogging(trace=False,debug=False):
	global log, logLevel
	#coll_home = getCollHome()
	#prog,ext = getProgramName()
	#Load properties file in java.util.Properties
	propFileName = coll_home+"/etc/collation.properties"
	inStream = FileInputStream(propFileName)
	propFile = Properties()
	propFile.load(inStream)


	if debug == True:
		logLevel = "DEBUG"
	else:
		logLevel = System.getProperty("com.collation.log.level")

	if logLevel == None:
		logLevel = "Info"


	# set properties for using the default TADDM log4j.xml file for logging
	if System.getProperty("com.collation.log.level") == None:
		System.setProperty("com.collation.log.level",propFile.getProperty("com.collation.log.level"))
	if System.getProperty("com.collation.log.filesize") == None:
		System.setProperty("com.collation.log.filesize",propFile.getProperty("com.collation.log.filesize"))
	if System.getProperty("com.collation.log.filecount") == None:
		System.setProperty("com.collation.log.filecount",propFile.getProperty("com.collation.log.filecount"))
	if System.getProperty("com.collation.log4j.servicename") == None:
		System.setProperty("com.collation.log4j.servicename","-" + prog)


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


	if logLevel == "INFO":
		log.setLevel(Level.INFO)
	elif logLevel == "ERROR":
		log.setLevel(Level.ERROR)
	elif logLevel == "DEBUG":
		log.setLevel(Level.DEBUG)
	elif logLevel == "TRACE":
		log.setLevel(Level.TRACE)

	logfile = File(coll_home+"/log/"+prog+".log")

	fileAppender = FileAppender(layout, logfile.getAbsolutePath(), True);

	log.addAppender(fileAppender);
	if trace == True:
		consoleAppender = ConsoleAppender(layout,"System.out")
		log.addAppender(consoleAppender);

	return log,logfile.getAbsolutePath()




###############################################################################
def executeCommandLineCommand(cmd):
	logit("DEBUG","executing:\t" +  cmd)
	##rc, output = commands.getstatusoutput(cmd + " " + args)
	p = Popen(cmd, shell=True, stdout=PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = p.communicate()
	rc = p.returncode

	logit("DEBUG",str(rc) + " returned from command :\t" + str(cmd))
	logit("DEBUG","command output:\t" + str(stdout))
	if rc > 0:
		logit("WARNING","command out :\t" + str(stdout))
		logit("WARNING","command err :\t" + str(stderr))
	else:
		logit("DEBUG","command error :\t" + str(stderr))
	return rc, stdout, stderr


###############################################################################
def trueOrFalse(val):
	ret = False
	if val.upper().strip() == "TRUE":
		ret = True
	return ret

###############################################################################
def debugDetails(obj):
	print 100*"^"
	print str(obj.__class__.__name__)
	print str(obj)
	print 100*"^"

###############################################################################
def getObjectMethods(obj):
	print 100*"^"
	print str(obj.__class__.__name__)
	
	methods = inspect.getmembers(obj,predicate=inspect.ismethod)
	debugDetails(methods)
	for m in methods:
		print "\t" + str(m)

###############################################################################
def	getmostRecentDLAFiles(files):
	
	
	currentFiles = getDLABookTimestamp(files)
	
	workFiles = {}
	for f in currentFiles.keys():
		mssName, newTS = currentFiles[f]
		
		if workFiles.has_key(mssName):
			fileName, oldTS = workFiles[mssName]
			if int(newTS) > int(oldTS):
				workFiles[mssName] = [ f, newTS]
		else:	
			workFiles[mssName] = [ f, newTS]
			
	recentFiles = {}
	for m in workFiles:
		fileName, timestamp = workFiles[m]
		recentFiles[fileName] = [m, timestamp]
			
	
	return recentFiles
###############################################################################
def	getDLABookTimestamp(files):
	# extract timestamp for each file
	mssNameRegex = "(.*)([0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9].[0-9][0-9].[0-9][0-9])Z.*"
	bookFiles = {}
	for f in files:
		r = re.findall(mssNameRegex, f)
   		if r != None:
			for h in r:
				mssName=h[0]
				t = h[1]
				timestamp = str(t[0:4]) + str(t[5:7]) + str(t[8:10]) + str(t[11:13]) + str(t[14:16]) + str(t[17:19])
				bookFiles[f] = [mssName, timestamp]
	
	return bookFiles

###############################################################################
def	getFilesFromFtpServer(action, ftp, sourceDirectory, targetDirectory):
		
	if ftpDebugLevel > 0:
		logit("DEBUG","Setting ftp-debug level to " + str(ftpDebugLevel))
		ftp.set_debuglevel(ftpDebugLevel)


	logit("DEBUG","Connecting to ftp server " + ftpHost + " on port " + ftpPort)
	conn = ftp.connect(ftpHost, ftpPort)
		
	#Open ftp connection
	logit("DEBUG","Logging in to ftp server " + ftpHost + " as user " + ftpUser + " using password " + ftpPassword)
	ftp.login(ftpUser, ftpPassword)
	code,home = ftp.sendcmd("pwd").split(" ",1)
	home = home.strip("\"") 
	logit("DEBUG","Home directory for user '" + ftpUser + "' is '" + str(home))
	
	
	#Change to source directory
	logit("DEBUG","Changing to ftpSourceDirectory '" + ftpSourceDirectory + "' on the ftp server")
	ftp.cwd(ftpSourceDirectory)

	
	#List the files from the ftp source directory
	logit("DEBUG","Getting files in '" + ftpSourceDirectory + "' on the ftp server")
	#bookFiles = ftp.nlst("*.xml")
	bookFiles = ftp.nlst("*")
	
	
	if targetFileMaxAgeDays != None:
		age = timedelta(targetFileMaxAgeDays)
		#local_tz = get_localzone()   # get local timezone
		utcNow = datetime.utcnow() # get timezone-aware datetime object
		days_ago = utcNow - age
		#naive = now.replace(tzinfo=None) - age # same time
		#yesterday = local_tz.localize(naive, is_dst=None) # but elapsed hours may differ
		
		currentTime = int(utcNow.strftime("%Y%m%d%H%M%S"))
		logit("DEBUG", "Execution UTC timestamp is : " + str(currentTime))
		cutoffTime = int(days_ago.strftime("%Y%m%d%H%M%S"))
		logit("DEBUG", "File age  timestamp is : " + str(cutoffTime))#Get the file info
		
	
		
	bookFiles.sort()
	files = []
	workFiles = getDLABookTimestamp(bookFiles)

	for book in workFiles.keys():
		if targetFilenameFilterRegex != None:
			r = re.match(targetFilenameFilterRegex, book)
			if r != None:
				logit("DEBUG","DLA book: " + str(book) + "  matches: " + str(targetFilenameFilterRegex))
				
				mssName, fileTime = workFiles[book]
				
				if targetFileMaxAgeDays != None and int(fileTime) < cutoffTime :
					logit("DEBUG","DLA book: " + str(book) + "  omitted. Older than : " + str(targetFileMaxAgeDays) + " days")
					continue
				
				files.append(book)
			else:
				logit("DEBUG", "DLA book EXCLUDED: " + str(book) + " DOES NOT MATCH  " + str(targetFilenameFilterRegex))
				continue
			
			
	dlaFiles = getDLABookTimestamp(files)


	keys = dlaFiles.keys()
	keys.sort()

				
	for book in keys: 
		if action == "list":
			print str(book)
		else:
			try:	
				# move to the target directory
				if not os.path.exists(targetDirectory):
					logit("DEBUG","Creating ftp target directory: '" + targetDirectory + "'")
					os.mkdir(targetDirectory)
				os.chdir(targetDirectory)
			
				#if runType != "test":
				retFile = open(book, "wb")
				r = ftp.retrbinary("RETR " + book, retFile.write)
				retFile.close()
				logit("DEBUG","Retrieved book '" + book + "' into " + os.getcwd())

				##  delete the source file
				if removeSourceFiles:
					logit("DEBUG","Deleting source book '" + book + "' from " + ftpSourceDirectory)
					if runType != "test":
						a = ftp.delete(book)

				
			except ftplib.error_perm, ex:
				ex_type, ex, tb = sys.exc_info()
				msg = "Exception retrieving '" + book + "':\t" + str(ex_type) + "\tErrorType:" + str(ex)
				#msg = "\n\texception class:\t" + str(ex_type) + "\n\tErrorType:\t" + str(ex) + "\n\t" + str(traceback.format_tb(tb)[0])
				#for i in xrange(len(traceback.format_tb(tb))-1):
				#	msg = msg + "\n\t" + str(traceback.format_tb(tb)[i+1])
				logit("WARNING", msg)
				bookFiles.remove(book)
				raise 
			
			except IOError, ex:
				ex_type, ex, tb = sys.exc_info()
				msg = "Exception retrieving '" + book + "':\t" + str(ex_type) + "\tErrorType:\t" + str(ex)
				#for i in xrange(len(traceback.format_tb(tb))-1):
				#	msg = msg + "\n\t" + str(traceback.format_tb(tb)[i+1])
				logit("WARNING", msg)
				bookFiles.remove(book)
				raise
			
	ftp.quit()

	return dlaFiles
		
			
###############################################################################
###   MAIN
###############################################################################

try:
	runType = "test"

	sStart = time.time()
	
	global log,logfileName,prog,ext,dirname,progname,quiet,ext, numberOfRecords, debug, trace, actionVerb
	log,logfileName,prog = init()
	
	
	### set defaults
	
	action = "help"
	actionVerb = None
	debug = False
	removeSourceFiles = False
	keepWorkFiles = False
	deltaBookScriptLocation = None
	deltaBookScriptName = "deltabooks"
	if "WINDOWS" in java.lang.System.getProperty('os.name').upper():
		deltaBookScriptName = deltaBookScriptName + ".cmd" 
	else:	
		deltaBookScriptName = deltaBookScriptName + ".sh" 
		
	loadIdmlScriptName = "loadidml"
	if "WINDOWS" in java.lang.System.getProperty('os.name').upper():
		loadIdmlScriptName = loadIdmlScriptName + ".cmd" 
	else:	
		loadIdmlScriptName = loadIdmlScriptName + ".sh" 
	
	#dlaRootDir = None
	enableBookDeltaProcessing = False
	help = ""
	propertiesFile = str(os.sep).join(["..","etc",prog+".properties"]) 
	quiet = False
	
	now = time.time()
	#localtime = time.gmttime(now)
	milliseconds = '%03d' % int((now - int(now)) * 1000)
	
	showInvocationOptions = False
	suppressWarnings = False
	targetFilenameFilterRegex = None
	targetFileMaxAgeDays = None
	#taddmServerHost = "localhost"
	#taddmServerPassword = "collation"
	#taddmServerPort = 9433
	#taddmServerUser = "administrator"
	ftpSourceDirectory = None
	targetDirectory = None
	locationTag = None
	loadidmlOptions = None
	ftpDebugLevel = 0
	ftpRetries = 5
	ftpWaitTime = 30
	ftpHost = None
	ftpPassword = None
	ftpPort = 21
	ftpUser = None
	
	#locationScopeSelectionWhereClause = None
	#operatingSystemScopeSelectionWhereClause = None
	#discoveryProtocolScopeSelectionWhereClause = None
	trace = False
	
	
	subSystemNameRegex = "(.*)[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9].[0-9][0-9].[0-9][0-9]Z.*"
	
	
	runTypes = ["test","doit"]
	actions = ["help", "list", "load" ]
	#expandedlocationTagPriorities = ["scope", "scopegroup"]
	#locationTagPriorities = ["assigned", "scope", "scopegroup", "nameregex", "locationtagregex","default","static"]
		
	
			
	#host = taddmServerHost
	#port = taddmServerPort
	#user = taddmServerUser
	#password = taddmServerPassword
	
	
	inputOpts = {}
			
	inputOpts["action="] = "a:"
	inputOpts["debug"] = "d"
	inputOpts["removeSourceFiles"] = "R"
	inputOpts["keepWorkFiles"] = "K"
	#inputOpts["dlaRootDir"] = "S"
	inputOpts["deltaBookScriptLocation="] = "s:"
	inputOpts["enableBookDeltaProcessing"] = "D"
	inputOpts["targetFilenameFilterRegex="] = "F:"
	inputOpts["targetFileMaxAgeDays="] = "A:"
	inputOpts["ftpSourceDirectory="] = "S:"
	inputOpts["targetDirectory="] = "T:"
	inputOpts["locationTag="] = "l:"
	inputOpts["loadidmlOptions="] = "o:"
	inputOpts["ftpDebugLevel="] = "f:"
	inputOpts["ftpRetries="] = "n:"
	inputOpts["ftpWaitTime="] = "w:"
	inputOpts["ftpHost="] = "H:"
	inputOpts["ftpPassword="] = "p:"
	inputOpts["ftpPort="] = "P:"
	inputOpts["ftpUser="] = "u:"
	inputOpts["propertiesFile="] = "I:"
	inputOpts["quiet"] = "q"
	inputOpts["runType="] = "r:"
	inputOpts["help"] = "h"
	inputOpts["showInvocationOptions"] = "O"
	inputOpts["suppressWarnings"] = "W"
	inputOpts["trace"] = "t"
	#inputOpts["host="] = "H:"
	#inputOpts["password="] = "p:"
	#inputOpts["port="] = "P:"
	#inputOpts["user="] = "u:"
	
	
	shortOpts = ",".join(inputOpts.values())
	longOpts = inputOpts.keys()


	#try:
	
	# properties file name
	try:
		sys.argv.index("--propertiesFile")
		prog_propsFileName = sys.argv[sys.argv.index("--propertiesFile") + 1]
	except:
		try:
			sys.argv.index("-I")
			prog_propsFileName = sys.argv[sys.argv.index("-"+ inputOpts["propertiesFile="][0]) + 1]
		except:
			prog_propsFileName = ".." + os.sep + "etc" + os.sep + prog + ".properties"



	###   READ THE PROPERTIES FILE

	if not os.path.exists(prog_propsFileName):
		pFileName = ".." + os.sep + "etc" + os.sep + prog_propsFileName
		if os.path.exists(pFileName):
			prog_propsFileName = pFileName
		else:
			name, ext = os.path.splitext(pFileName)
			if ext in [None,""] :
				prog_propsFileName = pFileName + ".properties"
				if not os.path.exists(prog_propsFileName):
					raise Fatal, "Properties file " + prog_propsFileName + " does not exist"


	progProps = {}
	logit("DEBUG", "reading properties file: " + prog_propsFileName)
	inStream = FileInputStream(prog_propsFileName)
	prog_props = Properties()
	prog_props.load(inStream)

	
	validProperties = inputOpts.keys()
	


	for key in prog_props.propertyNames():
		val = prog_props.getProperty(key).strip()
		progProps[key] = val.strip()
		
		if key.lower() == "action".lower():
			action = progProps[key]

		elif key.lower() == "debug".lower():
			debug = trueOrFalse(progProps[key])
					
		elif key.lower() == "targetFilenameFilterRegex".lower():
			targetFilenameFilterRegex = progProps[key]
					
		elif key.lower() == "targetFileMaxAgeDays".lower():
			targetFileMaxAgeDays = int(progProps[key])
					
		elif key.lower() == "removeSourceFiles".lower():
			removeSourceFiles = trueOrFalse(progProps[key])

		elif key.lower() == "keepWorkFiles".lower():
			keepWorkFiles = trueOrFalse(progProps[key])

		elif key.lower() == "enableBookDeltaProcessing".lower():
			enableBookDeltaProcessing = trueOrFalse(progProps[key])

		elif key.lower() == "deltaBookScriptLocation".lower():
			deltaBookScriptLocation = progProps[key]

		elif key.lower() == "targetDirectory".lower():
			targetDirectory = progProps[key]

		elif key.lower() == "ftpSourceDirectory".lower():
			ftpSourceDirectory = progProps[key]

		elif key.lower() == "ftpUser".lower():
			ftpUser = progProps[key]

		elif key.lower() == "ftpPassword".lower():
			ftpPassword = progProps[key]

		elif key.lower() == "ftpDebugLevel".lower():
			ftpDebugLevel = int(progProps[key])

		elif key.lower() == "ftpRetries".lower():
			ftpRetries = int(progProps[key])

		elif key.lower() == "ftpWaitTime".lower():
			ftpWaitTime = int(progProps[key])

		elif key.lower() == "ftpHost".lower():
			ftpHost = progProps[key]

		elif key.lower() == "ftpPort".lower():
			ftpPort = progProps[key]

		elif key.lower() == "locationTag".lower():
			locationTag = progProps[key]

		elif key.lower() == "loadidmlOptions".lower():
			loadidmlOptions = progProps[key]

		elif key.lower() == "quiet".lower():
			quiet = trueOrFalse(progProps[key])

		elif key.lower() == "runType".lower():
			runType = progProps[key]
					
		elif key.lower() == "suppressWarnings".lower():	
			suppressWarnings = trueOrFalse(progProps[key])

		elif key.lower() == "showInvocationOptions".lower():	
			showInvocationOptions = trueOrFalse(progProps[key])
		
			'''
			elif key.lower() == "taddmServerUser".lower():
				taddmServerUser = progProps[key]
	
			elif key.lower() == "taddmServerPassword".lower():
				taddmServerPassword = progProps[key]
	
			elif key.lower() == "taddmServerHost".lower():
				taddmServerHost = progProps[key]
	
			elif key.lower() == "taddmServerPort".lower():
				taddmServerPort = int(progProps[key])
			'''
		elif key.lower() == "trace".lower():
			trace = trueOrFalse(progProps[key])
		
		
		else:
			raise Fatal, "Unknown property '" + key + "' specified in properties file " + prog_propsFileName
		




	####################################################################
	#	   get arguments
	####################################################################

	if len(sys.argv) == 1:
		raise Usage("help")
	if len(sys.argv) > 1:
		if sys.argv[1].upper() in ["-H", "HELP", "--HELP"]:
			raise Usage("help")
		elif not (sys.argv[1][0] == "-"):
			action = sys.argv[1]
			argv = sys.argv[2:]
		else:
			argv = sys.argv[1:]

	#shortOpts = "a:c:de:hH:iI:l:Op:P:n:qr:s:x:w:Wt:u:?:"
	#longOpts = ["action=","concurrentDiscoveries=","debug","runNameEyeCatcher=","help","host=","inline","propertiesFile=","locationTag=","showInvocationOptions","password=","port=","profileName=","quiet","action=","scope=","whereClause=","suppressWarnings","threads=","user=","unknownValue"]

	opts = {}
	args = {}


	msg = None

	try:
		opts, args = getopt.getopt(argv, shortOpts, longOpts)
	except GetoptError, opt_ex:
		raise Usage(opt_ex.msg)


	for o, a in opts:

		o = o.strip()

		if o in ("-"+inputOpts["action="][0], "--action"):
			action = a.strip()

		elif o in ("-"+inputOpts["debug"][0], "--debug"):
			debug = True
			
		elif o in ("-"+inputOpts["removeSourceFiles"][0], "--removeSourceFiles"):	
			removeSourceFiles = True

		elif o in ("-"+inputOpts["keepWorkFiles"][0], "--keepWorkFiles"):	
			keepWorkFiles = True

		elif o in ("-"+inputOpts["targetFilenameFilterRegex="][0], "--targetFilenameFilterRegex"):	
			targetFilenameFilterRegex = str(a.strip())

		elif o in ("-"+inputOpts["targetFileMaxAgeDays="][0], "--targetFileMaxAgeDays"):	
			targetFileMaxAgeDays = int(a.strip())

		elif o in ["-"+inputOpts["deltaBookScriptLocation="][0], "--deltaBookScriptLocation"]:
			deltaBookScriptLocation = str(a.strip())

		elif o in ["-"+inputOpts["enableBookDeltaProcessing"][0], "--enableBookDeltaProcessing"]:
			enableBookDeltaProcessing = True

		elif o in ["-"+inputOpts["ftpSourceDirectory="][0], "--ftpSourceDirectory"]:
			ftpSourceDirectory = a.strip()

		elif o in ["-"+inputOpts["targetDirectory="][0], "--targetDirectory"]:
			targetDirectory = a.strip()

		elif o in ["-"+inputOpts["ftpUser="][0], "--ftpUser"]:
			ftpUser = a.strip()

		elif o in ("-"+inputOpts["ftpPassword="][0], "--ftpPassword"):
			ftpPassword = True

		elif o in ("-"+inputOpts["ftpDebugLevel="][0], "--ftpDebugLevel"):
			ftpDebugLevel = int(a)

		elif o in ("-"+inputOpts["ftpRetries="][0], "--ftpRetries"):
			ftpRetries = int(a)

		elif o in ("-"+inputOpts["ftpWaitTime="][0], "--ftpWaitTime"):
			ftpWaitTime = int(a)

		elif o in ("-"+inputOpts["ftpHost="][0], "--ftpHost"):
			ftpHost = a.strip()

		elif o in ("-"+inputOpts["ftpPort="][0], "--ftpPort"):
			ftpPort = a

		elif o in ["-"+inputOpts["locationTag="][0], "--locationTag"]:
			locationTag = a.strip()

		elif o in ["-"+inputOpts["loadidmlOptions="][0], "--loadidmlOptions"]:
			loadidmlOptions = a.strip()

		elif o in ("-"+inputOpts["help"][0], "--help"):
			raise Usage("help")

		#elif o in ("-"+inputOpts["host="][0], "--host"):
		#	taddmServerHost = str(a.strip())

		elif o in ("-"+inputOpts["propertiesFile="][0], "--propertiesFile"):
			prog_propsFile = a.strip()

		elif o in ("-"+inputOpts["showInvocationOptions"][0], "--showInvocationOptions"):
			showInvocationOptions = True

		#elif o in ("-"+inputOpts["password="][0], "--password"):
		#	taddmServerPassword = string.strip(a)

		#elif o in ("-"+inputOpts["port="][0], "--port"):
		#	taddmServerPort = int(a.strip())

		elif o in ("-"+inputOpts["quiet"][0], "--quiet"):
			quiet = True

		elif o in ("-"+inputOpts["runType="][0], "--runType"):
			runType = a.strip().lower()

		elif o in ("-"+inputOpts["trace"][0], "--trace"):
			trace = True
			
		#elif o in ("-"+inputOpts["user="][0], "--user"):
		#	taddmServerUser = string.strip(a)

		elif o in ("-"+inputOpts["unknownValue="][0], "--unknownValue"):
			taddmServerUser = string.strip(a)

		elif o in ("-"+inputOpts["suppressWarnings"][0], "--suppressWarnings"):
			suppressWarnings = True

		else:
			raise Usage("You provided an unknown option: " + str(o))

		if len(args) > 0 and len(opts) > 0:

			a = string.strip(str(opts[len(opts) - 1]), "(")
			a = string.strip(a, ")")
			x, y = string.split(a, ",", 1)
			a = string.strip(x, "'") + " " + string.strip(y, "'")
			raise Exit(4, "Your input was not parsed correctly. The problem is likely related to the '" + str(args[0]) + "' argument number following '" + a + "'")




	if showInvocationOptions or debug:
		logit("INFO",80*"=" + "\nINFO:\tStarting " + prog + " with options:")
	
		list = inputOpts.keys()
		list.sort()
		for key in list:
			opt = key.strip("=")
			prm = inputOpts[key]
			val = str(eval(opt))
			if "password" in opt.lower():
				val = "*"*len(val)
			logit("INFO","%-35s(-%s):  %-40s" % (opt,prm.strip(":"),val))
			
	
	###########################
	## validate input

	if runType not in runTypes:
		msg = "Invalid runType '-" + inputOpts["runType="][0] + "|--runType " + str(runType) + "' specified. Choose a value from '" + "', '".join(runTypes) + "'."

	if action not in actions:
		msg = "Invalid action '-" + inputOpts["action="][0] + "|--action " + str(action) + "' specified. Choose a value from '" + "', '".join(actions) + "'."

	if action == "list":
		actionVerb = "Listing"
	elif action == "load":
		actionVerb = "Loading"

	if ftpPort == None:
		ftpPort = 21

	'''	
	if taddmServerUser == None:
		msg = "\ttaddmServerUser (-u) must be specified."
	elif taddmServerPassword == None:
		msg = "\ttaddmServerPassword (-p) must be specified."
			
	elif ftpHost == None:
		msg = "You must provide the hostname or IP address of the ftp server"
				
	elif ftpUser == None:
		msg = "You must provide the hostname or IP address of the ftp server"
				
	elif ftpPassword == None:
		msg = "You must provide the password for the user used to access the ftp server"
	'''							
			
	if msg != None:
		raise Usage(msg)

	##################

	if action.lower() == 'help':
		show_help()
	

	ipInfo = socket.gethostbyaddr(socket.gethostname())
	thisHostName = str(ipInfo[0])
	thisHostIp = str(ipInfo[2][0])
	logit("debug","This host is: " + str(thisHostName) + "   with ipAddress: " + str(thisHostIp))

	cwd = os.getcwd()

		
	# get log level
	if System.getProperty("com.collation.log.level") == None:
		logit("INFO","setting loglevel to: " + str(propFile.getProperty("com.collation.log.level")))
		System.setProperty("com.collation.log.level",propFile.getProperty("com.collation.log.level"))



	## read bulkload properties
	bulk_propsFileName = coll_home + os.sep + "etc" + os.sep + "bulkload.properties"

	###   READ THE PROPERTIES FILE

	if not os.path.exists(bulk_propsFileName):
		raise Fatal("could not find bulkload properties file: '" + bulk_propsFileName + "'")

	
	logit("DEBUG", "reading bulkload properties file: " + prog_propsFileName)
	inStream = FileInputStream(bulk_propsFileName)
	bulkloadProperties = Properties()
	bulkloadProperties.load(inStream)

	
	if bulkloadProperties.containsKey("com.ibm.cdb.bulk.workdir") != None:
		bulkDirectory = str(bulkloadProperties.getProperty("com.ibm.cdb.bulk.installdir")) +  os.sep + str(bulkloadProperties.getProperty("com.ibm.cdb.bulk.workdir"))
		bulkDirectory = coll_home +  os.sep + str(bulkloadProperties.getProperty("com.ibm.cdb.bulk.workdir"))
		logit("DEBUG","bulk directory is: '" + bulkDirectory + "'")
	
	
		
		## move to target directory
		if not os.path.isdir(bulkDirectory):
			logit("DEBUG", "Target directory: '" + bulkDirectory +"' does not exist. Creating it.")
			#if runType != "test":
			os.mkdir(bulkDirectory)
			bulkDirectory = os.path.abspath(bulkDirectory)
		#targetDirectory = bulkDirectory
	
	
	if targetDirectory == None:
		targetDirectory = bulkDirectory
		
	if not os.path.exists(str(targetDirectory)):
		logit("DEBUG","Creating ftp target directory: '" + str(targetDirectory) + "'")
		os.mkdir(targetDirectory)
	
	
	targetDirectory = os.path.abspath(targetDirectory) 
	
	
	## manage directories for delta processing
	
	if action == 'load' and enableBookDeltaProcessing:
		targetRootDirectory = targetDirectory
		prev = os.path.abspath(targetDirectory + os.sep + "previous")
		curr = os.path.abspath(targetDirectory + os.sep + "current")
		if os.path.exists(str(prev)):
			logit("DEBUG","Deleting old 'previous' directory ('" + str(prev) + "') with content")
			#if runType != "test":
			for f in os.listdir(str(prev)):
				fileName = os.path.abspath(prev + os.sep + f)
				os.remove(fileName)
			os.rmdir(prev)	
			 
		if os.path.exists(curr):
			logit("DEBUG","Moving old 'current' directory ('" + str(curr) + "') to 'previous'('" + str(prev) + "')")
			#if runType != 'test':
			os.rename(curr, prev)
		
		logit("DEBUG","Creating new 'current' directory: '" + str(curr) + "'")
		os.mkdir(curr)
		
		if not os.path.exists(prev):
			os.mkdir(prev)
				 
		targetDirectory = curr
		

	
	ftpObject = FTP()

	##  get the files
	pStart = time.time()
	ftpWaitTime = 30
	ftpRetries = 5
	ftpRetries = Decimal(ftpRetries,1)
	i = Decimal(0,1)
	
	logit("DEBUG","Retrieving files from the ftp server " + ftpHost)
	
	while i < ftpRetries:
		i = i + 1
			
		try:
			dlaFiles = getFilesFromFtpServer(action, ftpObject, ftpSourceDirectory, targetDirectory)
			pElapsed = round(time.time() - pStart,2)
			if len(dlaFiles) > 0:
				logit("DEBUG",actionVerb + " " + str(len(dlaFiles)) + " files in " + str(pElapsed) + " seconds (" + str(round(pElapsed/60, 2)) + " minutes)")
			i = ftpRetries
		
		except Exception, ex:
			ex_type, ex, tb = sys.exc_info()
			if i < ftpRetries:
				msg = "Retrying in " + str(ftpWaitTime) + " seconds."
			else:
				msg = "Abandoning download from ftp server."	
			if i/ftpRetries == 1:
				ftpDebugLevel = 2
			elif round(Decimal(i/ftpRetries),1) > 0.5:
				ftpDebugLevel = 1
					
			logit("ERROR"," FTP download attempt # " + str(i) + ": An " + str(ex) + " error occured while retrieving files. " + msg)
			
			if i >= ftpRetries:	
				raise SystemExit(8)
		
	if action == 'list':
		raise SystemExit()
	
	
	# if no files need to be processed, move previous back to current	
	if len(dlaFiles) == 0:
		logit("INFO","There are no files to load into the TADDM database")
		if enableBookDeltaProcessing:
			logit("DEBUG","Moving previous to current")		
			os.rmdir(curr)
			os.rename(prev, curr)
		raise SystemExit()	

	
	

	logit("DEBUG","Current directory is: '" + str(cwd) + "'")
	
			
	## create delta books
	if enableBookDeltaProcessing:
		dlaFiles = {}
		delta = os.path.abspath(targetRootDirectory + os.sep + "delta")
		if not os.path.exists(delta):
			#if runType != 'test':
			os.mkdir(delta)

		# remove content of delta directory
		if os.path.exists(str(prev)):
			logit("DEBUG","Clearing delta directory")
			for f in os.listdir(delta):
				file = os.path.join(delta, f)
				if os.path.isfile(file):
					logit("DEBUG","\tRemoving file '" + file + "'")
					os.remove(file)
		
		
		deltaCmd = cwd + os.sep + deltaBookScriptLocation + os.sep + deltaBookScriptName +  " -f " + prev + " -t " + curr + " -o " + delta
		logit("DEBUG","Generating deltabooks using command: '" + deltaCmd + "'")
		
		#if runType != "test" :
		dStart = time.time()
		executeCommandLineCommand(deltaCmd)
		
		# list delta books
		for f in os.listdir(delta):
			file = os.path.join(delta, f)
			if os.path.isfile(file) and file.endswith(".xml")  :
				logit("INFO","Generated delta book: '" + os.path.abspath(file) + "'")
				logit("DEBUG","moving '" + os.path.join(delta,file) + "'  to  '" + os.path.join(targetRootDirectory,f) + "'")
				os.rename(os.path.join(delta,file), os.path.join(targetRootDirectory,f))
				dlaFiles[f] = None
				#						if os.path.exists(str(prev)):
				# bulkDirectory
		dElapsed = round(time.time() - dStart,2)
		logit("INFO","Generated " + str(len(dlaFiles)) + " delta books in " + str(dElapsed) + " seconds (" + str(round(dElapsed/60, 2)) + " minutes)")
		
	
	logit("DEBUG", "About to load " + str(len(dlaFiles)) + " DLA books ")
	#for f in os.listdir(targetDirectory):
	for f in dlaFiles.keys():
		file = os.path.join(targetDirectory, f)
		if os.path.isfile(file) and file.endswith(".xml"):			
			logit("DEBUG","\t'" + file + "'")
		
	
	loadIdmlCmd = coll_home + os.sep + "bin" + os.sep + loadIdmlScriptName + " -f \"" + targetDirectory + "\""
	if loadidmlOptions != None:
		loadIdmlCmd = loadIdmlCmd + " " + loadidmlOptions 
	if locationTag != None:
		loadIdmlCmd = loadIdmlCmd + " -l \"" + locationTag + "\"" 
	
	
	if action == "load":
		if runType == 'doit':
			msg = "Loading DLA books using command:"
		else:
			msg = "The following command will be used to load DLA books, if testing is disabled: " 	
		logit("INFO",msg + "\n'" + loadIdmlCmd + "'")
	
		if runType == 'doit':
			lStart = time.time()
			executeCommandLineCommand(loadIdmlCmd)
			lElapsed = round(time.time() - lStart,2)
			logit("INFO","Loaded " + str(len(dlaFiles)) + " books into the TADDM database in " + str(lElapsed) + " seconds (" + str(round(lElapsed/60, 2)) + " minutes)")
	
	
	##  delete the work file
	if not keepWorkFiles:
		directoryToDelete = targetDirectory
		if enableBookDeltaProcessing:
			directoryToDelete = targetRootDirectory
			
		logit("DEBUG","Removing work files")
		for f in dlaFiles:
			logit("DEBUG","\tDeleting  book '" + f + "' from " + directoryToDelete)
			if os.path.exists(os.path.join(directoryToDelete, f)):
				os.remove(os.path.join(directoryToDelete, f))
				
		if enableBookDeltaProcessing:
			logit("DEBUG","\tRmoving directory '" + prev)
			for root, dirs, files in os.walk(prev, topdown=False):
				for name in files:					
					logit("DEBUG","\tDeleting book '" + name + "' from " + root)
					os.remove(os.path.join(root, name))					
				for name in dirs:
					logit("DEBUG","\tDeleting directory '" + name + "' from " + root)
					os.rmdir(os.path.join(root, name))		
			os.rmdir(prev)			


	## keep only the most current files
	if enableBookDeltaProcessing:
		currentFiles = {}
		for root, dirs, files in os.walk(targetDirectory, topdown=False):
			for name in files:					
				#logit("DEBUG","\tretrieved '" + name + "' from " + root)
				currentFiles[name] = os.path.join(root, name)					
		logit("INFO","Read " + str(len(currentFiles)) + " file names from " + targetDirectory)
			
		recentFiles = getmostRecentDLAFiles(currentFiles.keys())
		logit("INFO","Identified " + str(len(recentFiles.keys())) + " files as most current")
		
		for f in currentFiles.keys():
			if not recentFiles.has_key(f):
				logit("DEBUG","\tRemoving obsolete file  '" + currentFiles[f])
				os.remove(currentFiles[f])
		
		
		
	sElapsed = round(time.time() - sStart,2)
	logit("INFO","Completed processing of " + str(len(dlaFiles)) + " DLA books in " + str(sElapsed) + " seconds (" + str(round(sElapsed/60, 2)) + " minutes)")
	
		
	raise SystemExit()


except Quit, quit_ex:
		if quit_ex.rc == 0:
			log.info("\n" + prog + " ended  sucessfully")
		SystemExit()

except SystemExit,sys_ex:
		#print "---- " + str(sys_ex)
		logit("DEBUG","Terminating")
		sys.exit(sys_ex)


except Exit, exit_ex:
		print exit_ex.msg
		log.error("("+str(exit_ex.rc)+") " + exit_ex.msg)
		raise SystemExit(exit_ex.rc)

except Exception, ex:
		ex_type, ex, tb = sys.exc_info()
		msg = "\n\t" + str(ex_type) + "\nErrorType:\t" + str(ex) + "\n" + str(traceback.format_tb(tb)[0])
		for i in xrange(len(traceback.format_tb(tb))-1):
			msg = msg + "\n" + str(traceback.format_tb(tb)[i+1])
		logit("ERROR", msg)
		sys.exit()


