#!/usr/bin/env ../../bin/jython_coll
############### Begin Standard Header - Do not add comments here ###############
# 
# File:     %W%
# Version:  %I%
# Modified: %G% %U%
# Build:    %R% %L%
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

import taddmJythonApiHelper

from taddmJythonApiHelper import *

    
#######################################################################################################
#######################################################################################################
class Usage(Exception):
    def __init__(self, msg):
        
        if msg != None:
            printit(msg)        
        show_help()        
        raise SystemExit


#######################################################################################################
#######################################################################################################
class Quit(Exception):
    def __init__(self,rc=0,msg=None):

        self.rc = rc
        self.msg = msg        

        return
        

#######################################################################################################
#######################################################################################################
class Exit(Exception):
    def __init__(self, rc=0,msg=None):

        self.msg = msg
        self.rc = rc
        
        if rc > 0:
            log.error(msg)
            #(ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
            #printit "\n\n***ERROR:"
            #printit sys.exc_info()
            #traceback.print_exc(ErrorTB)


###############################################################################
###############################################################################
class myRelationships:
    
    #########################################################################
    def __init__(self):
        self.relationships = {}

    #########################################################################
    def getCount(self):
        return len(self.relationships.keys())

    
    #########################################################################
    def populate(self,sources,targets,relationshipName,relGuids=[]):
        self.relationships = {}

        # gather relationship information
        source = None
        target = None
        
        if len(relGuids) > 0:
            for r in runRelationshipQuery(source,target,relationshipName,relGuids[0]):
                myRelationship(r)
        elif len(sources) > 0:
            for source in sources:
                if len(targets) > 0:
                    for target in targets:
                        for r in runRelationshipQuery(source,target,relationshipName):                        
                            myRelationship(r)
                else:
                    for r in runRelationshipQuery(source,target,relationshipName):                        
                        myRelationship(r)
        elif len(targets) > 0:
                for target in targets:
                    for r in runRelationshipQuery(source,target,relationshipName):                        
                        myRelationship(r)
        elif relationshipName != None:
            for r in runRelationshipQuery(source,target,relationshipName):                        
                myRelationship(r)
                
                
    ########################################################
    def newRelationships(self,sources,targets,relationshipName):
        self.relationships = {}

        # gather relationship information
        source = None
        target = None
        
        newRels = []
        if len(sources) > 0:
            for source in sources:
                if len(targets) > 0:
                    for target in targets:
                        newRels.append([source,target,relationshipName])
                        
            create = False            
            if force == False:
                printit("About to create the following relationships:")
                for r in newRels:
                    source = r[0]
                    target = r[1]
                    type = r[2]
                    sourceLongClass, sourceShortClass =  getClassNames(source)
                    targetLongClass, targetShortClass =  getClassNames(target)
                    
                    sourceShortClass = sourceShortClass 
                    targetShortClass = targetShortClass 
                    printit("\t" + sourceShortClass + "\t" + source.getDisplayName() +"\t" + type + "\t" + targetShortClass + "\t" + target.getDisplayName())  
                            
                create, deleteAll = promptUser("Are you certain that you want to create these relationships") 
            
            if force == True or create == True:
                for r in newRels:
                    source = r[0]
                    target = r[1]
                    type = r[2]
                    sourceLongClass, sourceShortClass =  getClassNames(source)
                    targetLongClass, targetShortClass =  getClassNames(target)
                    log.info("Creating relationship: \t" + sourceShortClass + "\t" + source.getDisplayName() +"\t" + type + "\t" + targetShortClass + "\t" + target.getDisplayName())
                    newRel = ModelObjectFactory.newInstance(Class.forName("com.collation.platform.model.topology.core.Relationship"))
                    newRel.setSource(source) 
                    newRel.setTarget(target)
                    newRel.setType("com.collation.platform.model.topology.relation." + relationshipName)
                    newRelGuid = api.update(newRel,None)
                    newRelObj = api.find(newRelGuid,2,None)                        
                    myRelationship(newRelObj)

            if force == True:                    
                self.populate(sources,targets,relationshipName)
                printit("Created " + str(self.getCount()) + " relationships:")
                self.showDetails()

    
    #######################################################
    def add(self,myRelationship):
        if myRelationship.guid != None:
            self.relationships[myRelationship] = myRelationship.modelObject
        else:
            self.relationships[myRelationship] = None


    ######################################################
    def deleteRelationships(self,sources,targets,relationshipName,relGuids=[]):
        global force
        self.populate(sources,targets,relationshipName,relGuids)
        
        guids = []
        for rel in self.relationships.keys():
            guids.append(rel.guid)   

        if len(guids) == 0:
            raise Exit("There are no relationships to delete.")
        delete = None
        if force != True:
            printit("About to delete relationships:")
            self.showDetails()        
            delete, deleteAll = promptUser("Are you certain that you want to delete these relationships")    
        
        if force == True or delete == True:
            api.delete(guids,None)
            printit("Deleted relationships")
    
        #self.showDetails()

    
    ######################################################
    def list(self,sources,targets,relationshipName,relGuids=[]):
        self.populate(sources,targets,relationshipName,relGuids)
        
        if self.getCount() > 0:
            if relationshipName == None:
                relationshipLabel =  "relationships"
            else:
                relationshipLabel =  relationshipName + " relationships"
    
            printit("Existing " + relationshipLabel + " are: ")    

            self.showDetails()
        else:
            printit("No relationships found")
    
    
    ######################################################
    def hasRelationship(self,myRelationship):
        ret = False
        if myRelationship in self.relationships:
            ret = True
        return ret
    
    ######################################################
    def getRelationships(self):
        return self.relationships
    
    
    ######################################################
    def showDetails(self):
        global relationshipName

        for rel in self.relationships.keys():
            guid = str(rel.guid)            
            sClass = align(rel.sourceShortClass,20)
            sName = align(rel.sourceName,40)
            rType = align(rel.shortRelationshipType,20)
            tClass = align(rel.targetShortClass,20)
            tName = align(rel.targetName,40)
            
            
            printit("\t" + guid + ":\t" + sClass + "\t" + sName+  "\t" + rType + "\t" + tClass + "\t" + tName) 

            
