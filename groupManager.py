#!/usr/bin/env ../../bin/jython_coll
#
# It is assumed that this user script is located in a directory
# which is not part of the standard TADDM directory structure.
# This minimizes the risk of removing the script inadvertently as part of an upgrade.
#
# To launch the TADDM jython environment, the first line should point to the 
# jython_coll script in the $COLLATION_HOME/bin directory. 
# Use the relative location of the directory to initialize the environment.
#
# If for example, the script is stored in /opt/IBM/taddm/usr/bin
# use the following path to launch the jython_coll script
#    ../../dist/bin/jython_coll 
#
##/usr/bin/env ../../dist/bin/jython_coll 
#######/usr/bin/env jython

import taddmJythonApiHelper

from taddmJythonApiHelper import *

    


#######################################################################################################
#######################################################################################################
class taddmSuper:
    
    #########################################################################
    def __init__(self,modelObject,parent):

        self.adminInfo = []
        self.userData = []
        self.relationships = []
        self.userDataInfo = {}
        self.userDataAttrMeta = None
        ##  MMMMMMMMMMMMMMMMMMMMM   setControls(self)
        self.modelObject = modelObject
        self.parent = parent
        
        # 
        log.debug("Processing modelObject:\t" + str(self.modelObject))
        self.className = str(self.modelObject.__class__.canonicalName)
        self.longClass = self.className[0:len(self.className)-4]
        c = re.split("\.",self.longClass)
        self.shortClass = c[len(c)-1]
        
        #self.attributes = getModelObjectAttributes(modelObject)
        self.findTaddmAttributes()
        #if includeExtendedAttributes == True:
        self.findExtendedAttributes() 
        #if includeAdminInfo == True:
        self.findAdminInfo()
        #if includeUserData == True:
        self.findUserData()
        #if includeRelationships == True:
        self.findRelationships()
        #
        self.guid = self.modelObject.getGuid()
        
    #########################################################################        
    def list(self):
        print("******   ModelObject:\t" + str(self.modelObject))
        print("******   Attributes:\t" + str(self.attributes))        
        print("******   ExtendedAttr:\t" + str(self.extendedAttributes))        
        print("******   AdminInfo:\t" + str(self.adminInfo))        
        print("******   ShortClass:\t" + str(self.shortClass))        
        print("******   guid:\t" + str(self.guid))        
        print("******   name:\t" + str(self.name))        

    #############################################################
    def addUserData(self,modelObject):
        self.userData.append(modelObject)
        
    #############################################################
    def addAdminInfo(self,modelObject):
        self.adminInfo.append(modelObject)

    #############################################################
    def findTaddmAttributes(self):

        # get the metadaa to be able to list all attributes         
        meta = api.getMetaData(self.shortClass,True)
        self.attributeNames = meta.getObjectAttributes()   
        
        modelObjectAttributes={}        
        #list the attributes and get the values 
        numAttr = 0
        numVal = 0
        for attr in self.attributeNames:
        
            numAttr = numAttr + 1    
            hasMethodName = "has" + string.upper(attr.name[0]) + attr.name[1:]
            hasMethod = getattr(self.modelObject,hasMethodName)
            value = ""
            if hasMethod():
                getMethodName = "get" + string.upper(attr.name[0]) + attr.name[1:]        
                getMethod = getattr(self.modelObject,getMethodName)
                value = getMethod()
                numVal = numVal + 1    
            log.debug("\t" + str(attr.name) + ":\t'" + str(value) + "'\t(" + attr.type + ")")
            modelObjectAttributes[attr.name] = [value, attr.type, attr.arrayType,attr.timestampType,attr.length,attr.displayString] 
               
        log.debug("modelObjectAttributes:\t" + str(modelObjectAttributes))
        self.attributes = modelObjectAttributes            

    #########################################################################
    def findExtendedAttributes(self):
        
        self.extendedAttributes = None    

        if includeExtendedAttributes == True:
            print "-----\t\t"+self.shortClass+" '"+self.name+"' hasExtendedAttributes?\t " + str(self.modelObject.hasExtendedAttributes())
            print "-----\t\t"+self.shortClass+" '"+self.name+"' getExtendedAttributes?\t " +str(self.modelObject.getExtendedAttributes())
            
        if self.modelObject.hasExtendedAttributes():
            self.extendedAttributes = self.modelObject.getExtendedAttributes()

            log.debug("EXTENDED ATTR: " + str(self.extendedAttributes.__class__) + "  " + str(self.extendedAttributes))
                
    
    
    #########################################################################
    def findAdminInfo(self,flatten=True):
        self.adminInfo = []
        
        if includeAdminInfo == True:
            log.debug("Getting adminInfo for " + self.shortClass)

            query = "select * from AdminInfo where objGuid equals '" + str(self.modelObject.getGuid()) + "'"
            adminInfoList = api.find(query,flatten, None,None)
    
            log.debug("AdminInfo for " + self.name +  " (" + self.shortClass + ") is: " + str(adminInfoList))
    
            if len(adminInfoList) == 0:
                log.debug("No AdminInfo found for " + self.shortClass + " " + self.name)
            else:
                taddmAdminInfo(adminInfoList[0],self)
                  
        if self.adminInfo == []:
            self.adminInfo = None

    #########################################################################
    def findUserData(self,flatten=True):
        
         
        self.userData = []       
        if includeUserData == True:

            userDataAttrMeta = api.find("select attrName, attrType,mappedAttrName from UserDataAttributeMeta where UserDataAttributeMeta.parent.guid == UserData.metaRef.guid and UserData.objRef == '" + str(self.modelObject.getGuid()),flatten,None,None)
            for attrMeta in userDataAttrMeta:
                attrName = attrMeta.getAttrName()
                mappedAttr = attrMeta.getMappedAttrName()
                
                
                userDataObjects = api.find("Select * from UserData where objRef == '" + str(self.modelObject.getGuid()) + "'",flatten,None,None)
                
                for userData in userDataObjects:
                    taddmUserData(userData,self)
                    self.userDataAttrMeta = attrMeta
                    self.getUserDataInfo()
                
    
            if self.userData == []:
                self.userData = None
    
            log.debug("USER DATA: " + self.shortClass +":" + str(self.name) + "\t" + str(self.userData))
                

    #########################################################################
    def findRelationships(self,flatten=True):
        
        self.relstionships = []
        if includeRelationships == True:
            relationshipObjects = api.find("select * from Relationship where (Relationship.source.guid == '" + str(self.modelObject.getGuid()) + "') or (Relationship.target.guid  == '" + str(self.modelObject.getGuid()) + "')",flatten,None,None)
           
            for rel in relationshipObjects:
                relTypeParts = re.split("\.",rel.getType())
                relType = relTypeParts[len(relTypeParts)-1]
                # filter out MemberOf relationships
                if relType != "MemberOf": 
                    #self.relationships.append(rel)
                    taddmRelationship(rel,self)
            if self.relationships == []:
                self.relationships = None
                    
            log.debug("RELATIONSHIPS: " + self.shortClass +":" + str(self.name) + "\t" + str(self.userData))
                

    ###############################################################################

    def cloneModelObject(self,newNamingAttributes):
        updateObjects = []           
        log.info("Creating new " + self.shortClass)
        print "\tCloning " + self.shortClass
        self.newObject = ModelObjectFactory.newInstance(Class.forName(self.longClass))
    
        log.debug(""+self.shortClass + "\tnewNamingAttributes:\t"+str(newNamingAttributes))
        
        for attr in newNamingAttributes.keys():
            attributName = string.upper(attr[0]) + attr[1:]
            setMethodName = "set" + attributName
            setMethod = getattr(self.newObject,setMethodName)
            log.info(self.shortClass + "\tUpdating naming attribute: '" + attr + "'.\tNew value is: '" + str(newNamingAttributes[attr]) + "'")
            setMethod(newNamingAttributes[attr])
            
        
        for attr in self.cloneAttributes:            
            #log.debug("\t\tupdating attributes for ("+ str(self.newGuid) + "):\t" + str(self.newObject))
            if attr in self.attributes.keys() and attr not in newNamingAttributes.keys():
                #validAttribs.index(attr)
                cloneAttribute(self,attr)

        # save the updates
        self.newGuid = api.update(self.newObject, None)
        log.debug(self.shortClass + "\tupdated object ("+ str(self.newGuid) + "):\t" + str(self.newObject))
        # refresh the object to include the system-managed attributes
        self.newObject = api.find(self.newGuid,3,None)


        if includeAdminInfo == True and self.adminInfo != None:
            print "\t\tCloning AdminInfo"
            for adminInfo in self.adminInfo:
                newNamingAttributes = {}
                newNamingAttributes["name"] = self.newObject.getName()
                newNamingAttributes["objGuid"] = self.newObject.getGuid()

                ## clone the existing AdminInfo object
                adminInfo.newObject = ModelObjectFactory.newInstance(adminInfo.modelObject,1)
                ## update the new copy
                for attr  in newNamingAttributes.keys():
                        methodName = string.upper(attr[0]) + attr[1:]                    
                        setMethodName = "set" + methodName        
                        setMethod = getattr(adminInfo.newObject,setMethodName)
                        setMethod(newNamingAttributes[attr])
                ## add additional adminInfo attributes
                for attr in adminInfo.attributes.keys():                    
                    if (not attr in newNamingAttributes.keys()) and (attr in adminInfo.cloneAttributes):
                        cloneAttribute(adminInfo, attr)   
                                     
                updateObjects.append(adminInfo.newObject)

        if includeUserData == True and self.userData != None:
            print "\t\tCloning UserData"
            self.newUserData = []

                    
            for userData in self.userData:
                newNamingAttributes = {}
                newNamingAttributes["objRef"] = self.newObject.getGuid()
                
                ## clone the existing UserData object
                userData.newObject = ModelObjectFactory.newInstance(Class.forName("com.collation.platform.model.topology.extattrib.UserData"))
                ## update the new copy
                for attr in newNamingAttributes.keys():
                    methodName = string.upper(attr[0]) + attr[1:]                    
                    setMethodName = "set" + methodName        
                    setMethod = getattr(userData.newObject,setMethodName)
                    setMethod(newNamingAttributes[attr])
                for attr in userData.attributes.keys():                    
                    if (not attr in newNamingAttributes.keys()) and (attr in userData.cloneAttributes):
                        cloneAttribute(userData, attr)   
                
                
                self.newUserData.append(userData.newObject)         
                updateObjects.append(userData.newObject)
                updateObjects.append(self.newObject)
        
        
        

        if includeRelationships == True and  self.relationships != None:
            log.debug("\t\tCloning Relationships")
            self.newRelationships = []
            
                    
            for relationship in self.relationships:
                newNamingAttributes = {}
                                
                if relationship.modelObject.getSource().getGuid() == self.guid:                
                    newNamingAttributes["source"] = self.newObject
                else:                
                    newNamingAttributes["target"] = self.newObject
                
                ## clone the existing UserData object
                relationship.newObject = ModelObjectFactory.newInstance(Class.forName("com.collation.platform.model.topology.core.Relationship"))
                ## update the new copy
                for attr in newNamingAttributes.keys():
                    methodName = string.upper(attr[0]) + attr[1:]                    
                    setMethodName = "set" + methodName        
                    setMethod = getattr(relationship.newObject,setMethodName)
                    setMethod(newNamingAttributes[attr])                    
                for attr in relationship.attributes.keys():                    
                    if (not attr in newNamingAttributes.keys()) and (attr in relationship.cloneAttributes):                        
                        cloneAttribute(relationship, attr)   
                
                self.newRelationships.append(relationship.newObject)         
                updateObjects.append(relationship.newObject)
                updateObjects.append(self.newObject)
        
            
        # persist updates
        if updateObjects != []:            
            api.update(updateObjects,None)
            
    ###############################################################################            
    def getUserDataInfo(self):    
        # extract user data information
        ###########        
        attrName = self.userDataAttrMeta.getAttrName()
        attrType = self.userDataAttrMeta.getAttrType()
        mappedAttr = self.userDataAttrMeta.getMappedAttrName()
        mappedAttrName = string.upper(mappedAttr[0]) + mappedAttr[1:]

        # get category
        hasMethod = getattr(self.userData[0].modelObject,"hasCategory")
        if str(hasMethod()) == "True": 
            getMethod = getattr(self.userData[0].modelObject,"getCategory")
            category = getMethod()
        else:
            category = "None"

        # get value
        hasMethodName = "has" + mappedAttrName
        hasMethod = getattr(self.userData[0].modelObject,hasMethodName)
        if str(hasMethod()) == "True": 
            getMethodName = "get" + mappedAttrName
            getMethod = getattr(self.userData[0].modelObject,getMethodName)
            value = getMethod()
        else:
            value = ""
            
        log.debug("" + self.shortClass + "\tGetting UserData for: '" + mappedAttr + "'.\tValue is: '" + str(value) + "'")
        self.userDataInfo[mappedAttr] = [category,attrName,attrType,value]

    #########################################################################
    def addRelationship(self,relationship):
        self.relationships.append(relationship)




