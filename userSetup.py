#Andrew Python Development Rig
#Andrew Willis 2013 [MNC]

import maya.utils as utils
import maya.cmds as cmds
import maya.mel as mel
import imp
import maya.OpenMaya as om
import getpass

#Determining root path
SERVERlis='Z:/development/temporary/'

def launcherscr(scr,srvrname):
    exec('import '+scr) in globals()
    exec('reload('+scr+')')in globals()
    return

def BEFORESAVEfn(*args):
    global CURRENTLAYERvar,DASTATlis,ALLPANELlis
    CURRENTLAYERvar=cmds.editRenderLayerGlobals(q=True, crl=True)
    cmds.editRenderLayerGlobals(crl='defaultRenderLayer')
    ALLPANELlis=cmds.getPanel(type='modelPanel')
    DASTATlis=[]
    for chk in ALLPANELlis:
        DASTATlis.append(cmds.modelEditor(chk,q=True,da=True))
        cmds.modelEditor(chk,e=True,da='wireframe')
    return

def AFTERSAVEfn(*args):
    global CURRENTLAYERvar,DASTATlis,ALLPANELlis
    cmds.editRenderLayerGlobals(crl=CURRENTLAYERvar)
    cnt=0
    for chk in ALLPANELlis:
        cmds.modelEditor(chk,e=True,da=DASTATlis[cnt])
        cnt+=1
    return

def menutls(*args):
    gMainWindow = mel.eval('$temp1=$gMainWindow')
    mainzmenu=cmds.menu(tearOff=True,l='Python Development Tools',p=gMainWindow)
    cmds.menuItem(parent=mainzmenu, l='Python Script Compiler',c=lambda*args:launcherscr('mayaPyCompiler',SERVERlis))
    BEFORESAVECALLBACKvar = om.MSceneMessage.addCallback(om.MSceneMessage.kBeforeSave,BEFORESAVEfn)
    AFTERSAVECALLBACKvar = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterSave,AFTERSAVEfn)
    return
    
utils.executeDeferred (menutls)