###############################################################################
###############################################################################
class myRelationship:

    def __init__(self,relationship):
        self.modelObject = relationship
        log.debug("\tExisting relationship is: " + str(self.modelObject))                            
        self.guid = self.modelObject.getGuid()        
        self.longType, self.shortType = taddmJythonApiHelper.getClassNames(self.modelObject)        
        self.sourceLongClass, self.sourceShortClass = taddmJythonApiHelper.getClassNames(self.modelObject.source)
        self.sourceGuid = str(self.modelObject.source.guid)
        self.sourceName = str(self.modelObject.source.displayName)
        self.targetLongClass, self.targetShortClass = taddmJythonApiHelper.getClassNames(self.modelObject.target)
        self.targetGuid = str(self.modelObject.target.guid)
        self.targetName = str(self.modelObject.target.displayName)
        self.longRelationshipType = self.modelObject.type
        splits = re.split(r'\.',self.longRelationshipType)
        self.shortRelationshipType = splits[len(splits)-1]
        
        #log.debug("The " + self.shortType + " relationship between " + self.sourceShortClass + ":" + str(source.getGuid()) + " and " + self.targetShortClass + ":" + str(target.getGuid()) + " already exists. Relationship guid is " + str(self.guid))

        myRelationships.add(self)


            
###############################################################################
###############################################################################
def show_help():
    pref = "\t\t"
    delim = "\t\t"
    print ""
    print "\tUsage: " + prog + " OPTIONS   -a ACTION   ACTION_OPTIONS    ACTION_PARAMETERS"
    print ""
    print pref + "OPTIONS:"
    print pref + "    Mandatory:"
    print pref + "\t-p, --password <password that authenticates this user>"
    print pref + "    Optional:"
    print pref + "\t-u, --user <user to perform the action as>. If none is provided 'administrator' is used."
    print pref + "\t-H, --host <host the TADDM server is installed on, defaults to localhost>"
    print pref + "\t-P, --port <port the TADDM server public service registry is listening on, defaults to 9433>"
    #print pref + "\t-h, --help <This help>"
    print ""
    print pref + "ACTION:\t list|crate|delete|help"
    print pref + "\tlist\t List all relationships for the resources identified through the sourceQuery or targetQuery, and relatioshipName arguments.(default)"
    print pref + "\tcreate\t Create new relationships for the resources identified through the sourceQuery, targetQuery and relatioshipName arguments." 
    print pref + "\tdelete\t Delete relationships identified through the sourceQuery or targetQuery, and optionally relationshipName arguments."
    print pref + "\thelp\t This help."
    print ""
    print pref + "ACTION-OPTIONS:"
    print pref + "\tcreate:\t -s|--sourceQuery <MQLQuery>|<GUID> -t|--targetQuery <MQLQuery>|<GUID> -r|--relationshipName <relationshipName>"    
    print pref + "\tdelete:\t[ [-s|--sourceQuery <MQLQuery>|<GUID>] | [-t|--targetQuery <MQLQuery>|<GUID>] | [-s|--sourceQuery <MQLQuery>|<GUID>  -t|--targetQuery <MQLQuery>|<GUID> ] ] [-r|--relationshipName <relationshipName>] ] | -g|--relationshipGuid <GUID>"    
    print pref + "\tlist:  \t[ [-s|--sourceQuery <MQLQuery>|<GUID>] | [-t|--targetQuery <MQLQuery>|<GUID>] | [-s|--sourceQuery <MQLQuery>|<GUID>  -t|--targetQuery <MQLQuery>|<GUID> ] ] [-r|--relationshipName <relationshipName>] ] | -g|--relationshipGuid <GUID>"    
    print " "
    print pref + "\t-s|--sourceQuery <MQLQuery>|<GUID>\tSpecifies the resources that will be used as targets for the relationships."    
    print pref + "\t-t|--targetQuery <MQLQuery>|<GUID>\tSpecifies the resources that will be used as targets for the relationships."    
    print pref + "\t-r|--relationshipName <relationshipName>\tIdentifies the type of the relationships."
    print pref + "\t-g|--relationshipGuid <GUID>\t\tIdentifies the guid of the relationship to be deleted."
    print " "    
    print pref + "\t<MQLQuery>\t\tA valid MQL Query that idenitfies resources."   
    print pref + "\t<GUID>\t\t\tA GUID that represents a single resource."
    print pref + "\t<relationshipName>\tUse the short form of the relationshipName. For example 'Requires', 'Uses', 'Federates', or 'Contains' "
    print ""
    print pref + "ACTION-PARAMETERS:"
    print pref + "\t-f|--force"+delim + "Forces the deletion of existing resources without user confirmation."
    print pref + "\t-q|--quiet"+delim + "Suppresses output to the console, and user confirmations. If the -f|--force option is not used, all user confirmations will be rejected."
    print pref + "\t-D|--debug"+delim + "Sets the loglevel to debug."
    print pref + "\t-T|--trace"+delim + "Enables log messages to be displayed in the console."
    print pref + "\t-h|--help"+delim + "Shows this help."
    print ""
    print "\tLog messages can be found in " + coll_home + "/log/" + prog + ".log."
    print " "
    print "\tEXAMPLES:"
    print ""
    print pref+"List a relationship:"
    print pref+"\t"+prog+" -u administrator -p collation -a list -g <guid>"
    print ""
    print pref+"List all relationships for source resources identified by a query:"
    print pref+"\t"+prog+" -u administrator -p collation -a list -s 'select guid from Application'" 
    print ""
    print pref+"List all Contains relationships for a single resources identified by guid:"
    print pref+"\t"+prog+" -u administrator -p collation -a list -s <guid> -r Contains" 
    print ""
    print pref+"Delete all relationships between resources identified by queries:"
    print pref+"\t"+prog+" -u administrator -p collation -a delete -s 'select guid from Application' -t 'select guid from J2EEApplication'" 
    print ""
    print pref+"Create a Requires relationships between resources identified by queries without prompting the user for confirmation:"
    print pref+"\t"+prog+" -u administrator -p collation -a delete -s 'select guid from Application' -t 'select guid from J2EEApplication' -r Requires -f" 






    raise SystemExit()