#######################################################################################################
#######################################################################################################
class taddmObject(taddmSuper):

    #########################################################################
    def __init__(self,modelObject,parent):
        if self.name == None: 
            self.name = modelObject.getName()  
        taddmSuper.__init__(self,modelObject,parent)    
        self.parent.addFunctionalGroup(self)
        self.list()


#######################################################################################################
#######################################################################################################
class taddmSuperGroup(taddmSuper):

    #########################################################################
    def __init__(self,modelObject,parent):
        self.applicationDef = None
        self.appTemplate = None
        self.functionalGroups = []
        
        
        self.name = modelObject.getName()  
        taddmSuper.__init__(self,modelObject,parent)    
        # get the application definition        
        self.findApplicationDef()
        # get the functional groups        
        self.findFunctionalGroups()
        # get the application template        
        self.findAppTemplate()



    #########################################################################
    def findApplicationDef(self):
        
        if self.__class__.__name__ == "taddmApplication":
            if self.modelObject.hasAppDef():            
                log.info("ApplicationDef for group '" + self.name + "' of type " + self.shortClass + " exists: " + str(self.modelObject.hasAppDef()))
                resourceFilter = "name equals '" + oldGroupName + "'"            
                modelObjects = getModelObjectsFromQuery("ApplicationDef",resourceFilter)
            
                if len(modelObjects) == 0:
                    log.info("AplicationDef for group '" + self.name + "' of type " + self.shortClass + " was not found.")
                else:
                    taddmApplicationDef(modelObjects[0],self)
                    #oldApplicationDefObject.list()

    #########################################################################
    def addApplicationDef(self,appDef):
        self.applicationDef = appDef

    #########################################################################
    def findFunctionalGroups(self):
        
        resourceFilter = "app.guid equals '" + str(self.modelObject.getGuid()) + "'"            
        modelObjects = getModelObjectsFromQuery("FunctionalGroup",resourceFilter)
        if len(modelObjects) == 0:
            log.debug("No functionalGroups found for " + self.shortClass + " '" + self.name + "'")
        else:
            for fgModelObject in modelObjects:       
                taddmFunctionalGroup(fgModelObject,self)

    #########################################################################
    def addFunctionalGroup(self,fg):
        self.functionalGroups.append(fg)

    #########################################################################
    def findAppTemplate(self):
        
        resourceFilter = "appTemplateName equals '" + str(self.modelObject.getGuid()) + ":" + str(self.modelObject.getName()) + "'"            
        modelObjects = getModelObjectsFromQuery("AppTemplate",resourceFilter)
        if len(modelObjects) == 0:
            log.debug("Apptemplate for group '" + self.name + "' of type " + self.shortClass + " was not found.")
        else:
            for appTemplate in modelObjects:       
                taddmAppTemplate(appTemplate,self)

    #########################################################################
    def addAppTemplate(self,appTmpl):
        self.appTemplate = appTmpl



    #########################################################################
    def listResults(self):
    
        print("\n===========================================================================")
        print("RESOURCE TYPE: " + self.shortClass)
        print("===========================================================================")
        
        show_details(self,None)
        #show_details(self,self.attributes,self.extendedAttributes, self.adminInfo,self.adminInfo.attributes)
        if self.applicationDef != None:                
            show_details(self.applicationDef,1)
        if self.functionalGroups != None:      
            for functionalGroup in self.functionalGroups:                                        
                show_details(functionalGroup,1)
        if self.appTemplate != None:      
            show_details(self.appTemplate,1)
            #for oldMQLRuleObject in oldMQLRuleObjects:                                        
            #    show_details(oldMQLRuleObject,oldMQLRuleObjects[oldMQLRuleObject])
        if self.appTemplate  != None:      
            if self.appTemplate.MQLRules != None:      
                for MQLRule in self.appTemplate.MQLRules:                                        
                    show_details(MQLRule,2)
        

    #############################################################
    def delete(self,force=False):
        
        if force == False:
            force,deleteAll = promptUser("Are you sure that you want to delete " + self.shortClass + " '" + self.name + "' ?")    
    
        if force == True:
            log.debug("About to delete "  + self.shortClass + " '" + self.name + "'")    
            num = api.delete([self.modelObject],None)
            log.debug("Deleted " + str(num) + " objects.")
    


    #########################################################################
    def clone(self,newGroupName):
        global force
        #global includeAdminInfo
        #global includeExtendedAttributes
        #global includeRelationships
        #global includeUserData
        #global modifyRyles
        #global overwriteGroupName
        # figure out if newName already exists
                        
        resourceFilter = "displayName equals '" + newGroupName + "'"                        
        modelObjects = getModelObjectsFromQuery(self.shortClass,resourceFilter,True)

        doit = True
        if len(modelObjects) > 0:
            if force == False:
                force, self.deleteAll = promptUser(self.shortClass + " '" + newGroupName + "' exists. Do you want to replace it?")
                doit = False
            
            if force == True:
                tempGroupObject = taddmSuperGroup(modelObjects[0],None)
                tempGroupObject.delete(force)
                doit = True
                
        if doit == False:
            print "Operation cancelled."
            log.info("User cancelled the operation.")    
        else:    
            ####################################################
            ####################################################
            ## clone the existing group object
            newObjectList = []
            ## The Application object must be created so the GUID can be used to name FunctionalGroupsand AppTEmplates
            newNamingAttributes = {}
            newNamingAttributes["name"]=newGroupName
            newNamingAttributes["label"]=newGroupName
    
            self.cloneModelObject(newNamingAttributes)
            newGroupObject = self.newObject
            #newGroupObjectGuid=api.update(newGroupObject,None)
            #log.debug("newGroupObjectGuid:\t" + str(newGroupObjectGuid))
            newObjectList.append(self.newObject)
                    
            ## Clone ApplicationDef objects for applications
            ## This must also be created to avoid GUI error messages when editing the application
            if self.applicationDef != None: 
                newNamingAttributes = {}             
                newNamingAttributes["name"]=newGroupName
                newNamingAttributes["label"]=newGroupName
                    
                self.applicationDef.cloneModelObject(newNamingAttributes)
                     
                newObjectList.append(self.applicationDef.newObject)
                ## update references
                    
            if self.appTemplate == None:
                ## Clone FunctionalGroup objects for applications that are not based on an AppTemplate
                log.debug("oldFunctionalGroupObjectList:\t" + str(self.functionalGroups))
                newFunctionalGroups = []
                if self.functionalGroups != None and self.functionalGroups != []:                     
                    newNamingAttributes = {}             
                        
                    for functionalGroup in self.functionalGroups:
                        newNamingAttributes["groupName"]=functionalGroup.modelObject.getGroupName()
                        newNamingAttributes["app"]=newGroupObject                        
                            
                        functionalGroup.cloneModelObject(newNamingAttributes)
                    
                        newObjectList.append(functionalGroup.newObject)
                        newFunctionalGroups.append(functionalGroup.newObject)
                    ### update the members attribute in the application
                    hasMethod = getattr(newGroupObject,"hasGroups")
                    if hasMethod():
                        log.debug("Updating Functionalgroups in groupObject: " +str(newGroupObject))
                        newGroupObject.setGroups(newFunctionalGroups)
                    api.update(newGroupObject,None)
                    
                
            ## create the new appTemplate    
            elif self.appTemplate != None:
                newNamingAttributes = {}
                newNamingAttributes["appTemplateName"]=str(newGroupObject.getGuid()) + ":" + newGroupName
                newNamingAttributes["label"]=str(newGroupObject.getGuid()) + ":" + newGroupName
                    
                self.appTemplate.cloneModelObject(newNamingAttributes)
                    
                newObjectList.append(self.appTemplate.newObject)
    
                newMQLRules = []
                if len(self.appTemplate.MQLRules) > 0:                     
                    newNamingAttributes = {}                                 
                    for MQLRule in self.appTemplate.MQLRules:
                        newName = str(newGroupObject.getGuid()) + MQLRule.name[32:]
                        newNamingAttributes["MQLRuleName"]=newName
                        newNamingAttributes["label"]=MQLRule.name[32:]                        
                            
                        MQLRule.cloneModelObject(newNamingAttributes)
                        newObjectList.append(MQLRule.newObject)
                        newMQLRules.append(MQLRule.newObject)
                    ### update the members attribute in the application
                    log.debug("Updating MQLRules in appTemplate: " +str(self.appTemplate.newObject))
                    self.appTemplate.newObject.setMQLRules(newMQLRules)
                    api.update(self.appTemplate.newObject,None)
                    api.update(newGroupObject,None)
                    
            
            # update the objects with the latest references
            num = api.update(newObjectList,None)
            log.debug("Updated "+ str(num) + " resources")
                        
    
            newGroupObject = taddmGroup().populate(resourceType,newGroupName)
            newGroupObject.listResults()
    
            # rebuild the topology to populate the Functional Groups from the appTemplate
            #if self.rebuildTopology == True:
            log.info("Rebuilding topology")
            api.rebuildTopology()



