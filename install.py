import shutil
import os
import sys
import Tkinter, tkFileDialog, tkMessageBox
import filecmp
import unittest

src = os.getcwd() + '\pre-commit'
dst = ''

def getDestinationPathInteractive():
    print('Specify your repository directory:')
    path = raw_input()
    #path = 'E:/test1/.git/hooks'
    #path = path.replace('\\', '/')
    if not os.path.isdir(path):
        print("The specified path doesn't exist.")
        raw_input()
        sys.exit(1) 
    else:
        return path
    
def getDestinationPathWin():
    root = Tkinter.Tk()
    root.withdraw()
    path = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select a directory')
    if path == '':
        tkMessageBox.showerror('Error', "Installation was cancelled.")
        sys.exit(1)
    return path
         
def checkIfPathValid(path):
    if path[-1] in ['/','\\']:
        path = path[:-1]
        
    # Get path to /.git folder
    if path[-10:] in ['.git\\hooks','.git/hooks']:
        return path[:-6]
    elif (path[-4:] == '.git'):
        return path
    elif (os.path.isdir(path + '/.git')):
        return path + '/.git'
    else:
        errorMsg = "The specified directory doesn't contain a git repository."
        if os.name == 'nt':
            tkMessageBox.showerror('Error', errorMsg)
        else:
            print(errorMsg)
            raw_input()
        sys.exit(1)        
        
def fileExists(dst):
    if filecmp.cmp(os.getcwd() + '\pre-commit', dst + '/hooks/pre-commit'):
        infoMsg = "The specified repository already contains the hook."
        if os.name == 'nt':
            tkMessageBox.showinfo('', infoMsg)
        else:
            print(infoMsg)
            raw_input()
        sys.exit(0)
    else:
        yesnoMsg = "The specified repository already contains some pre-commit hook. Do you want to overwrite it?"
        successMsg = "Installation completed succesfully!"
        failMsg = "Installation was cancelled."
        
        if os.name == 'nt':
            if tkMessageBox.askyesno('Warning', yesnoMsg):
                shutil.copyfile(src, dst + '/hooks/pre-commit')
                tkMessageBox.showinfo('', successMsg)
                sys.exit(0)
            else:
                tkMessageBox.showinfo('', failMsg)
                sys.exit(1)  
        else:
            print(yesnoMsg)
            if raw_input().lower()[0] == 'y':
                shutil.copyfile(src, dst + '/hooks/pre-commit')
                print(successMsg)
                raw_input()
                sys.exit(0)
            else:
                print(failMsg)
                raw_input()                
                sys.exit(1)      

def printHelp():
    print('usage: install.py [<path>]')
    print('<path> is the path to git repository, where you want the hook to be installed')
    raw_input()
    sys.exit(1)        
   
   
   
    
args = sys.argv
if not len(args) in [1, 2]:
    printHelp()
elif len(args) == 2:
    if not os.path.isdir(args[1]):
        printHelp()
    else:
        dst = args[1]
else:
    if os.name == 'nt':
        dst = getDestinationPathWin()
    else:
        dst = getDestinationPathInteractive()

dst = checkIfPathValid(dst)
if not os.path.isdir(dst + '/hooks'):
    os.makedirs(dst + '/hooks')

if os.path.isfile(dst + '/hooks/pre-commit'):
    fileExists(dst)
else:
    infoMsg = "Installation completed succesfully!"
    shutil.copyfile(src, dst + '/hooks/pre-commit')
    if os.name == 'nt':
        tkMessageBox.showinfo('', infoMsg)
    else:
        print(infoMsg)
        raw_input()
    sys.exit(0)
    
    

class UnitTests(unittest.TestCase):
    def testIfPathValid(self):
        self.assertEqual(checkIfPathValid('C:/Git/.git/hooks/'), 'C:/Git/.git')
        self.assertEqual(checkIfPathValid('C:/Git/.git/'), 'C:/Git/.git')

    
    
    
    
    
    
    
    
    
    
    