###############################################################################        
def analyzeQuery(query):
    queryType = "query"
    splits = re.split(" ",query)
    if len(splits) == 1:            # we are dealing with a guid
        queryType = "guid"    
    else:
        i = 0
        for f in splits:
            if string.upper(f) == "FROM":
                break
            i = i + 1
        query = "select displayName, guid"

        while i < len(splits):
            query = query + " " + splits[i]
            i = i + 1
                   
    return queryType, query

###############################################################################        
def findModelObjects(query):
    
    queryType, query = analyzeQuery(query)
    log.debug("\tExecuting query: " + query)
    if queryType == "query":
        modelObjects = api.find(query,1,None,None)
    else:
        guid = Guid(query)
        modelObjects = []
        try:
            modelObjects.append(api.find(guid,1,None))    
        except:
            pass

    #if len(modelObjects) == 0:
    #    raise Exit(0,"No modelObjects found for query: " + query)
    
    return modelObjects

###########################################################
def runRelationshipQuery(source, target, relType,relGuid=None):
    query = "select source, target, type, guid, source.displayName, target.displayName  from Relationship where "   
    
    if relGuid != None:
        query = query + "Relationship.guid == '" + str(relGuid.getGuid()) + "' "
    else:
        if source != None:
            query = query + "Relationship.source.guid == '" + str(source.getGuid()) + "' "
            if target != None or relType != None:
                query = query + " and "
        if target != None:
            query = query + "Relationship.target.guid == '" + str(target.getGuid()) + "'"
            if relType != None:
                query = query + " and "
        if relType != None:
            #query = query + "type == 'com.collation.platform.model.topology.relation." + relType + "'" 
            query = query + "type IN ('com.collation.platform.model.topology.relation." + relType + "','com.collation.platform.model.topology.app.dependencies." + relType + "') " 
    log.debug("Fetching relationship data")
    log.debug("Executing query: " + query)                        
    relationshipObjects = api.find(query,2,None,None)

    return relationshipObjects