#######################################################################################################
#######################################################################################################
class taddmApplication(taddmSuperGroup):

    def __init__(self,modelObject,parent):
        self.applicationDef = None
        self.appTemplate = None
        self.functionalGroups = []
        
        self.name = modelObject.getName()  
        self.cloneAttributes = ["CDMSource","CICategory","CIRole","URL","adminState","appDescriptors","appVersion","assetID","assetTag","cmdbSource","components","contact","containingSystem","contextIp","description","extendedAttributes","generalCIRole","installationNumber","isPlaceholder","licenseExpiryDate","lifecycleState","locationTag","managedSystemName","objectType","primaryOwner","roles","sourceToken","vendor"]
        taddmSuperGroup.__init__(self,modelObject,parent)    

    
#######################################################################################################
#######################################################################################################
class taddmCollection(taddmSuperGroup):

    def __init__(self,modelObject,parent):
        self.appTemplate = None
        self.functionalGroups = []
        
        self.name = modelObject.getName()  
        self.cloneAttributes = ["CDMSource","active","adminState","cmdbSource","contextIp","description","extendedAttributes","locationTag","managedSystemName","members","objectType","roles","sourceToken"]
        taddmSuperGroup.__init__(self,modelObject,parent)    

    
#######################################################################################################
#######################################################################################################
class taddmBusinessSystem(taddmSuperGroup):

    def __init__(self,modelObject,parent):        
        self.name = modelObject.getName()  
        self.cloneAttributes = ["CDMSource","CICategory","CIRole","URL","adminState","assetID","assetTag","businessImpact","businessPriority","businessRole","cmdbSource","components","contact","containingSystem","contextIp","description","extendedAttributes","generalCIRole","isPlaceholder","lifecycleState","locationTag","managedSystemName","objectType","primaryOwner","roles","sourceToken"] 
        taddmSuperGroup.__init__(self,modelObject,parent)    



#######################################################################################################
#######################################################################################################
class taddmGroup:

    def __init__(self):
        self.groupObject = None
        self.userData = []
        self.userDataAttrMeta = None
        
    def populate(self,groupType,groupName,parent=None):
        
        ################################################################                
        ## Get the group
        log.debug("Fetching data for " + groupType + " " + groupName)
            
        resourceFilter = "displayName equals '" + groupName + "'"                        
        self.modelObjects = getModelObjectsFromQuery(groupType,resourceFilter)

        if len(self.modelObjects) == 0:
            log.debug("Group '" + groupName + "' of type " + groupType + " was not found.")
            sys.exit()
        else:
            # save the object and gather information
                
            if groupType.lower() in ["service","businesssystem"]: 
                self.groupObject = taddmBusinessSystem(self.modelObjects[0],parent)
            elif groupType.lower() in ["application"]: 
                self.groupObject = taddmApplication(self.modelObjects[0],parent)
            elif groupType.lower() in ["collection"]: 
                self.groupObject = taddmCollection(self.modelObjects[0],parent)

        return self.groupObject


#######################################################################################################
#######################################################################################################
class taddmApplicationDef(taddmObject):

    def __init__(self,modelObject,parent):
        self.cloneAttributes = ["CDMSource","adminState","cmdbSource","contextIp","description","extendedAttributes","isPlaceholder","locationTag","managedSystemName","objectType","orgEntity","roles","serviceInstances","sourceToken"]
        self.name = modelObject.getName()  
        taddmSuper.__init__(self,modelObject,parent)    
        self.parent.addApplicationDef(self)

#######################################################################################################
#######################################################################################################
class taddmFunctionalGroup(taddmObject):

    #########################################################################
    def __init__(self,modelObject,parent):         
        self.cloneAttributes = ["active","adminState","CDMSource","contextIp","description","managedSystemName","memberType","members","modelObjects","objectType","operationalStatus","orgEntity","roles","serviceInstances","sourceToken"]        
        self.name = modelObject.getGroupName()  
        taddmSuper.__init__(self,modelObject,parent)    
        self.parent.addFunctionalGroup(self)
    
#######################################################################################################
#######################################################################################################
class taddmAppTemplate(taddmObject):

    #########################################################################
    def __init__(self,modelObject,parent):
                    
        self.cloneAttributes = ["CDMSource","adminState","appTemplateType","cmdbSource","contextIp","description","extendedAttributes","isPlaceholder","locationTag","managedSystemName","objectType","removeNonMembers","roles","sourceToken"]
        self.MQLRules = []
        self.name = modelObject.getAppTemplateName()  
        taddmSuper.__init__(self,modelObject,parent)    
        self.parent.addAppTemplate(self)
        # get the MQLRules
        self.findMQLRules()

    #########################################################################
    def findMQLRules(self):
        
        resourceFilter = "MQLRuleName starts-with '" + str(self.parent.modelObject.getGuid()) + "'"            
        modelObjects = getModelObjectsFromQuery("MQLRule",resourceFilter)
        if len(modelObjects) == 0:
            log.debug("MQLRule for appTemplate '" + self.name + "' of type " + self.shortClass + " was not found.")
        else:
            for mqlRule in modelObjects:       
                taddmMQLRule(mqlRule,self)

    #########################################################################
    def addMQLRule(self,mqlRule):
        self.MQLRules.append(mqlRule)



