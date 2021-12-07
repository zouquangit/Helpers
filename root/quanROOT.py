'''
--------Collective ROOT functions---------  
usage:from quanROOT import myROOT as mR---
@author:Quan
@date:Nov.17 2021
@email:zouquan@ihep.ac.cn        
'''
from ROOT import TDirectoryFile,TDirectory,TKey,TTree,TChain,TFile,gDirectory,gStyle,RDataFrame
import ROOT
class myROOT(object):
  def __init__(self,inputFile='test.root',print_msg='false'):#'testNewMC-MC2018MU_D2Kpi.root'
    """
    intialize the class
    inputfile: supply the filename to begin.
    If it's a list of file,please use a txt file. TODO
    """  
    self.inFile=TFile(inputFile,'r')
    #gDirectory.cd(directory)
    #self.inTree=gDirectory.Get(trName)
    #self.df=RDataFrame(self.inTree)
    self.test='---initialize successfully---\n The file is like:\n'
    print(self.test)
    #print(gDirectory.ls())
  def __deBUG__(self):
    """
    debug function 
    """
    pass 
  def getTree(self,absPath='/BcTuple1',trName='DecayTree'):
    reTr=self.inFile.cd(absPath)
    return gDirectory.Get(trName)
  def setDataFrame(self,thisTree):
    return RDataFrame(thisTree)
  def checkDir(self,currentDir,levels=0,print_msg='False'):
    """
    To check the folder hierarchy
    print_msg: to save the output into a file
    """
    #self.inFile.ls()
    listOfKeys=currentDir.GetListOfKeys()
    levels+=1
   
    #print(levels)
    #topDir=[k for k in listOfKeys if k.GetClassName()=='TDirectoryFile']
    for key in listOfKeys:
      if levels==1:print('\n+++++++++++\n')
      name=key.GetClassName()
      if name=='TDirectoryFile':
        print("-"*levels+">"+key.GetName())
        #print(levels)
        #TKey class don't have attr GetPath,key.GetMotherDir()->TDirectory
        nameCycle=key.GetName()+":"+str(key.GetCycle())
        par=key.GetMotherDir()
        curr=par.Get(key.GetName())
        #print(curr)
        self.checkDir(curr,levels)

      else:
        print('-'*levels+'>'+key.GetClassName()+':'+key.GetName())
    return
        
  def printBr(self,tr):
    self.inTree.GetEntries()
    self.inTree.Show(1)
  
  def saveHisto(self,tree,*br):
    tmpTree=tree
    #tmpTree.Show()
    leaves=tmpTree.GetListOfLeaves()
    for leave in leaves:
      tree_dict[key].append(leave.GetName())
    dataFrame=ROOT.RDataFrame(tmpTree)
 
    HistogramFile = ROOT.TFile("histo"+key+".root", "recreate")
    histogramlist = br
    for histoiter in histogramlist:
      storinghistogram = dataFrame.Histo1D(histoiter)
      storinghistogram.SetDirectory(HistogramFile)
      storinghistogram.SetNameTitle(key,key)
      storinghistogram.Write()
      del storinghistogram
    print("Wrote out histogram file at "+HistogramFile.GetName())
  def makeSideband(self,thisTree,x,xlow,xup):
    '''
    overload scenario 1
    '''
    assert xlow<xup
    dataFrame=self.setDataFrame(thisTree)
    df=dataFrame.Filter((x+'<'+str(xlow))+' || '+(x+'>'+str(xup)) )
    #branches=[]
    #for br in thisTree.GetListOfBranches():
      #branches.append(br.GetName()
    branchList = ROOT.vector('string')()
    for branch in thisTree.GetListOfBranches():
      branchList.push_back(branch.GetName())
    df.Snapshot("tree",x+'_sideband.root',branchList)
    
if __name__ == '__main__':#test func, only run standalone
  mR=myROOT()
  mR.checkDir(mR.inFile,0)
  #mR.printBr()