################################################
def printit(msg):
    if quiet != True:
        log.info(msg)
        print msg
    
    

################################################
def align(value,length):
    
    i = len(value)
    while i <= length:
        value = value +"\t"
        length = length - 7        
    return value
    

###############################################################################        
###############################################################################
###############################################################################

def main(argv=None):

    
    global prog,dirname,progname,log,trace,coll_home    
    global api,conn,sess,debug,log
    global category, name, value
    global myRelationships, action
    global relationshipName, force, debug, trace, quiet
    
    quiet = False
    force = False
    debug = False
    trace = False
    optMsg = None
    

    log,prog = taddmJythonApiHelper.init()    
    coll_home = getCollHome()    
    
    if argv is None:
        argv = sys.argv
    
                            
    
    taddmServerPort = -1
    taddmServerHost = "localhost"
    taddmServerUser = "administrator"
    taddmServerPassword = None

    action = "list"
    sourceQuery = None
    targetQuery = None
    relationshipName = None
    relationshipGuid = None


    #############################
    #  Set logging
    #############################
    ##log = setLogging()



    
    ####################################################################
    #    get arguments
    ####################################################################
    if True == True:   #try:
               
        shortOpts = "a:Dfg:hH:p:P:qr:s:Tt:u:"
        longOpts = ["action","debug","force","relationshipGuid=","help","host=","password=","port=","quiet","relationshipName=","sourceQuery=","trace","targetQuery=","user="]
                
        opts = {}
        args = {}
        
        try:        
            opts, args = getopt.getopt(argv[1:], shortOpts, longOpts)
        except GetoptError, opt_ex:
            raise Usage(opt_ex.msg)    

        
        for o, a in opts:
            o = string.strip(o)

            if o in ("-a", "--action"):
                a = string.strip(a)
                action = string.lower(a)
                if action == "help":
                    show_help()

            elif o in ("-D", "--debug"):
                debug = True

            elif o in ("-f", "--force"):
                force = True

            elif o in ("-g", "--relationshiGuid"):
                relationshipGuid = string.strip(a)

            elif o in ("-h", "--help"):
                raise Usage("help")

            elif o in ("-H", "--host"):
                taddmServerHost = string.strip(a)

            elif o in ("-p", "--password"):
                taddmServerPassword = string.strip(a)

            elif o in ("-P", "--port"):
                taddmServerPort = int(a)

            elif o in ("-q", "--quiet"):
                quiet = True

            elif o in ("-r", "--relationshiName"):
                #name = string.lower(string.strip(a))
                #relationshipName = string.upper(name[0]) + name[1:]
                relationshipName = string.strip(a)

            elif o in ("-s", "--sourceQuery"):
                sourceQuery = string.strip(a)

            elif o in ("-T", "--trace"):
                trace = True

            elif o in ("-t", "--targetQuery"):
                targetQuery = string.strip(a)

            elif o in ("-u", "--user"):
                taddmServerUser = string.strip(a)                

            else:
                raise Usage("You provided an unknown option: " + str(o))

        
            if len(args) > 0 and len(opts) > 0:
                a = string.strip(str(opts[len(opts) - 1]), "(")
                a = string.strip(a, ")")
                x, y = string.split(a, ",", 1)
                a = string.strip(x, "'") + " " + string.strip(y, "'")
                raise Exit(4, "Your input was not parsed correctly. The problem is likely related to the '" + str(args[0]) + "' argument number following '" + a + "'") 

        #############################
        #  validation arguments
        #############################        
        
        msg = "You must provide input arguments to " + prog
        
        if optMsg == None:

            msg = None
            
            if sourceQuery == None and targetQuery == None and relationshipName == None:
                msg = "You must, as a minimum, provide a value for one of the sourceQuery(-s), targetQuery(-t) arguments."

            if action == "create":
                if sourceQuery == None:
                    msg = "You must provide a value for the sourceQuery(-s) argument. Provide an MQLQuery or a Guid."

                if targetQuery == None:
                    msg = "You must provide a value for the targetQuery(-t) argument. Provide an MQLQuery or a Guid."

                if relationshipName == None:
                    msg = "You must provide a relationshipName for the relationship."

            if action == "delete":
                if sourceQuery == None and targetQuery == None: 
                    if relationshipGuid != None:
                        msg = "You must provide a value for either the sourceQuery(-s) or targetQuery(-t) argument. Provide an MQLQuery or a Guid."
        
            #if taddmServerHost == None:
            #    msg = "You MUST provide a host name of ip address of the TADDM storage server using the '-H' or '--host' argument."

            #if taddmServerPort == None:
            #    msg = "You MUST provide a port number used to connect the TADDM storage server using the '-P' or '--port' argument."

            #elif taddmServerUser == None:
            #    msg = "You MUST provide a user name using the '-u' or '--user' arguments."

            if taddmServerPassword == None:
                msg = "You MUST provide password using the '-p' or '--password' arguments."


        if msg != None:
            raise Usage(msg)
        


    
    
    #####################################################
    #####################################################
    ##
    ##  DO IT
    ## 
    #####################################################
    #####################################################
                
    # Setup logging                
    log = taddmJythonApiHelper.setupLog4jLogging(trace,debug)
    

    # connect to TADDM
    api = taddmJythonApiHelper.connectToTaddm(taddmServerHost, taddmServerPort,taddmServerUser, taddmServerPassword)
    
    # initialize tuple to keep instances        
    
    try:
    
        relGuids = []
        sources = []
        targets = []

        if relationshipGuid != None:
            log.info("Fetching relationshipGuid: " + relationshipGuid )
            relGuids = findModelObjects(relationshipGuid)                
            if relationshipGuid != None:
                if len(relGuids) == 0:
                    raise Exit(0,"Relationship Guid '" + relationshipGuid +"' does not exist.")
                else:
                    log.debug("Found " + str(len(relGuids)) + " relationships for " + str(relationshipGuid))        
        else:
            
            if sourceQuery != None:
                log.info("Fetching source modelObject from query: " + sourceQuery + ".")
                sources = findModelObjects(sourceQuery)        
                #if len(sources) == 0:
                #    raise Exit(4,"No source resources were found by query '" + sourceQuery + "'")
            
            if targetQuery != None:
                log.info("Fetching target modelObject from query: " + targetQuery)
                targets = findModelObjects(targetQuery)
                #if len(targets) == 0:
                #    raise Exit(4,"No source resources were found by query '" + sourceQuery + "'")
        
            if sourceQuery != None:                
                if len(sources) == 0:
                    raise Exit(0,"Source query '" + sourceQuery+"' did not produce any results.")
                else:
                    log.info("Found " + str(len(sources)) + " sources for " + str(sourceQuery))
    
            if targetQuery != None:
                if len(targets) == 0:
                    raise Exit(0,"Target query '" + targetQuery+"' did not produce any results.")
                else:
                    log.info("Found " + str(len(targets)) + " targets for " + str(targetQuery) + ".")
    

    
        if (len(sources) == 0) and (len(targets) == 0) and (relationshipName == None) and len(relGuids) == 0: 
            raise Exit(4,"You did not specify any search argument in either of the source, target or type arguments")


        myRelationships = myRelationships()

        if action == "list":
            myRelationships.list(sources,targets,relationshipName,relGuids)

        elif action == "create":
            myRelationships.newRelationships(sources,targets,relationshipName)
                    
        elif action == "delete":
            myRelationships.deleteRelationships(sources,targets,relationshipName,relGuids)
                                     
        raise SystemExit
    
    except Quit, quit_ex:
        if quit_ex.rc == 0:
            printit("\n" + prog + " ended  sucessfully")
        SystemExit()

    except Exit, exit_ex:
        printit(exit_ex.msg)
        #printit("("+str(exit_ex.rc)+") " + exit_ex.msg)        
        ##exit_ex.leave()
        raise SystemExit(exit_ex.rc)    
    
    except SystemExit,sys_ex:
        #printit "---- " + str(sys_ex)
        sys.exit(sys_ex)

    except:
        
        traceB=traceback.format_exc()
        
        msg = "Fatal Error: " + str(sys.exc_info())
        printit(msg)
        log.error(msg)
        log.error(traceB)
                
        if not string.find(str(sys.exc_info()[0]), "Exit"):
            printit >> sys.stderr, "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        
        #sys.exit(main())                
        sys.exit()
        



tracer = None
# tracer = trace.trace(ignoredirs=[sys.prefix, sys.exec_prefix], trace=1, count=2)


if __name__ == "__main__":
    if not tracer == None:
        sys.exit(tracer.run('main()'))
    else:    
        sys.exit(main())