#######################################################################################################
#######################################################################################################
class taddmMQLRule(taddmObject):

    #########################################################################
    def __init__(self,modelObject,parent):
        self.name = modelObject.getMQLRuleName()
        self.cloneAttributes = ["CDMSource","MQLQuery","adminState","cmdbSource","contextIp","description","extendedAttributes","functionalGroupName","label","locationTag","objectType","sourceToken"]        
        taddmSuper.__init__(self,modelObject,parent)    
        self.parent.addMQLRule(self)


#######################################################################################################
#######################################################################################################
class taddmAdminInfo(taddmObject):

    #########################################################################
    def __init__(self,modelObject,parent):
        self.adminInfo = {}        
        self.name = modelObject.getDisplayName()
        self.cloneAttributes = ["CDMSource","adminContact","adminState","appGroupName","cmdbSource","contextIp","description","escalationContact","extendedAttributes","label","locationTag","note","objGuid","objectType","roles","site","sourceToken","trackingNumber"]
        taddmSuper.__init__(self,modelObject,parent)    
        self.parent.addAdminInfo(self)
        

#######################################################################################################
#######################################################################################################
class taddmUserData(taddmObject):

    #########################################################################
    def __init__(self,modelObject,parent):
        self.userDataInfo = {}        
        self.name = modelObject.getDisplayName()
        self.cloneAttributes = ["CDMSource","adminState","category","cmdbSource","contextIp","description","extendedAttributes","label","locationTag","metaRef","objGuid","objectType","roles","sourceToken"]
        i = 1
        while i <= 100:        
            self.cloneAttributes.append("userAttr" + str(i))
            i = i + 1       
        taddmSuper.__init__(self,modelObject,parent)    
        self.parent.addUserData(self)
        
#######################################################################################################
#######################################################################################################
class taddmRelationship(taddmObject):

    #########################################################################
    def __init__(self,modelObject,parent):
        self.name = modelObject.getDisplayName()
        self.cloneAttributes = ["CDMSource","adminState","cmdbSource","derived","description","extendedAttributes","generated","locationTag","objectType","source","sourceToken","source","sourceType","target","targetType","type"]
        taddmSuper.__init__(self,modelObject,parent)    
        self.parent.addRelationship(self)
        
    
#######################################################################################################
#######################################################################################################
class Usage(Exception):
    def __init__(self, msg):
        
        self.msg = msg


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

            
    def leave(self): 
        raise SystemExit()

###########################################################################
###########################################################################
def set_resourceType(groupType):
    
    if string.lower(groupType) == "service":
        resourceType = "BusinessSystem"
    elif string.lower(groupType) == "businesssystem":
        resourceType = "BusinessSystem"
    elif string.lower(groupType) == "accesscollection":
        resourceType = "AccessCollection"
    elif string.lower(groupType) == "collection":
        resourceType = "Collection"
    elif string.lower(groupType) == "application":
        resourceType = "Application"
    
    return resourceType

###########################################################################
###########################################################################
def show_help():
    
    pref = "\t\t"
    delim = "\t\t"
    print ""
    print "\tUsage: " + prog + "  OPTIONS -a ACTION ACTION-OPTIONS ACTION-PARAMETERS REPORT-OPTIONS"
    print ""
    print pref + "OPTIONS:"
    print pref + "    Mandatory:"
    print pref + "\t-u, --user <user to perform the action as>"
    print pref + "\t-p, --password <password that authenticates this user>"
    print pref + "    Optional:"
    print pref + "\t-H, --host <host the TADDM server is installed on, defaults to localhost>"
    print pref + "\t-P, --port <port the TADDM server public service registry is listening on, defaults to 9433>"
    #print pref + "\t-h, --help <This help>"
    print ""
    print pref + "ACTION:"
    print pref + "\tlistall: List all resources of specific type.(default)"
    print pref + "\tlist:\t List details for a specific resource identified by type and name."
    print pref + "\tdelete:\t Delete a specific resource identified by type and name."
    print pref + "\tclone:\t Make a new named copy of a specific resource identified by type and name."
    print pref + "\thelp:\t This help."
    print ""
    print pref + "ACTION-OPTIONS:"
    print pref + "\tlistall -t|--type [AccessCollection|BusinessSystem|Collection|Application|Service]"
    print ""
    print pref + "\tlist\t-t|--type [AccessCollection|BusinessSystem|Collection|Application|Service]"    
    print pref + "\t\t-g|--groupName <name>"
    print pref + "REPORT-OPTIONS"
    print ""
    print pref + "\tdelete\t-t|--type [AccessCollection|BusinessSystem|Collection|Application|Service]"    
    print pref + "\t\t-g|--groupName <name>"
    print ""
    print pref + "\tclone\t-t|--type [AccessCollection|BusinessSystem|Collection|Application|Service]"    
    print pref + "\t\t-g|--groupName <name>"
    print pref + "\t\t-n|--newName <name>"
    print pref + "<ACTION-PARAMETERS>"
    print pref + "<REPORT-OPTIONS>"
    print ""
    print pref + "ACTION-PARAMETERS:"
    print pref + "\tGeneral:"
    print pref + "\t\t-e|--exclude"+delim + "Suppresses cloning of specific report types. Valid types are:"
    print pref + "\t\t\t\t\t\tA: adminInfo"
    print pref + "\t\t\t\t\t\tR: relationships"
    print pref + "\t\t\t\t\t\tU: user data"
    print pref + "\t\t-m|--modifyRules"+delim + "Instructs "+prog+" to replace the group name in MQLRules."
    print pref + "\t\t-o|--overwriteGroupName"+delim + "Instructs "+prog+" to replace the group name in extended attributes."
    print pref + "\t\t-f|--force"+delim + "Forces the deletion of existing resources without user confirmation."
    print pref + "\t\t-h|--help"+delim + "Shows this help."
    print pref + "\t\t-r|--rebuildTopology"+"\t" + "Rebuilds the TADDM topology after the creation of new groups."
    print pref + "\t\t-q|--quiet"+delim + "Supresses output to the console."
    print pref + "\t\t-T|--trace"+delim + "Enables log messages to the displayed in the console."
    print pref + "\t\t-D|--debug"+delim + "Sets the log level to DEBUG, so debugging messages are displayed in the console if -T is also specified."
    print pref + ""
    print pref + "REPORT-OPTIONS: [-c|--compact] [-e|--exclude<type>]* [-s|summary] [-q|--quiet]"
    print pref + "\t\t-c|--compact"+delim + "Shows only resource attributes that has a value."
    print pref + "\t\t-e|--exclude"+delim + "Suppresses display of specific report types. Valid types are:"
    print pref + "\t\t\t\t\t\tA: adminInfo"
    print pref + "\t\t\t\t\t\tR: relationships"
    print pref + "\t\t\t\t\t\tU: user data"
    print pref + "\t\t-s|--summary"+delim + "Shows only the high-level objects related to a group."
    ##print pref + "\t\t-x|--includeExtendedAttributes"+delim + "includes extAttr in the cloning process."
    print ""
    print "\tLog messages can be found in " + coll_home + "/log/" + prog + ".log."
    print ""
    print "\tEXAMPLES:"
    print ""
    print pref+"List all groups:"
    print pref+"\t"+prog+" -u administrator -p collation -a listall"
    print ""
    print pref+"List the summary for the application named Trade:"
    print pref+"\t"+prog+" -u administrator -p collation -a list -t Application -g Trade -s\n"
    print pref+"List the application named Trade, show only attributes that have a value, and suppress relationship and userData information:"
    print pref+"\t"+prog+" -u administrator -p collation -a list -t Application -g Trade -c -eA -eU\n"
    print ""
    print pref+"Delete the collection named MyColl without user confirmation:"
    print pref+"\t"+prog+" -u administrator -p collation -a delete -t Collection -g MyColl -f"
    print ""
    print pref+"Clone the MyService business service to a new service named NewService including only AdminInfo and UserData information. Do not replace the group name in any related objects."
    print pref+"\t"+prog+" -u administrator -p collation -a clone -t Service -g MyService -n NewService -eR"
    print pref+"Clone the MyColl collection to a new collection named NewColl, and replace all instances of the original collation name with the new collation name in all userData objects:"
    print pref+"\t"+prog+" -u administrator -p collation -a clone -t Collection -g MyColl -n NewColl -o"
    print pref+"Clone the Trade application to a new application named NewApp including adminInfo, UserData, and Relationships, and replace all instances of the original application name with the new application name in all MQLRule, and userData objects:"
    print pref+"\t"+prog+" -u administrator -p collation -a clone -t Collection -g MyColl -n NewApp -o -m"
    print pref+"Clone the Trade application to a new application named NewApp, include all related objects except relationships, and replace all instances of the original application name with the new application name:"
    print pref+"\t"+prog+" -u administrator -p collation -a clone -t Collection -g MyColl -n NewApp -eR -o -m"
    

    raise SystemExit()


