#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# autowx2 - genpastable.py
# generates the pass table and recording plan for tne next few days and the appropriate plot
#
# GANTT Chart with Matplotlib
# Sukhbinder
# inspired by:
# https://sukhbinder.wordpress.com/2016/05/10/quick-gantt-chart-with-matplotlib/
# taken from
# https://github.com/fialhocoelho/test/blob/master/plot/gantt.py
# 

from autowx2 import *
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import HOURLY, DAILY, DateFormatter, rrulewrapper, RRuleLocator 
import numpy as np

def t2humanHM(timestamp):
    '''converts unix timestamp to human readable format'''
    return strftime('%H:%M', time.localtime(timestamp))
  
 
def _create_date(timestamp):
    """Creates the date from timestamp"""
    mdate = matplotlib.dates.date2num(datetime.fromtimestamp(timestamp))
    return mdate
 
def CreateGanttChart(listNextPasesListList):
    """
        Create gantt charts with matplotlib
    """ 

    ylabels = []
    customDates = []
    
    i=1
    for tx in listNextPasesListList:
        ylabel,startdate,enddate=tx
        ylabels.append("%s (%1i)" % (ylabel, i) )
        #ylabels.append("%s" % (ylabel) )
        customDates.append([_create_date(startdate),_create_date(enddate)])
        i+=1
             
    ilen=len(ylabels)
    pos = np.arange(0.5,ilen*0.5+0.5,0.5)
    task_dates = {}
    for i,task in enumerate(ylabels):
        task_dates[task] = customDates[i]
    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(111)
    for i in range(len(ylabels)):
         ylabelIN,startdateIN,enddateIN=listNextPasesListList[i]
         start_date,end_date = task_dates[ylabels[i]]
         ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date, height=0.3, align='center', edgecolor='black', color='navy', alpha = 0.95)
         ax.text(end_date, (i*0.5)+0.55,' %s | %s' % (t2humanHM(startdateIN), ylabelIN ), ha='left', va='center', fontsize=7, color='gray')

    locsy, labelsy = plt.yticks(pos,ylabels)
    plt.setp(labelsy, fontsize = 8)
    ax.axis('tight')
    ax.set_ylim(ymin = -0.1, ymax = ilen*0.5+0.5)
    ax.grid(color = 'silver', linestyle = ':')
    ax.xaxis_date()
    
    #FAKE,startdate,FAKE=listNextPasesListList[0]
    #minutOdPelnej = int(datetime.fromtimestamp(time.time()).strftime('%M'))
    #plotStart = int(time.time() - minutOdPelnej*60)
    #print t2human(plotStart)
    #ax.set_xlim(_create_date(plotStart), _create_date(enddate+600))

    
    Majorformatter = DateFormatter("%H:%M\n%d-%b")
    ax.xaxis.set_major_formatter(Majorformatter)

    labelsx = ax.get_xticklabels()
    #plt.setp(labelsx, rotation=30, fontsize=10)
    plt.setp(labelsx, rotation=0, fontsize=7)
    plt.title('Transit plan for %s, generated %s' % (stationName, t2human(time.time()) ) )
 
    font = font_manager.FontProperties(size='small')
    ax.legend(loc=1,prop=font)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(ganttNextPassList)



def listNextPasesHtml(passTable, howmany):
    i=1
    output="<table>\n"
    output+="<tr><td>#</td><td>satellite</td><td>start</td><td>duration</td><td>peak</td><td>azimuth</td><td>freq</td><td>process with</td><tr>\n"
    
    for satelitePass in passTable[0:howmany]:
        satellite, start, duration, peak, azimuth = satelitePass
        freq   = satellitesData[satellite]['freq']
        processWith = satellitesData[satellite]['processWith']
        
        output+="<tr><td>%i</td><td>%s</td><td>%s</td><td>%s</td><td>%s°</td><td>%s° (%s)</td><td>%sHz</td><td>%s</td><tr>\n" % (i, satellite, t2human(start), t2humanMS(duration), peak, azimuth, azimuth2dir(azimuth), freq, processWith)
        i+=1
    
    output+="</table>\n"
    
    return output

def listNextPasesList(passTable, howmany):
    output = []
    for satelitePass in passTable[0:howmany]:
        satellite, start, duration, peak, azimuth = satelitePass
        freq   = satellitesData[satellite]['freq']
        processWith = satellitesData[satellite]['processWith']
        
        output.append( [satellite, start, start+duration] )
    return output



def saveToFile(filename, data):
    plik = open(filename,"w") 
    plik.write(data) 
    plik.close() 


if __name__ == "__main__":

    # recalculate table of next passes
    passTable = genPassTable(howmany=50)
    listNextPasesHtmlOut = listNextPasesHtml(passTable, 100)
    saveToFile(htmlNextPassList, listNextPasesHtmlOut)
    
    listNextPasesListList = listNextPasesList(passTable, 20)
    CreateGanttChart(listNextPasesListList)