#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: renm79@126.com
@Version: 1.2.2.1
@Date: 2011-7-24
@Note: 利用正则表达式发掘SSR程序的窗口版本
        串行多线程程序
        稳定发展版本
        
        修正控件大小不能调整的问题
        进一步做界面调整（2011-7-26）
        
'''

import os, sys, re
import wx, wx.grid
import threading

class MainFrame(wx.Frame):
    def __init__(self):
        """
        """
        wx.Frame.__init__(self, None, -1, 'regexSSRw')        
        panel = wx.Panel(self, -1)
        ## SIZER --------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL) # 最外面的sizer
        upSizer = wx.BoxSizer(wx.HORIZONTAL) # 控制上半部
        ## CONTROL ------------------------------------------------------------
        pnlResult = self.__ResultPanel(panel)
        pnlSeq = self.__InputSeqPanel(panel)
        pnlMid = self.__MidPanel(panel)
        pnlRgt = self.__RightPanel(panel)
        ## BARS
        self.__createMenuBar() # 添加菜单栏
        self.__createStatusBar() # 添加状态栏
        ## LAYOUT -------------------------------------------------------------
        ## 如果不需要控件自动缩放，第二个参数为0即可
        upSizer.Add(pnlSeq, 1, wx.EXPAND|wx.ALL, 1)
        upSizer.Add(pnlMid, 0, wx.EXPAND|wx.ALL, 1)
        upSizer.Add(pnlRgt, 0, wx.EXPAND|wx.ALL, 1)
        sizer.Add(upSizer, 0, wx.EXPAND|wx.ALL, 1)
        sizer.Add(pnlResult, 1, wx.EXPAND|wx.ALL, 1)
        ## RESIZE -------------------------------------------------------------
        panel.SetSizer(sizer)
        panel.Fit()
        self.Fit()
        self.Center()
        ## BINDING ------------------------------------------------------------
        self.Bind(wx.EVT_BUTTON, self.__On_btnRun_Click, self.btnRun)
        self.Bind(wx.EVT_BUTTON, self.__On_btnOpen_Click, self.btnOpen)
    
    ## 构建PANEL ---------------------------------------------------------------
    def __InputSeqPanel(self, p):
        """
        2011-7-25 21:34:59
        """
        ## PANEL
        panel = wx.Panel(p, -1, pos=wx.DefaultPosition)
        ## SIZER
        sizer = wx.BoxSizer(wx.VERTICAL)
        ## CONTROLS
        labInfoA = wx.StaticText(panel, -1, 
                "Input or load Fasta formated sequence(s) here")
        self.txtSeq = wx.TextCtrl(panel, -1, value='', 
                    style=wx.TE_MULTILINE|wx.TE_RICH2, size=(-1,-1))
        self.txtSeq.SetMaxLength(0)
        ## LAYOUT
        sizer.Add(labInfoA, 0, wx.FIXED_MINSIZE|wx.ALL, 5)
        sizer.Add(self.txtSeq, 1, wx.EXPAND|wx.ALL, 5)        
        ## FIT
        panel.SetSizer(sizer)
        panel.Fit()
        return panel
    
    def __ResultPanel(self, p):
        """
        2011-7-25 21:42:52
        """
        ## PANEL
        panel = wx.Panel(p, -1, pos=wx.DefaultPosition)
        ## SIZER
        sizer = wx.BoxSizer(wx.VERTICAL)
        ## CONTROLS
        labInfoB = wx.StaticText(panel, -1, "SSR(s)")
        self.gridSsr = self.__CreateGrid(panel)
        ## LAYOUT
        sizer.Add(labInfoB, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.gridSsr, 1, wx.EXPAND|wx.ALL, 5)
        ## FIT
        panel.SetSizer(sizer)
        panel.Fit()
        return panel
        
        
    def __MidPanel(self, p):
        """
        2011-7-25 21:44:21
        """
        ## *PANEL
        panel = wx.Panel(p, -1, pos=wx.DefaultPosition)
        ## *SIZER
        sizer = wx.BoxSizer(wx.VERTICAL)
        ## *CONTROLS
        self.btnOpen = wx.Button(panel, -1, 'Open')
        labInfoC = wx.StaticText(panel, -1, 
                    'a) The maximum\n motif-length.')        
        labInfoD = wx.StaticText(panel, -1, 
                    'b) The minimum\n number of repeats.') 
        ## ComboBox
        liMotif = ['dimer','trimer','tetramer',
                 'pentamer','hexamer','heptamer',
                 'octamer','nonamer','decamer']
        self.comboBox = wx.ComboBox(panel, -1, choices=liMotif, 
            style=wx.CB_READONLY)
        ## Spin
        self.spin = wx.SpinCtrl(panel, -1, value=wx.EmptyString,
            style=wx.SP_ARROW_KEYS, size=(70,22), min=3, max=100, initial=5)        
        ## *LAYOUT
        sizer.Add(self.btnOpen, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(wx.StaticLine(panel, -1, size=(-1,2), 
            style=wx.LI_HORIZONTAL), 0, wx.EXPAND|wx.ALL, 10) # 一条分割线        
        sizer.Add(labInfoC, 0, wx.FIXED_MINSIZE|wx.ALL, 5)
        sizer.Add(self.comboBox, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(labInfoD, 0, wx.FIXED_MINSIZE|wx.ALL, 5)
        sizer.Add(self.spin, 0, wx.FIXED_MINSIZE|wx.ALL, 5)        
        ## *FIT
        panel.SetSizer(sizer)
        panel.Fit()
        return panel        
    
    def __RightPanel(self, p):
        """
        2011-7-25 21:50:09
        """
        ## PANEL
        panel = wx.Panel(p, -1, pos=wx.DefaultPosition)
        ## SIZER
        sizer = wx.BoxSizer(wx.VERTICAL)
        ## CONTROLS
        labInfoE = wx.StaticText(panel, -1, 'CSV compatible\n with Excel')
        self.btnRun = wx.Button(panel, -1, 'Scan SSR')  
        self.btnSaveText = wx.Button(panel, -1, 'Save to Text')
        self.btnSaveCSV = wx.Button(panel, -1, 'Save to CSV')  
        self.gauge = wx.Gauge(panel, range=100, size=(-1,20))      
        ## LAYOUT
        sizer.Add(self.btnRun, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(wx.StaticLine(panel, -1, size=(-1,2), 
            style=wx.LI_HORIZONTAL), 0, wx.EXPAND|wx.ALL, 10) # 一条分割线 
        sizer.Add(self.btnSaveText, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.btnSaveCSV, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(labInfoE, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.gauge, 0, wx.EXPAND|wx.ALL, 5)
        ## FIT
        panel.SetSizer(sizer)
        panel.Fit()
        return panel
        
#
#    def __Panel(self, p):
#        """
#        
#        """
#        ## PANEL
#        panel = wx.Panel(p, -1, pos=wx.DefaultPosition)
#        ## SIZER
#        ## CONTROLS
#        ## LAYOUT
#        ## FIT 
#        panel.SetSizer(sizer)
#        panel.Fit()
#        return panel
#   

    ## 菜单栏 工具栏 状态栏 ---------------------------------------------------
    ## 菜单栏数据
    def __menuData(self): 
        return [("File", (
                    (u"Open", "Open Sequence File(s)", self.__On_btnOpen_Click),
                    ("", "", ""),
                    ("Exit", u"Exit", self.__On_CloseWindow))),
                ("Tools", (                              
                    ("Extract Sequence(s)", "Scan SSR", self.__On_btnRun_Click),)),                
                (u"Help",(
                    (u"Help", u"Help Document", None),
                    ("", "", ""),
                    ("About", "About this program", None)))]
    
    ## 创建菜单
    def __createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.__menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.__createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)
    
    def __createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.__createMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu)
            else: self.__createMenuItem(menu, *eachItem)
        return menu        
    
    def __createMenuItem(self, menu, label, status, handler, kind = wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem) 
        
    ## 创建工具栏
    def __createStatusBar(self):
        """
        2011-7-27 8:52:55
        """
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-1, -1])
    
    ## ------------------------------------------------------------------------ 

    ## 构建控件 ---------------------------------------------------------------
    def __CreateGrid(self, p):
        """
        构建一个表格控件，以展示运算结果
        2011-7-24 20:31:32
        """
        grid = wx.grid.Grid(p)
        grid.CreateGrid(10, 7)
        ## 设置表头
        grid.SetColLabelValue(0, 'Sequence')
        grid.SetColLabelValue(1, 'Motif')
        grid.SetColLabelValue(2, 'Repeats')
        grid.SetColLabelValue(3, 'Start')
        grid.SetColLabelValue(4, 'End')
        grid.SetColLabelValue(5, 'SSR_len')
        grid.SetColLabelValue(6, 'Seq_len')
        ## 设置列宽
        grid.SetColSize(0, 200)
#        grid.SetColSize(1, 50)
#        grid.SetColSize(1, 80)
#        grid.SetColSize(1, 50)
#        grid.SetColSize(1, 50)
#        grid.SetColSize(1, 50)
#        grid.SetColSize(2, 50)
        return grid
    
    def __DialogOpenSeqFiles(self):
        _sFile = ''
        style = wx.OPEN|wx.CHANGE_DIR
        wildcard = 'Fasta Formats (*.fas;*.fasta;*.fa)|*.fas;*.fasta;*.fa|'\
                    'All Formats (*.*)|*.*'
        dialog = wx.FileDialog(self, 
                    message="Choose Sequences file(s)", 
                    defaultDir="", defaultFile="", 
                    wildcard=wildcard, style=style, 
                    pos=wx.DefaultPosition)
        if dialog.ShowModal() == wx.ID_OK:
            _sFile = dialog.GetPath()
            ## 先删除以前的运算结果
            self.gridSsr.DeleteRows(0, self.gridSsr.GetNumberRows())
            ## 复位进度条
            self.gauge.SetValue(0)
            
        dialog.Destroy()
        return _sFile
    
    
    ## 控件响应处理函数 -------------------------------------------------------
    def __On_btnRun_Click(self, evt):
        """
        'Run'按钮点击时
        2011-7-24 21:23:13
        """
        
        ## 获得运行参数
        if self.comboBox.GetValue() == '':
            dial = wx.MessageDialog(None, 
                    'Please set the maximum motif length', 'Error',
                    wx.OK|wx.ICON_ERROR)
            dial.ShowModal()
        else: 
            ## 开始读取用户输入的内容  
            liLines = self.txtSeq.GetValue().split('\n')
            liFasta = FastaLoader(liLines).liFasta
            sMax = self.comboBox.GetValue()
            sRep = self.spin.GetValue()
            th = SsrFindingTH(self, liFasta, (sMax, sRep))
            th.start()
        
    def __On_btnOpen_Click(self, evt):
        """
        "open"按钮点击时
        打开一个对话框，让用户选择序列文件（单选）
        然后将文件的内容读入txtSeq文本框
        2011-7-25 14:43:21
        """
#        print self.comboBox.GetValue()
        sFile = self.__DialogOpenSeqFiles()
        if sFile != '':
            # 用户选择了序列文件
            s = open(sFile, 'r')
            self.txtSeq.SetValue(s.read())
            s.close()
            
    def __On_CloseWindow(self, evt):
        """
        2011-7-27 8:30:18
        """
        self.Destroy()
        
    ## 事件处理函数 -----------------------------------------------------------
    def SsrReport(self, msg):
        """
        得到一个SSR位点信息后
        2011-7-24 22:10:14
        """
        liMsg = msg.split('\t')
        self.gridSsr.AppendRows(1) # 追加一行
        iInsert = self.gridSsr.GetNumberRows() 
        # 已经有的行数-1即为要插入的行号， 因为刚刚在上面追加了一行
        for i in range(len(liMsg)):
            self.gridSsr.SetCellValue(iInsert-1, i, liMsg[i])
    
    def UpdateGauage(self, msg):
        """
        更新进度条
        2011-7-25 20:09:36
        """
        self.gauge.SetValue(int(msg))

## 线程类 *********************************************************************
class SsrFindingTH(threading.Thread):
    """
    进行SSR发掘的线程
    2011-7-24 21:39:45
    """
    def __init__(self, frame, liFasta, tpPar):
        """
        2011-7-24 21:58:31
        """
        dcMotif = { 'dimer': 2,     'trimer': 3,    'tetramer': 4,
                    'pentamer': 5,  'hexamer': 6,   'heptamer': 7,
                    'octamer': 8,   'nonamer': 9,   'decamer': 10}        
        threading.Thread.__init__(self)
        self.frame = frame
        self.liFasta = liFasta
        self.iMax = dcMotif[tpPar[0]]
        self.iRep = int(tpPar[1])
        self.iCount = 0 # 当前处理到第几条序列
        
    def run(self):
        """
        2011-7-24 21:58:35
        """        
        iTotalSeq = len(self.liFasta) # 总共有多少条序列        
        for dcFas in self.liFasta:
            sSeq = dcFas['Sequence'].lower()
            rgxSsr = RgxSSR(sSeq, 2, self.iMax, self.iRep)
            self.iCount += 1
            iPercent = (self.iCount * 100) / iTotalSeq
            wx.CallAfter(self.frame.UpdateGauage, str(iPercent))
            if rgxSsr.CountSSR() > 0:  
                ## 如果存在SSR位点
                liMotif = rgxSsr.ListMotif()
                liSSR = rgxSsr.ListSSR()
                for i in range(rgxSsr.CountSSR()):
                    sTitle =  '%s of %s' %(i+1, dcFas['Desc'][1:].replace('\t', '_'))
                    sMotif = liMotif[i]
                    iRepeats = len(liSSR[i]) / len(liMotif[i])
                    iStart, iEnd = rgxSsr.GetPosition(i+1)
                    iSSRLen = len(liSSR[i])
                    iSeqLen = len(dcFas['Sequence'])
                    sOut = '%s\t%s\t%s\t%s\t%s\t%s\t%s' \
                        %(sTitle, sMotif, iRepeats, iStart, iEnd, iSSRLen, iSeqLen)
                    wx.CallAfter(self.frame.SsrReport, sOut)
                    
    
## 公用类 *********************************************************************
class RgxSSR(object):
    """
    分析一条序列中SSR位点的类
    这个类在使用前应当把字符统一转换成大写或小写
    2011-7-19 10:58:33
    """
    def __init__(self, sSequence, iMinMotif=2, iMaxMotif=6, iRepeats=5):
        """
        iMinMotif, 基序的最小长度
        iMaxMotif, 基序的最大长度
        iRepeats, 基序的重复次数
        sSequence, 目标序列
        2011-7-19
        """
        assert iMinMotif >= 2 # 基序不应为1
#        sSequence = sSequence.lower() # 全部转换成小写
        self.regex = r'(.{%s,%s}?)(\1){%s,}' \
                    %(iMinMotif, iMaxMotif, iRepeats - 1)
        # 正则表达式模式字符串
        pattern = re.compile(self.regex) # 正则表达式模式对象
        liFindAll = pattern.findall(sSequence)
        liSplit = pattern.split(sSequence)
        liGroup = self.__ListGroup_li(pattern, sSequence) # 匹配上的序列列表
        liFlank = self.__ListFlank_li(liSplit, liGroup) # 非匹配序列的列表
        self.markedUpList = self.__GetMarkedUp_li(liFlank, liGroup)
#        print liGroup
#        print liFlank
#        print self.MarkedUpList        
    
    def __ListGroup_li(self, pattern, sSequence):
        """
        列出所有SSR序列
        2011-7-19
        """
        liTemp = []
        for eachSSR in pattern.finditer(sSequence):
            liTemp.append(eachSSR.group())
        return liTemp

    def __ListFlank_li(self, liSplit, liGroup):
        """
        依次列出所有非SSR序列
        2011-7-19 21:49:10
        """
        return [liSplit[i] for i in [x*3 for x in range(len(liGroup)+1)]]
    
    def __GetMarkedUp_li(self, liFlank, liGroup):
        """
        将上面匹配到的序列和非配套序列整合到一起
        由于这个正则表达式会将形如'tttttttt'这样的序列匹配上，
        但是这个序列并不是我们想要的SSR位点
        因此这时还要将这样的序列去掉。
        合并后的序列格式如下：
        ['GT', 'atatatat', 'GCtataattttttttAG', 'ctgctgctgctg', 'ctataatgtat']
        一个上有序列跟一个SSR序列，最后面是最后一个SSR序列的下游序列
        其长度为2*n+1,n=0,1,2,3,...
        2011-7-19 23:05:44
        2011-7-20 12:30:42
        """
        liMarkedUp = []
        sTemp = ''
        for i in range(len(liGroup)):
            if len(set(liGroup[i])) == 1:
                ## 不是真的SSR
                sTemp += liFlank[i] + liGroup[i]
            else:
                ## 不为1，就是真的SSR
                liMarkedUp.append(sTemp + liFlank[i])
                liMarkedUp.append(liGroup[i])
                sTemp = ''
        liMarkedUp.append(liFlank[-1])
        return liMarkedUp

    def CountSSR(self):
        """
        计算有多少处SSR序列
        2011-7-27 12:55:07
        """
        return (len(self.markedUpList)-1)/2

    def ListSSR(self):
        """
        列出所有SSR序列，以一个List的形式返回
        2011-7-20 11:59:45
        """
        li = self.markedUpList
        return [li[i] for i in [j*2+1 for j in range((len(li)-1)/2)]]
    
    def ListMotif(self):
        """
        列出所有的基序（motif）
        2011-7-27 12:59:33
        """
        liSSR = self.ListSSR()
        liMotif = []
        for eachSSR in liSSR:
            p = re.compile(self.regex)
            liMotif.append(p.findall(eachSSR)[0][0])
        return liMotif
        # [''.join(list(set(li[i]))) for i in range(len(li))]
        
    def GetLeft(self, i):
        """
        得到某个SSR位点的上游序列
        从这个SSR的起点到上个SSR终点间的序列
        如果这是第一个SSR，那就是到序列头
        i 为第几个SSR，i=1,2,3,4,...,N
        2011-7-27 13:25:52
        """
        li = self.markedUpList
        assert i <= (len(li)-1)/2
        # 用户输入的数据不能超过实际SSR位点数。
        return li[(i-1)*2]

    def GetRight(self, i):
        """
        得到某个SSR位点的下游序列
        从这个SSR的终点到下一个SSR起点间的序列
        如果这是最后一个SSR，那就是到序列尾
        i 为第几个SSR，i=1,2,3,4,...,N
        2011-7-27 13:39:24
        """
        li = self.markedUpList
        assert i <= (len(li)-1)/2
        # 用户输入的数据不能超过实际SSR位点数。
        return li[i*2]
    
    def GetPosition(self, i):
        """
        得到某个SSR位点的位置        
        i 为第几个SSR，i=1,2,3,4,...,N
        返回一个tuple：(start,end) ,起始位置从 1 开始
        算法：1、把第几个SSR转换成markeduplist中的第几个元素
        2、把这几个之前的加起来求和，就是起始位置
        3、在加上本身序列的长度就是终止位置
        2011-7-21 10:26:05
        """
        iEle = i*2-1 # 这个SSR在self.markedUpList中对应的是第几个元素
        iStart = len(''.join(self.markedUpList[:iEle])) + 1
        iEnd = iStart + len(self.markedUpList[iEle]) - 1
        return (iStart, iEnd)    

class  FastaLoader(object):                
    '''
    读取Fasta格式文件的类-2009-11-2
    
    把读取的结果保存到一个列表里面
    列表的数据结构为：[{'Desc':'>xx|xxx|xx xxxxx','Sequence':'ATCGGCTA'},
    ......,
    {'Desc':'>xx|xxx|xx xxxxx','Sequence':'ATCGGCTA'}]
    '''
    def __init__(self, Lines_li):
        self.liFasta = self.__FastaParser_li(Lines_li)
            
    def __FastaParser_li(self, Lines_li):
        _liFasta = []
        liTemp = [] # 用来临时保存一个Fasta记录
        for i in range(0, len(Lines_li)):
            fastaLine = Lines_li[i].strip()
            if len(fastaLine) > 0:
                # 有数据内容才进行下面的分析
                if fastaLine.find('>') != -1:
                    # 说明这是描述
                    ## 先整理liTemp（如果有内容）
                    if len(liTemp) > 0:
                        ## 整理liTemp
                        _liFasta.append(self.__Fasta_dc(liTemp))
                    liTemp = []
                    liTemp.append(fastaLine)
                else:
                    liTemp.append(fastaLine)
        ##  在全部循环完整之后还要把liTemp里剩下的内容也整理了
        _liFasta.append(self.__Fasta_dc(liTemp))
        return _liFasta
            
    def __Fasta_dc(self, liTemp):
        '''
        整理liTemp里面的内容成为一个字典-2009-11-10
        
        字典的格式为{'Desc':'>xx|xxx|xx  xxxxx','Sequence':'ATCGGCTA'}
        '''
        
        _dcFasta = {'Desc':'', 'Sequence':''}
        #定义一个字典用来保存fasta格式序列信息
        ## 第一行是Contig的描述
        _dcFasta['Desc'] = liTemp[0]        
        _dcFasta['Sequence'] = ''.join(liTemp[1:])
        return _dcFasta


def main():
    app = wx.PySimpleApp()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()    

if __name__ == "__main__":
    main()