#################################
#################################
def cloneAttribute (obj,attribute):
    
    methodName = string.upper(attribute[0]) + attribute[1:]
    value = obj.attributes[attribute][0]
    dataType = obj.attributes[attribute][1]
    shortDataTypes = re.split(r'\.',dataType)
    shortDataType = shortDataTypes[len(shortDataTypes)-1]

    
    if value != '' and value != None:
    
        ## replace instances of the old group name with the new group name
        if (obj.shortClass != "MQLRule" and overwriteGroupName == True) or (obj.shortClass == "MQLRule" and modifyRules == True):
            if string.lower(shortDataType) in ["string"]:
                old = oldGroupName
                new = newGroupName
                if (obj.shortClass == "MQLRule" and modifyRules == True):
                    old = "'"+oldGroupName+"'"
                    new = "'"+newGroupName+"'"
                    log.debug("\t\t\tReplacing '" + old + "' with '" + new + "' in attribute: " + attribute + " in " + obj.shortClass)
                    value = re.sub(old,new,value)

                    old = "\""+oldGroupName+"\""
                    new = "\""+newGroupName+"\""
                    log.debug("\t\t\tReplacing '" + old + "' with '" + new + "' in attribute: " + attribute + " in " + obj.shortClass)
                    value = re.sub(old,new,value)
                else:
                    log.debug("\t\t\tReplacing '" + old + "' with '" + new + "' in attribute: " + attribute + " in " + obj.shortClass)
                    value = re.sub(old,new,value)

            
            
        setMethodName = "set" + methodName        
        setMethod = getattr(obj.newObject,setMethodName)
        log.debug("\t\t\tCloning attribute: '" + attribute + "':\t'" + str(value) + "' (" + dataType + ")")
        setMethod(value)


#################################
#################################
def logit (message):  
    
    #print "'"+message[0:4]+"'"
    if quiet == False:
        if message[0:4] == "++++":            
            log.error(message)
        elif message[0:4] == "----":
            log.info(message)
        else:
            #log.info(message) 
            print(message)
            #log.info(message)
            #print >> logFileHandle, message
        #log.debug(message[6:])
    
    return


#################################
#################################
def exportDefs(groupObject,appDir):

    modelObject = groupObject.modelObject
    indent = 4
    
    className = groupObject.shortClass
        
    log.info("Exporting " + className + " " + groupObject.modelObject.getName() + " to " + appDir)
    

    queryDepth = 2    
            
                    
    serviceAttributes = ["CDMSource","CICategory","CIRole","URL","adminState","assetID","assetTag","businessImpact","businessPriority","businessRole","cmdbSource","components","contact","containingSystem","contextIp","description","extendedAttributes","generalCIRole","isPlaceholder","lifecycleState","locationTag","managedSystemName","name","objectType","primaryOwner","roles","sourceToken"] 
    collectionAttributes = ["CDMSource","active","adminState","cmdbSource","contextIp","description","extendedAttributes","locationTag","managedSystemName","members","name","objectType","roles","sourceToken"]    
    applicationAttributes = ["CDMSource","CICategory","CIRole","URL","adminState","appDescriptors","appVersion","assetID","assetTag","cmdbSource","components","contact","containingSystem","contextIp","description","extendedAttributes","generalCIRole","installationNumber","isPlaceholder","licenseExpiryDate","lifecycleState","locationTag","managedSystemName","name","objectType","primaryOwner","roles","sourceToken","vendor"]
    appTemplateAttributes = ["CDMSource","MQLRules","adminState","appTemplateName","appTemplateType","cmdbSource","contextIp","description","extendedAttributes","isPlaceholder","locationTag","managedSystemName","objectType","removeNonMembers","roles","sourceToken"]
    applicationDefAttributes = ["CDMSource","adminState","cmdbSource","contextIp","description","displayName","extendedAttributes","isPlaceholder","label","locationTag","managedSystemName","name","objectType","roles","sourceToken"]
    mqlRuleAttributes = ["CDMSource","MQLQuery","MQLRuleName","adminState","cmdbSource","contextIp","description","extendedAttributes","functionalGroupName","locationTag","objectType","sourceToken"]
    functionalGroupAttributes = ["active","adminState","CDMSource","contextIp","description","groupName","managedSystemName","memberType","members","modelObjects","objectType","operationalStatus","orgEntity","roles","serviceInstances","sourceToken"]
    
    
    columns = []
    if className == "BusinessSystem":
        columns = serviceAttributes
    elif className == "AcceessCollection":
        columns = collectionAttributes
    elif className == "Collection":
        columns = collectionAttributes
    elif className == "Application":
        columns = applicationAttributes
            
    cols = columns[0]
    for col in columns[1:]:
        cols = cols + "," + col  

    where = ""
    # Get the group
    if not (oldGroupName == "" or oldGroupName is None):
        where = "displayName equals '" + oldGroupName + "'"
        query = "select " + cols + " from " + className + " where " + where
        # get the object as xml
        xmlString = api.findXML(query,queryDepth,indent,None,None)

        appFile = appDir + "/" + prog + "_" + resourceType
        if oldGroupName != None:
            appFile = appFile + "_" + oldGroupName 
        else:
            appFile = appFile + "_ALL"
        appFile = appFile + ".xml"
        
        output=open(appFile,'w')
        print >> output,xmlString
        #        output.write(res)
        output.flush()
        output.close()

        log.info("\texported " + className + "(s) to " + appFile)
        

        ##  get AppTemplates
        if className != "BusinessSystem":

            log.debug("Exporting application templates")
            #queryDepth = 2
            cols = appTemplateAttributes[0]
            for col in appTemplateAttributes[1:]:
                cols = cols + "," + col  
            
            where = "appTemplateType == '0'"    
            if className == "AccessCollection":
                where = "appTemplateType == '1'"            
            if className == "Collection":
                where = "appTemplateType == '1'"            
                
            if not (oldGroupName == "" or oldGroupName is None):
                where = where + " and appTemplateName ends-with \":" + oldGroupName + "\""
                query = " select " + cols + " from AppTemplate where " + where
                    
            xmlString = api.findXML(query,queryDepth,indent,None,None)
            log.debug("Length of xmlString is: " + str(len(xmlString)) )

            



            if xmlString == "<results/>":
                log.debug("No appTemplate is defined for " + className + " " + oldGroupName)
            else:    
                appFile = appDir + "/" + prog + "_" + resourceType

                if oldGroupName != None:
                    appFile = appFile + "_" + oldGroupName 
                else:
                    appFile = appFile + "_ALL" 
                appFile = appFile + "_AppTemplate.xml"

                output=open(appFile,'w')
                print >> output,xmlString
            
                output.flush()
                output.close()
                log.debug("\tExported appTemplate(s) to " + appFile)
            
            ###  get MQLRules
            #
            log.debug("Exporting MQL Rules")
            queryDepth = 1
            cols = mqlRuleAttributes[0]
            for col in mqlRuleAttributes[1:]:
                cols = cols + "," + col  
            
                
            where =  " MQLRuleName starts-with '" + str(modelObject.getGuid()) + "'"
            query = " select " + cols + " from MQLRule where " + where
                    
            xmlString = api.findXML(query,queryDepth,indent,None,None)
            log.debug("Length of xmlString is: " + str(len(xmlString)) )

            if xmlString == "<results/>":
                log.debug("No MQLRules are defined for " + className + " " + oldGroupName)
            else:    
                appFile = appDir + "/" + prog + "_" + resourceType
            
                if oldGroupName != None:
                    appFile = appFile + "_" + oldGroupName 
                else:
                    appFile = appFile + "_ALL" 
                appFile = appFile + "_MQLRules.xml"
            
                output=open(appFile,'w')
                print >> output,xmlString
            
                output.flush()
                output.close()
                log.debug("\tExported MQLRules to " + appFile)

            
            
            
            
            
            ##  get ApplicationDefs
            if className == "Application":

                log.debug("Exporting application definitions")
                queryDepth = 1
                cols = applicationDefAttributes[0]
                for col in applicationDefAttributes[1:]:
                    cols = cols + "," + col  
            
                
                if not (oldGroupName == "" or oldGroupName is None):
                    where = "name equals '" + oldGroupName + "'"
                    query = " select " + cols + " from ApplicationDef where " + where
                    
                xmlString = api.findXML(query,queryDepth,indent,None,None)

                if len(xmlString) < 15:
                    log.debug("No ApplicationDef is defined for " + className + " " + oldGroupName)
                else:    
                    appFile = appDir + "/" + prog + "_" + resourceType

                    if oldGroupName != None:
                        appFile = appFile + "_" + oldGroupName 
                    else:
                        appFile = appFile + "_ALL" 
                    appFile = appFile + "_ApplicationDef.xml"

                    output=open(appFile,'w')
                    print >> output,xmlString
            
                    output.flush()
                    output.close()
                    log.debug("\tExported ApplicationDef to " + appFile)





