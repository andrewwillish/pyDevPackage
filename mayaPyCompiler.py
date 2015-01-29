#Python Compiler and Dispatcher
#Andrew Willis 2013

import maya.cmds as cmds
import os
import imp
import sys, shutil

if cmds.window('PyCompiler', exists=True):cmds.deleteUI('PyCompiler', window=True)

#Determining root path
rootPathVar=os.path.dirname(os.path.realpath(__file__)).replace('\\','/')

class PYCOMPILERcls:
    def __init__(self):
        global SERVERlis,SCRIPTINDIRtxtscr, WORKINGDIRtxtfld, TARGEToptmn, SEARCHvar
        cmds.window('PyCompiler',t='Python Compiler',s=False)
        cmas=cmds.columnLayout(adj=True)

        #get working directory
        try:
            OPENvar=open(rootPathVar+'/workingdir.txt','r')
            WORKINGDIRvar=OPENvar.readlines()[0]
            OPENvar.close()       
        except:
            WORKINGDIRvar=rootPathVar
        
        f1=cmds.frameLayout(l='WORKING DIRECTORY',w=300)
        A=cmds.columnLayout(adj=True)
        cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 250), (2, 45)])
        WORKINGDIRtxtfld=cmds.textField(tx=WORKINGDIRvar)
        cmds.button(l='...',c=self.SELDIRfn)
        cmds.columnLayout(adj=True,p=A)
        cmds.separator()
        
        f2=cmds.frameLayout(l='SCRIPT COMPILER & DISPATCH',p=cmas)
        b=cmds.columnLayout(adj=True)
        cmds.text(l='Note:')
        cmds.text(l='Not every python files listed here are engineered for maya.')
        cmds.separator()
        SEARCHvar=cmds.textField(cc=self.SEARCHfn,pht='search script')
        SCRIPTINDIRtxtscr=cmds.textScrollList(dcc=self.SCRPTLAUNCHERfn,h=300)
        sys.path.append(str(WORKINGDIRvar))
        if os.path.isdir(WORKINGDIRvar)==True:
            PYSCRIPTlis=os.listdir(WORKINGDIRvar)
            for chk in PYSCRIPTlis:
                if chk.endswith('.py'):
                    cmds.textScrollList(SCRIPTINDIRtxtscr,e=True,a=chk[:-3])
        else:
            PYSCRIPTlis=[]
        cmds.separator()
        TARGEToptmn=cmds.optionMenu(l='Target: ',w=295)
        cmds.menuItem(l='')

        if os.path.isfile(rootPathVar+'/dispatchtarget.txt'):
            TARGETopn=open(rootPathVar+'/dispatchtarget.txt','r')
        else:
            tempOp=open(rootPathVar+'/dispatchtarget.txt','w')
            tempOp.close()
            TARGETopn=open(rootPathVar+'/dispatchtarget.txt','r')
        
        TARGETlis=TARGETopn.readlines()
        TARGETopn.close()
        for chk in TARGETlis:
            cmds.menuItem(chk[:-2])
        cmds.button(l='REGISTER NEW TARGET',bgc=[1.0,0.643835616566,0.0],c=self.REGISTERTARGETfn)
        cmds.button(l='DISPATCH>>',w=90,bgc=[1.0,0.643835616566,0.0],c=self.DISPATCHERfn)
        cmds.separator(p=b)

        cmds.button(l='REFRESH',c=self.REFRESHfn,p=cmas)
        cmds.showWindow()        
        return

    def SEARCHfn(self,*args):
        global SERVERlis,SCRIPTINDIRtxtscr, WORKINGDIRtxtfld, TARGEToptmn, SEARCHvar
        TEMPlis=[]
        WORKDIRvar=cmds.textField(WORKINGDIRtxtfld,q=True,tx=True)
        if os.path.isdir(WORKDIRvar)==True:
            PYSCRIPTlis=os.listdir(WORKDIRvar)
            print PYSCRIPTlis
            for chk in PYSCRIPTlis:
                if chk.endswith('.py'):
                    TEMPlis.append(chk[:-3])
        else:
            TEMPlis=[]

        cmds.textScrollList(SCRIPTINDIRtxtscr,e=True,ra=True)
        for chk in TEMPlis:
            if chk.find(str(cmds.textField(SEARCHvar,q=True,tx=True)))<>-1:
                cmds.textScrollList(SCRIPTINDIRtxtscr,e=True,a=chk)
        return

    def SELDIRfn(self,*args):
        global SERVERlis,SCRIPTINDIRtxtscr, WORKINGDIRtxtfld
        DIRvar=cmds.fileDialog2(dir=cmds.textField(WORKINGDIRtxtfld,q=True,tx=True),cap='Select working directory',fm=3)
        if DIRvar==None:
            cmds.error('[CANCELLED BY USER]')
        else:
            OPENvar=open(rootPathVar+'/workingdir.txt','w')
            OPENvar.write(DIRvar[0])
            OPENvar.close()    
            import mayaPyCompiler
            reload( mayaPyCompiler)
        return

    def REGISTERTARGETfn(self,*args):
        global SERVERlis,SCRIPTINDIRtxtscr, WORKINGDIRtxtfld, TARGEToptmn
        DIRvar=cmds.fileDialog2(dir=cmds.textField(WORKINGDIRtxtfld,q=True,tx=True),cap='Select target directory',fm=3)
        if DIRvar==None:
            cmds.error('[CANCELLED BY USER]')
        else:
            OPENvar=open(rootPathVar+'/dispatchtarget.txt','a')
            OPENvar.write(DIRvar[0]+'\r\n')
            OPENvar.close()    
            import mayaPyCompiler
            reload(mayaPyCompiler)
        return

    def DISPATCHERfn(self,*args):
        global SERVERlis,SCRIPTINDIRtxtscr, WORKINGDIRtxtfld, TARGEToptmn
        if cmds.textScrollList(SCRIPTINDIRtxtscr,q=True,si=True)==None:
            cmds.confirmDialog(icon='warning',title='message', message='Select script to be dispatched!',button=['Ok'])
            cmds.error('[SELECT SCRIPT TO BE DISPATCHED]')
            
        if cmds.optionMenu(TARGEToptmn,q=True,v=True)=='':
            cmds.confirmDialog(icon='warning',title='message', message='Select dispatch target!',button=['Ok'])
            cmds.error('[SELECT DISPATCH TARGET]')
                        
        SOURCEvar=cmds.textField(WORKINGDIRtxtfld,q=True,tx=True)+'/'+cmds.textScrollList(SCRIPTINDIRtxtscr,q=True,si=True)[0]+'.pyc'
        TARGETvar=cmds.optionMenu(TARGEToptmn,q=True,v=True)+'/'+cmds.textScrollList(SCRIPTINDIRtxtscr,q=True,si=True)[0]+'.pyc'
        
        if os.path.isfile(TARGETvar)==True:
            REPLYvar=cmds.confirmDialog(icon='question',title='message', message='There is another script exist with the same file. Continue?',button=['Yes','No'])
            if REPLYvar=='No':
                cmds.error('[CANCELLED BY USER]')
            else:
                try:
                    self.SCRPTLAUNCHERfn()
                except:
                    print ''
                shutil.copy(SOURCEvar, TARGETvar)
                cmds.confirmDialog(icon='information',title='Message',message='Script dispathed!',button=['Ok'])
        else:
            try:
                self.SCRPTLAUNCHERfn()
            except:
                print ''
            shutil.copy(SOURCEvar, TARGETvar)
            cmds.confirmDialog(icon='information',title='Message',message='Script dispathed!',button=['Ok'])
        return    

    def SCRPTLAUNCHERfn(self,*args):
        global SERVERlis,SCRIPTINDIRtxtscr, WORKINGDIRtxtfld
        SELECTEDSCRvar=cmds.textScrollList(SCRIPTINDIRtxtscr,q=True,si=True)
        SELECTEDSCRvar=SELECTEDSCRvar[0]

        imp.load_source(SELECTEDSCRvar,cmds.textField(WORKINGDIRtxtfld,q=True,tx=True)+'/'+SELECTEDSCRvar+'.py')
        
        #exec('import '+SELECTEDSCRvar) in globals()
        #exec('reload('+SELECTEDSCRvar+')')in globals()
        return
    
    def REFRESHfn(self,*args):
        import mayaPyCompiler
        reload (mayaPyCompiler)
        return

PYCOMPILERcls()