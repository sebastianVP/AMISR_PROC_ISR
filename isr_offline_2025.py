"""
Autor: Alexander Valdez
AKA: Magic 
Fecha de creación: [27/02/2025]
Descripción: [Procesamiento ISR OFF-LINE AMISR-14]
Versión: [1.0]
"""
#####################################
######## LIBRERIAS ##################
import os,sys,json
import time
import datetime
from multiprocessing import Process
from shutil import rmtree
from schainpy.controller import Project
from multiprocessing.connection import wait
from schainpy.model.io.utilsIO import MergeH5
##########################################
##########################################

dty  = datetime.date.today()
str1 = dty+datetime.timedelta(days=1) # un dia despues
str2 = dty-datetime.timedelta(days=1) # un dia antes
today     = dty.strftime("%Y/%m/%d")
tomorrow  = str1.strftime("%Y/%m/%d")
yesterday = str2.strftime("%Y/%m/%d")
##########################################
##########################################

print("today",today)
print("tomorrow",tomorrow)
print("yesterday",yesterday)

##############################################
path          = "/mnt/data_amisr"
outPath       = "/mnt/DATA/AMISR14/2025/ISR"
path_hdf5_out = "/mnt/DATA/data2Fabiano/POWER_H5_AMISR/2025"
##############################################
########### PARAMETROS DE TIEMPO##############
xmin      = 7
xmax      = 18
localtime = 1
startDate = yesterday
endDate   = today
startTime = "07:00:00"
endTime   = "17:59:59"
Nday      = 3
###############################################
##############################################
nChannels = 2
nFFT      = 1
IPPms     = 10
nCode     = 1
nBaud     = 1
dataList  = ["data_spc","nIncohInt","utctime"]
nipp      = (1000/IPPms)/nChannels
ippP10sec = nipp*10
print(f"{ippP10sec} profiles in 10 seconds")



def schain(channel,Outdata,factor=1):
    """
    This method will be called many times so here you should put all your code
    """
    if os.path.exists(Outdata):
        print("Outdata {}: ".format(channel), Outdata)
    else :
        os.mkdir(Outdata)

    controllerObj = Project()
    controllerObj.setup(id = channel, name='isr offline', description='desc')
    controllerObj.start()