#################################
#################################
def importDefs(groupType):





    feed = "xml"    
    
    try:
                

        appFile = prog + "_" + resourceType + "." + feed

        print "Importing " + string.lower(groupType) + " from " + appFile 

        
        infile=open(appFile,'r')
        xmlString = input.read()
        infile.close()

        '''    
        serviceAttributes = ["CDMSource","CICategory","CIRole","URL","adminState","assetID","assetTag","businessImpact","businessPriority","businessRole","cmdbSource","components","contact","containingSystem","contextIp","description","extendedAttributes","generalCIRole","isPlaceholder","label","lifecycleState","locationTag","managedSystemName","name","objectType","primaryOwner","roles","sourceToken"] 
        collectionAttributes = ["CDMSource","active","adminState","cmdbSource","contextIp","description","extendedAttributes","label","locationTag","managedSystemName","members","name","objectType","roles","sourceToken"]    
        applicationAttributes = ["CDMSource","CICategory","CIRole","URL","adminState","appDef","appDescriptors","appVersion","assetID","assetTag","cmdbSource","components","contact","containingSystem","contextIp","description","extendedAttributes","generalCIRole","groups","installationNumber","isPlaceholder","label","licenseExpiryDate","lifecycleState","locationTag","managedSystemName","name","objectType","primaryOwner","roles","sourceToken","vendor"]
        appTemplateAttributes = ["CDMSource","MQLRules","adminState","appTemplateName","appTemplateType","cmdbSource","contextIp","description","extendedAttributes","isPlaceholder","label","locationTag","managedSystemName","objectType","removeNonMembers","roles","sourceToken"]
        '''




        dom = parseString(xmlString)
        #retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
        xmlTag = dom.getElementsByTagName('tagName')[0].toxml()
        #strip off the tag (<tag>data</tag>  --->   data):
        xmlData=xmlTag.replace('<tagName>','').replace('</tagName>','')
        #print out the xml tag and data in this format: <tag>data</tag>
        print xmlTag
        #just print the data
        print xmlData






        rc, resourceGuid = resource_create(resourceType, res ,prompt=True)

            
        if string.lower(groupType) == "application":            
            appFile = prog + "_" + resourceType +"_AppTemplate." + feed
            print "Importing " + string.lower(groupType) + " from " + appFile         
            infile=open(appFile,'r')
            res = input.read()
            infile.close()

            ##  replace the GUID in the AppTemplate definition
            

            rc, resourceGuid = resource_create("AppTemplate", res ,prompt=True)
            
            
    except:
        pass        
        
    
    return


    

#########################################################################
#########################################################################
def findModelObjects(query, flatten=True):
    if True == True: #try:
        modelObjects = api.find(query,flatten, None,None)
            
        for modelObject in modelObjects:
            ##MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM            
            log.debug("Fetched")
            log.debug("\tmodelObject:\t\t"+str(modelObject))
            log.debug("\tmodelObject _class:\t"+str(modelObject.getClass()))
            log.debug("\tmodelObject guid :\t"+str(modelObject.getGuid()))
            ##MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
        
                
        return modelObjects


    
        

#############################################################
#############################################################
def deleteModelObjects(deleteObjectList,mss=None):
    
    for o in deleteObjectList:
        log.debug("About to delete : "  + str(o.getDisplayName()) + " " + str(o.__class__))
    
    
    tempObjectList = []
    for tempGroupModelObject in deleteObjectList:
        ##  find the appTemplate if it exists, and delete it
        if tempGroupModelObject.hasName():
            log.debug("Inspecting objectType " + str(tempGroupModelObject.__class__))
            tempAppTemplateName = str(tempGroupModelObject.getGuid())+":"+str(tempGroupModelObject.getName())                        
            resourceFilter = "appTemplateName equals '" + tempAppTemplateName +  "'"
            tempAppTemplateModelObjects,modelObjectExtAttr,adminInfo,adminInfoAttributes,adminInfoExtAttr = getModelObjectsFromQuery("AppTemplate", resourceFilter)
            ## add appTemplates to list of objects to be deleted
            for tempAppTemplateObject in tempAppTemplateModelObjects: 
                log.debug("About to delete : " + tempAppTemplateObject.getDisplayName() + " " + str(tempAppTemplateObject.__class__))
                tempObjectList.append(tempAppTemplateObject)
    
    for o in tempObjectList:
        deleteObjectList.append(o)   
    
    log.debug("Deleting:\t" + str(deleteObjectList))
    num = api.delete(deleteObjectList,None)
    log.debug("Deleted " + str(num) + " objects.")
    
    return


#############################################################
#############################################################
def getModelObjectsFromQuery(resourceType,resourceFilter,flatten=True):
                    
    query = "select * from " + resourceType + " where " + resourceFilter
    log.debug("Query:\t" + str(query))
    modelObjects = []
    modelObjects = findModelObjects(query, flatten)
    log.debug("Results:\t" + str(modelObjects))
    return  modelObjects  

#############################################################
#############################################################
def getModelObjectAttributes(modelObject):
    object = modelObject
    _class = modelObject.__class__
    className = str(_class.__name__)
    classNameShort = className[:len(className)-4]   ##   remove the last four characters 'Impl'

    # get the metadata to be able to list all attributes         
    meta = api.getMetaData(classNameShort,True)
    attributeNames = meta.getObjectAttributes()        

                        
            
    modelObjectAttributes={}        
    #list the atttibutes and get the values 
    numAttr = 0
    numVal = 0
    for attr in attributeNames:
        numAttr = numAttr + 1    
        hasMethodName = "has" + string.upper(attr.name[0]) + attr.name[1:]
        hasMethod = getattr(object,hasMethodName)
        value = ""
        if hasMethod():
            getMethodName = "get" + string.upper(attr.name[0]) + attr.name[1:]        
            getMethod = getattr(object,getMethodName)
            value = getMethod()
            numVal = numVal + 1    
        #log.debug("" + str(attr.name) + ":\t'" + str(value) + "'\t(" + attr.type + ")")
        modelObjectAttributes[attr.name] = [value, attr.type, attr.arrayType,attr.timestampType,attr.length,attr.displayString]    
    
    #log.debug("modelObjectAttributes:\t" + str(modelObjectAttributes))
    return modelObjectAttributes            

