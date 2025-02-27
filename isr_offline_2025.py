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
"""
         ISR 2 BEAM OFFLINE
"""
path = os.path.dirname(os.getcwd())
path = os.path.dirname(path)
sys.path.inser(0,path)


def main(results):

    desc= "AMISR ISR 2 Beam Experiment"
    ##############################################
    path          = "/mnt/data_amisr"
    outPath       = "/mnt/DATA/AMISR14/2025/ISR"
    path_hdf5_out = "/mnt/DATA/data2Fabiano/POWER_H5_AMISR/2025"
    ##############################################
    ##### PARAMETROS DE TIEMPO-HORA ##############
    xmin      = 7
    xmax      = 18
    localtime = 1
    startDate = yesterday
    endDate   = today
    startTime = "07:00:00"
    endTime   = "17:59:59"
    Nday      = 3
    #############################################
    ##### PARAMETROS DE DIA #####################
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
    ########### PARAMETROS DE EXPERIMENTO ########
    nChannels = 2
    nFFT      = 1
    IPPms     = 10
    nCode     = 1
    nBaud     = 1
    dataList  = ["data_spc","nIncohInt","utctime"]
    nipp      = (1000/IPPms)/nChannels
    ippP10sec = nipp*10
    print(f"{ippP10sec} profiles in 10 seconds")
    ##############################################
    ########### PATH OUTPUT            ###########
    l        = startDate.split("/")
    datelist = datetime.date(int(l[0]),int(l[1]),int(l[2]))
    DOY      = datelist.timetuple().tm_yday
    year     = l[0]
    month    = l[1].zfill(2)
    day      = l[2].zfill(2)
    doy      = str(DOY).zfill(3)

    outPath1 = outPath+"/"+l[0]+doy
    outPath2 = path_hdf5_out+"/ISR"+l[0]+doy
    print(outPath1,outPath2)
    if os.path.exists(outPath1):
        print("outPath 1: ", outPath1)
    else :
        os.makedirs(outPath1)

    if os.path.exists(outPath2):
        print("outPath 2: ", outPath2)
    else :
        os.makedirs(outPath2)

    controllerObj = Project()
    controllerObj.setup(id = '33', name= 'isr_proc', description=desc)
    ##.......................................................................................
    ##.......................................................................................

    readUnitConfObj = controllerObj.addReadUnit(datatype='AMISRReader',
                                                path=inPath,
                                                startDate=startDate,#startDate,#'2016/07/12',
                                                endDate=endDate,#endDate,#'2016/07/13',
                                                startTime='07:00:00',
                                                endTime='17:59:59',
                                                walk=0,
                                                code = code,
                                                nCode = nCode,
                                                nBaud = nBaud,
                                                timezone='lt',
                                                nOsamp = nosamp,
                                                nChannels=10,
                                                margin_days=4,
                                                nFFT=NFFT,
                                                online=0)

