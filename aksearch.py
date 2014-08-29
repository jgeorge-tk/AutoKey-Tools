#####################################################################
###################### AK Tools - Search Tool #######################
######################## Author: JGeorge-tk #########################
##################### Copyright 2013 jgeorge.tk #####################
######################## License: GNU GPL v3 ########################
########## License URI: http://www.gnu.org/licenses/gpl.txt #########
#####################################################################
# Imports OS for file manipulation and fnmatch for file name matches#
#####################################################################
import os
import fnmatch
from os.path import expanduser
home = expanduser("~")
#####################################################################
#########################Start Configuration#########################
#####################################################################
# Enter the path to your autokey folder you want to index between   #
# the '' MUST start with /, home is assumed                         #
#####################################################################
pathToAutoKeys = home + '/.config/autokey/data/'
#####################################################################
# Toggle searching by file name, file contents or both '1' for on   #
# anything else for off, default is both                            #
#####################################################################
searchFilePath = 1
searchContents = 1
#####################################################################
# List folders you would like excluded from indexing in this format #
# (this assumes the pathToAutoKeys variable):                       #
# ['doesntExist1','doesntExist2/doesntExist3'] < this example blocks#
# folders doesntExist1 and doesntExist3 but not doesntExist2        #
#####################################################################
excludeFolders = []
#####################################################################
# Sets file type to search for between the '' example 'txt', should #
# not be changed unless you know what you are doing as 'py' is      #
# expirimental only                                                 #
#####################################################################
fileType = 'txt'
#####################################################################
##########################End Configuration##########################
#####################################################################
# Due to Autokey's xselection function causing AK to fail if no     #
# selection is found, this is a hack using bash to check and see if #
# there is any xselection, and if found then execute AK API call to #
# pull it, if not set the value to ""                               #
#####################################################################
xclip = "xclip -o -selection"
process = subprocess.Popen(xclip.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]
if output != "":
    xclip = clipboard.get_selection().lstrip().rstrip()
else:
    xclip = ""
#########################################
# Prompts for search terms using AK API #
#########################################
retCode, searchTerm = dialog.input_dialog("Autokey Search Tool", "Enter a search term.", xclip)
if retCode == 0:
    ###########################################
    # Sets empty arrays to be populated later #
    ###########################################
        totalFiles=[]
        nameMatches=[]
        contentMatches = []
        condensedMatches = []
        sortedMatches = []
        ##########################################################
        # Counts the number of search terms for comparison later #
        ##########################################################
        count=0
        for term in searchTerm.split():
                count+=1
    #####################################################################
    # Finds all the files in the pathToAutoKeys folder which are not in #
    # any excludedFolders as defined in the configuration section       #
    #####################################################################
        for dirpath,_,filenames in os.walk(pathToAutoKeys):
                for file in filenames:
                        if fnmatch.fnmatch(file, '*' + fileType):
                                filteredFile = "False"
                                for eachFolder in excludeFolders:
                                        if fnmatch.fnmatch(dirpath, "*" + eachFolder + "*"):
                                                filteredFile = "True"
                                                break
                                if filteredFile == "False":
                                        totalFiles.append(os.path.abspath(os.path.join(dirpath, file)))
        ###################################################################
        # If searchFilePath is enabled in the configuration settings then #
        # it will exclude any non matching files and populate nameMatches #
        # array                                                           #
        ###################################################################
        if searchFilePath == 1:
                for eachFile in totalFiles:
                        c = 0
                        for term in searchTerm.split():
                                if fnmatch.fnmatch(eachFile.lower(), "*" + term.lower() + "*" + fileType):
                                        c += 1
                                if c >= count:
                                        nameMatches.append(eachFile)
        #####################################################################
        # If searchContents is enabled in the configuration settings then   #
        # it will exclude any non matching files and populate contentMatches#
        # array                                                             #
        #####################################################################
        if searchContents == 1:
                for eachFile in totalFiles:
                        openFile = open(eachFile)
                        readFile = openFile.read()
                        c = 0
                        for term in searchTerm.split():
                                if term.lower() in readFile.lower():
                                        c += 1
                        if c >= count:
                                    contentMatches.append(eachFile)
                        openFile.close()
        #################################################################
        # Adds contents of contentMatches and nameMatches arrays into a #
        # single array totalMatches                                     #
        #################################################################
        totalMatches = contentMatches + nameMatches
        #####################################################################
        # Prioritizes search results that the searchTerms are found in both #
        # contentMatches and nameMatches arrays and stores them into sorted #
        # matches                                                           #
        #####################################################################
        if searchFilePath == 1 and searchContents == 1:
                for entry in set(sorted(totalMatches)):
                        condensedMatches.append((entry, totalMatches.count(entry)))
                condensedMatches.sort(key = lambda x: -x[1])
                for entry in condensedMatches:
                        ############################################################
                        # replace(".tx", "." + fileType) is being used as a hack   #
                        # because for some reason the last letter of the file name #
                        # was getting truncated if you update the file type in the #
                        # configuration, you will also need to update it here...   #
                        # at least for now                                         #
                        ############################################################
                        sortedMatches.append(entry[0].strip(pathToAutoKeys).replace(".tx", "." + fileType))
        else:
                sortedMatches = totalMatches
        ###############################################################
        # If no results are found after filtering, error message will #
        # display informing no matches found                          #
        ###############################################################
        if sortedMatches == []:
                dialog.info_dialog("Autokey Search Tool", "<span font='16' color='red'>No Matches Found!?!</span>")
        ###############################################################
        # If results are found, they are sent to the AK API where the #
        # results can be be displayed and a selection made            #
        ###############################################################
        else:
                retCode, choice = dialog.list_menu(sortedMatches, title="Autokey Search Tool", message="Choose a Phrase to send to your Keyboard", default=sortedMatches[0], height='300', width='500')
                if retCode == 0:
                    #######################################################
                    # expirimental 'py' file execution do not enable      #
                    # unless you know what you are doing                  #
                    #######################################################
                    #if fileType == 'txt':
                    openFile = open(pathToAutoKeys + choice , 'r')
                    readFile = openFile.read().rstrip('\n')
                    openFile.close()
                    ############################################
                    # Sends selection to keyboard using AK API #
                    ############################################
                    keyboard.send_keys(readFile.replace('\n', '<shift>+<enter>'))
                    #######################################################
                    # expirimental py file execution do not enable unless #
                    # you know what you are doing                         #
                    #######################################################
                    #elif fileType == 'py':
                    #    test = choice.lstrip('/')
                    #    dialog.info_dialog("Autokey Search Tool", "Output:\n" + test)
                    #    engine.run_script(test)