#############################                    
#############################
#def show_details(modelObject,attrs,extAttr,adminInfo,adminInfoAttr,userData,indent=0):
#    show_details(self.modelObject,self.attributes,self.extendedAttributes, self.adminInfo, None, self.userData,None)
def show_details(obj,indent=0):

    modelObject = obj.modelObject
    attrs = obj.attributes
    extAttr = obj.extendedAttributes
    adminInfo = obj.adminInfo
    adminInfoAttr = None
    userDataInfo = obj.userDataInfo
    relationships = obj.relationships




    ##   layout of the incoming structure
    ##    attrs["attr.name"] = [value, type, arrayType,timestampType,length,displayString]

    ## find attributes with values
    numVals = 0    
    for a in attrs.keys():        
        if attrs[a][0] != "":
            numVals = numVals + 1
    
    className = modelObject.__class__.__name__
    className = className[:len(className)-4]
    if string.find(className,".") > -1:
        className = re.split(r'\.',className)
        className = string.upper(className[len(className)-1])
        
    ind = ""
    if indent == 1:
        ind = "\t"
    elif indent == 2:
        ind = "\t\t"
    elif indent == 3:
        ind = "\t\t\t"
    elif indent == 4:
        ind = "\t\t\t\t"
    elif indent == 5:
        ind = "\t\t\t\t\t"
                        
    print("\n" + ind + className + ":\t" + modelObject.getDisplayName() + "(" + str(modelObject.getGuid()) + ") has " + str(len(obj.attributeNames)) + " attributes and " + str(numVals) + " values.")
    if summary == True:           
        print(ind + "\t\tExtendedAttributes:\t\t" + str(extAttr))
        print(ind + "\t\tAdminInfo:\t\t\t" + str(adminInfo))        
        print(ind + "\t\tUserData:\t\t\t" + str(userDataInfo))
        print(ind + "\t\tRelationships:\t\t\t" + str(relationships))
        print("")

    keyNames = attrs.keys()
    keyNames.sort()
    
    if summary != True:
        print(ind + "\t      Attributes:")
        for attr in keyNames:            
            log.debug("\t" + attr + ":\t'" + str(attrs[attr][0]) + "'")
            val = attrs[attr][0]
        
            if val == '' and compact == True:
                continue
                
            # find type
            objType = attrs[attr][1]
            ##objType = className
            if string.find(objType,".") > -1:
                objType = re.split(r'\.',objType)
                objType = objType[len(objType)-1]                
            pref = ""    
            if len(attr) > 23:
                pref = "\t"
            elif len(attr) > 15:
                pref = "\t\t"
            elif len(attr) > 7:
                pref = "\t\t\t"
            else:
                pref = "\t\t\t\t"

            if len(objType) > 23:
                space = "\t"
            elif len(objType) > 15:
                space = "\t\t"
            elif len(objType) > 7:
                space = "\t\t\t"
            else:
                space = "\t\t\t\t"
        
            print(ind + "\t\t" + attr + pref + objType + space + str(val))
            
        # ExtendedAttributes
        print(ind + "\t      ExtendedAttributes:\t\t" + str(extAttr))
        
        # AdminInfo
        if adminInfo == None:
            print(ind + "\t      AdminInfo:\t\t\t" + str(adminInfo))
        else:
            print(ind + "\t      AdminInfo:")        
            for adm in adminInfo:
                for attr in adm.attributes.keys():
                    name = attr
                    value = adm.attributes[attr][0]
                    typeList = re.split(r'\.',adm.attributes[attr][1])
                    type = typeList[len(typeList)-1]
                    isArray = adm.attributes[attr][2]
                    isBoolean = adm.attributes[attr][2]
                    length = adm.attributes[attr][4]

                    if value == '' and compact == True:
                        continue
                    
                    sep = "\t"
                    if len(name) >= 16:
                        sep = "\t\t"
                    elif len(name) >= 8:
                        sep = "\t\t\t"
                    elif len(name) >= 4:
                        sep = "\t\t\t\t"
                    
                    print ind + "\t\t" + name + sep + type + "\t\t\t\t" + str(value)
        
        ##for
        
        # UserData

        if userDataInfo == None:
            print(ind + "\t      UserData:\t\t\t\t" + "None")
        elif len(userDataInfo.keys()) == 0:
            print(ind + "\t      UserData:\t\t\t\t" + "None")
        else:
            print(ind + "\t      UserData:")
            for u in userDataInfo.keys():        
                category = userDataInfo[u][0]
                attrName = userDataInfo[u][1]
                attrType = userDataInfo[u][2]
                value = userDataInfo[u][3]    
                print(ind + "\t\t" + category+":"+attrName + "\t\t" + attrType + "\t\t\t\t'" + value+"'")           
        
        # Relationships        
        if relationships == None:
            print(ind + "\t      Relationships:\t\t\t" + "None")
        elif len(relationships) == 0:
            print(ind + "\t      Relationships:\t\t\t" + "None")
        else:
            print(ind + "\t      Relationships:")
            for rel in relationships:
                r = rel.modelObject            
                source = r.getSource()
                target = r.getTarget()
                type = r.getType()
                
                relTypeParts =  re.split("\.",type)
                relType = relTypeParts[len(relTypeParts) -1]   
                src = api.find(source.getGuid(),1,None,None)
                srcName = src.getDisplayName()
                srcType = str(source.getClass().getSimpleName())
                srcType = srcType[:len(srcType)-4]
                tgt = api.find(target.getGuid(),1,None,None)
                tgtType = str(target.getClass().getSimpleName())                
                tgtType = tgtType[:len(tgtType)-4]
                tgtName = tgt.getDisplayName()
                
                details = ind + "\t\t" + srcName + " (" + srcType + ")\t\t" + relType + "\t\t\t" + tgtName + " (" + tgtType + ")"
                
                print(details)           
        print("")
        
        
        
    return



        
###############################################################################        
###############################################################################
###############################################################################

def main(argv=None):
    
    
    global log,coll_home
    global prog
    
    log,prog = taddmJythonApiHelper.init()    
    coll_home = getCollHome()
    
    if argv is None:
        argv = sys.argv


    global compact
    global optMsg    
    global api,conn,sess
    global attributes, resources,cdmclasses
    global resourceType
    global action
    global fetchSize,queryDepth,oldGroupName,newGroupName    
    global appFile, logFile, errFile, pidFile 
    global logFileHandle, errFileHandle,pidFileHandle
    global taddmServerHost, taddmServerPort, taddmServerUser, taddmServerPassword
    global trace, force, debug, quiet, rebuildTopology, modifyRules,includeExtendedAttributes, includeUserData,includeAdminInfo,includeRelationships, overwriteGroupName,summary
    optMsg = None
    
    
    rebuildTopology = False
    appFile = None
    taddmServerPort = -1
    taddmServerHost = "localhost"
    taddmServerUser = "administrator"
    taddmServerPassword = None
    groupName = None
    groupType = None
    resourceType = None
    includeUserData = True
    includeRelationships = True
    includeAdminInfo = True
    includeExtendedAttributes = False
    overwriteGroupName = False
    modifyRules = False
    appDir = "./"
    action = "list"
    
        
    trace = False
    debug = False
    force = False
    quiet = False
    replace = False
    compact = False
    summary = False
         


    ## Default values to control queries
    queryDepth=1
    fetchSize=100
    resourceType = None
    resourceFilter = None
    oldGroupName = None


    
    


    
    ####################################################################
    #    get arguments
    ####################################################################
    try:

        
               
        shortOpts = "a:cdDe:fhH:g:mn:op:P:qrst:Tu:"
        longOpts = ["action=","compact","directory","debug","exclude=","force","help","host=","group=","modifyRules","newGroup=","overwriteGroupName","quiet","password=","port=","rebuildTopology","summary","type","Trace=","user="]
                
        opts = {}
        args = {}
        
        try:        
            opts, args = getopt.getopt(argv[1:], shortOpts, longOpts)
        except GetoptError, opt_ex:
            raise Usage(opt_ex.msg)    

        
        for o, a in opts:
            o = string.strip(o)

            if o in ("-a", "--action"):
                action = string.strip(a)
                action = string.lower(action)                
                if not action in ["help","clone", "export","list", "listall","delete"]:
                    raise Usage("Illegal action '" + string.strip(a) + "' specified.")

            elif o in ("-c", "--compact"):
                compact = True
                
            elif o in ("-e", "--exclude"):
                argument = string.strip(a)
                argument = string.upper(argument)
                if argument in ["A","ADMININFO"]:
                    includeAdminInfo = False 
                elif argument in ["R","RELATIONSHIPS"]:
                    includeRelationships = False 
                elif argument in ["U","USERDATA"]:
                    includeUserData = False 
                elif argument in ["X","EXTATTR","EXTENDEDATTRIBUTES"]:
                    includeExtendedAttributes = False 
                else:
                    raise Usage("Illegal argument '" + string.strip(a) + "' specified.")

            elif o in ("-d", "--directory"):
                appDir = string.strip(a)

            elif o in ("-D", "--debug"):
                debug = True


            elif o in ("-f", "--force"):
                force = True

            elif o in ("-h", "--help"):
                raise Usage("help")

            elif o in ("-H", "--host"):
                taddmServerHost = string.strip(a)
                #taddmServerIp = socket.gethostbyname(taddmServerHost)
                #taddmServerHost, a, dummy = socket.gethostbyaddr(taddmServerIp)

            elif o in ("-g", "--group"):
                oldGroupName = string.strip(a)

            elif o in ("-m", "--modifyRules"):
                modifyRules = True

            elif o in ("-n", "--newGroup"):
                newGroupName = string.strip(a)
                
            elif o in ("-o", "--overwriteGroupName"):
                overwriteGroupName = True
                
            elif o in ("-p", "--password"):
                taddmServerPassword = string.strip(a)

            elif o in ("-P", "--port"):
                taddmServerPort = int(a)

            elif o in ("-q", "--quiet"):
                quiet = True
                force = True

            elif o in ("-r", "--rebuildTopology"):
                rebuildTopology = True

            elif o in ("-s", "--summary"):
                summary = True

            elif o in ("-T", "--trace"):
                trace = True
                quiet = False
                
            elif o in ("-t", "--type"):
                groupType = string.strip(a)
                if not string.lower(groupType) in ["application","accesscollection","collection","businesssystem","service"]:
                    raise Usage("Invalid type : '" + groupType + "' specified.")                

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
             
            if action == "help":
                show_help()
                
            if action == None:
                msg = "You MUST provide a valid action using the -a or --action arguments"
        
            elif taddmServerHost == None:
                msg = "You MUST provide a host name of ip address of the TADDM storage server using the '-H' or '--host' argument."

            elif taddmServerUser == None:
                msg = "You MUST provide a user name using the '-u' or '--user' arguments."

            elif taddmServerPassword == None:
                msg = "You MUST provide password using the '-p' or '--password' arguments."

            elif groupType == None:
                msg = "To use the '" + action + "' function, you MUST provide a group type using the '-t' or '--type' argument."

            elif action != "listall" and oldGroupName == None:
                msg = "To use the '" + action + "' function, you MUST provide a valid group name (name of Service, Application or Collection) using the -g or --group argument."

            elif action == "clone" and newGroupName == None:
                msg = "To use the '" + action + "' function, you MUST provide a name for the resource to be created using the -n or --newGroup argument."

        if msg != None:
            raise Usage(msg)
        

        
    except Usage, usage_ex:                
        if not usage_ex.msg == "help":
            msg = "\nINVOCATION ERROR:\t" + usage_ex.msg
            print msg
            
            
        show_help()            
        raise SystemExit(0)
    

    except Exit, exit_ex:
        msg = "("+str(exit_ex.rc)+") " + exit_ex.msg
        print msg
               
        ##exit_ex.leave()
        raise SystemExit(exit_ex.rc)    


                
    # Setup logging                
    log = taddmJythonApiHelper.setupLog4jLogging(trace,debug)


    #############################
    #  connect to TADDM
    #############################    
    api = connectToTaddm(taddmServerHost,taddmServerPort,taddmServerUser,taddmServerPassword)

        
    #####################################
    #  find the action
    #####################################
    try:        
        if string.lower(action) == "clone":
            msg = "Cloning " + groupType + " " + oldGroupName + " to " + newGroupName
        elif string.lower(action) == "list":
            msg = "Listing " + groupType + " " + oldGroupName
        elif string.lower(action) == "listall":
            msg = "Listing all " + groupType + "s "
        elif string.lower(action) == "delete":
            msg = "Deleting " + groupType + " " + oldGroupName
        elif string.lower(action) == "export":
            if oldGroupName == None:
                msg = "Exporting all " + groupType + "s " 
            else:
                msg = "Exporting " + groupType + " " + oldGroupName

        print(msg)



        ###########################################################
        #  list all of a single type
        ###########################################################
        resourceType = set_resourceType(groupType)
        
        if string.lower(action) == "listall":
        
            print("\n\t================================================================================")
            print("\t\t" + resourceType + "(s)")
            print("\t================================================================================")

            log.debug("DEBUG")
                
            query = "select displayName, label from " + resourceType + " order by displayName"
            results = api.find(query,1,None,None)
            for r in results:
                className = r.__class__.__name__
                className = className[:len(className)-4]
                shortClassName = re.split('\.',className)
                shortClassName = shortClassName[len(shortClassName)-1]
                if shortClassName == resourceType:
                    ##print("\t\t"  + str(shortClassName)+ "\t" + str(r.getDisplayName()) )
                    print("\t\t"  + str(r.getDisplayName()) )
        
            raise Quit()


                        

        ##########################
        #  get the data
        ##########################

        resourceType = set_resourceType(groupType)
            
        if not action == ["import"]:
            
            ################################################################                
            ## Get the group
            oldGroupObject = taddmGroup().populate(resourceType,oldGroupName)
        
        
        ############################################################
        ##
        ##              LIST
        ##
        ############################################################
        if action in ["list"]:
            oldGroupObject.listResults()
            raise Quit
                
        ############################################################
        ##
        ##              Clone
        ##
        ############################################################
        elif action in ["clone"]:
            oldGroupObject.clone(newGroupName)                    
            raise Quit

        ############################################################
        ##
        ##              Delete
        ##
        ############################################################

        elif string.lower(action) == "delete":
            
                
            oldGroupObject.delete(force)
        
            raise Quit(0)    


        ############################################################
        ##
        ##            Clone
        ##
        ############################################################
        
        elif string.lower(action) == "clone":

                
            oldGroupObject.clone()
                
            # rebuild the topology to populate the Functional Groups from the appTemplate
            #if self.rebuildTopology == True:
            log.debug("Rebuilding topology")
            api.rebuildTopology()


            raise Quit(0)    

            
        
        ############################################################
        ##
        ##              Export
        ##
        ############################################################
        
        elif string.lower(action) == "export":
            log.info("exporting " + string.lower(groupType) + " to " + appDir)            
            exportDefs(oldGroupObject ,appDir)
            log.info("exported " + string.lower(groupType))

        ############################################################
        ##
        ##              Import
        ##
        ############################################################
        
        elif string.lower(action) == "import":
    
    
            
            importDefs(string.lower(groupType))
    
    
    
        
            '''
            print "Exporting " + string.lower(groupType) 
    
            serviceAttributes = ["CDMSource","CICategory","CIRole","URL","adminState","assetID","assetTag","businessImpact","businessPriority","businessRole","cmdbSource","components","contact","containingSystem","contextIp","description","extendedAttributes","generalCIRole","isPlaceholder","label","lifecycleState","locationTag","managedSystemName","name","objectType","primaryOwner","roles","sourceToken"] 
            collectionAttributes = ["CDMSource","active","adminState","cmdbSource","contextIp","description","extendedAttributes","label","locationTag","managedSystemName","members","name","objectType","roles","sourceToken"]    
            applicationAttributes = ["CDMSource","CICategory","CIRole","URL","adminState","appDef","appDescriptors","appVersion","assetID","assetTag","cmdbSource","components","contact","containingSystem","contextIp","description","extendedAttributes","generalCIRole","groups","installationNumber","isPlaceholder","label","licenseExpiryDate","lifecycleState","locationTag","managedSystemName","objectType","primaryOwner","roles","sourceToken","vendor"]
            appTemplateAttributes = ["CDMSource","MQLRules","adminState","appTemplateName","appTemplateType","cmdbSource","contextIp","description","extendedAttributes","isPlaceholder","label","locationTag","managedSystemName","objectType","removeNonMembers","roles","sourceToken"]
            
            
            if string.lower(groupType) == "collection":
                queryDepth = 1
            elif string.lower(groupType) == "application":
                queryDepth = 2
            elif string.lower(groupType) == "service":
                queryDepth = 1
            
            
            fetchSize= 1000000
            feed = "xml"
            
            columns = []
            if string.lower(groupType) == "service":
                columns = serviceAttributes
            elif string.lower(groupType) == "collection":
                columns = collectionAttributes
            elif string.lower(groupType) == "application":
                columns = applicationAttributes
            
            cols = columns[0]
            for col in columns[1:]:
                cols = cols + "," + col  

            where = ""
            if not (oldGroupName == "" or oldGroupName is None):
                where = "displayName equals '" + oldGroupName + "'"

            url, query = build_query_url(cols, None, resourceType, where, "query",None,None,feed,queryDepth)
            rc, res = http_process(url,None, query, "GET")

            appFile = prog + "_" + resourceType +"." + feed
            output=open(appFile,'w')
            output.write(res)
            output.close()
        

            ##  get App templates
            if string.lower(groupType) != "service":

                print "\tExporting application templates"
                queryDepth = 3
                cols = appTemplateAttributes[0]
                for col in appTemplateAttributes[1:]:
                    cols = cols + "," + col  
                
                if string.lower(groupType) != "collection":
                    where = "appTemplateType == '0'"
                else:
                    where = "appTemplateType == '1'"
                if not (oldGroupName == "" or oldGroupName is None):
                    where = "and appTemplateName ends-with ':" + oldGroupName + "'"
                    
                url, query = build_query_url(cols, None, "AppTemplate", where, "query",None,None,feed,queryDepth)
                rc, res = http_process(url,None, query, "GET")

 
                appFile = prog + "_" + resourceType +"_AppTemplate." + feed
                output=open(appFile,'w')
                output.write(res)
                output.close()
        '''
        
        
        
        
        
        
        
        ###############################################
        #  cleanup and close files
        ###############################################
        raise Quit(0)

    
    
    except Usage, usage_ex:                
        if not usage_ex.msg == "help":
            msg = "\nINVOCATION ERROR:\t" + usage_ex.msg
            print msg
            
        show_help()            
        raise SystemExit(0)
    
    except Quit, quit_ex:
        if quit_ex.rc == 0:
            msg = "\n" + prog + " ended  successfully"
            #log.error(msg) 
        SystemExit()

    except Exit, exit_ex:
        msg = str(exit_ex.rc)+") " + exit_ex.msg        
        print msg
        
        ##exit_ex.leave()
        raise SystemExit(exit_ex.rc)    
    
    except SystemExit,sys_ex:
        #print "---- " + str(sys_ex)
        sys.exit(sys_ex)

    except:
        
        traceB=traceback.format_exc()
        
        log.error("Fatal error: "+ str(sys.exc_info()[0])+ str(sys.exc_info()[1]))
        log.error(traceB)
        
        print "Fatal Error: " + str(sys.exc_info())
        print traceB
        
        if not string.find(str(sys.exc_info()[0]), "Exit"):
            print >> sys.stderr, "Unexpected error: ", sys.exc_info()[0], sys.exc_info()[1]
        
        sys.exit()
        




tracer = None
# tracer = trace.trace(ignoredirs=[sys.prefix, sys.exec_prefix], trace=1, count=2)


if __name__ == "__main__":
    if not tracer == None:
        sys.exit(tracer.run('main()'))
    else:    
        sys.exit(main())
