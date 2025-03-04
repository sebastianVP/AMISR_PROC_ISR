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
sys.path.insert(0,path)
##############################################
path          = "/mnt/data_amisr"
outPath       = "/mnt/DATA/AMISR14/2025/ISR/"
path_hdf5_out = "/mnt/DATA/data2Fabiano/POWER_H5_AMISR/2025"
#############################################
##### PARAMETROS DE DIA #####################
dty  = datetime.date.today()
str1 = dty+datetime.timedelta(days=1) # un dia despues
str2 = dty-datetime.timedelta(days=4) # un dia antes
today     = dty.strftime("%Y/%m/%d")
tomorrow  = str1.strftime("%Y/%m/%d")
yesterday = str2.strftime("%Y/%m/%d")
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
##########################################
##########################################
print("today",today)
print("tomorrow",tomorrow)
print("yesterday",yesterday)
##############################################
########## PARAMETROS DE EXPERIMENTO ########
nChannels = 2
factors =[1.06, 1.06]
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

def schain(channel,Outdata,factor=1):

    desc= "AMISR ISR 2 Beam Experiment"
    if os.path.exists(Outdata):
       print("Outdata {}:".format(channel),Outdata)
    else:
       os.mkdir(Outdata)

    controllerObj = Project()
    controllerObj.setup(id = '33', name= 'isr_proc_offline', description=desc)
    ##.......................................................................................
    ##.......................................................................................

    readUnitConfObj = controllerObj.addReadUnit(datatype='AMISRReader',
                                                path=path,
                                                startDate=startDate,#startDate,#'2016/07/12',
                                                endDate=endDate,#endDate,#'2016/07/13',
                                                startTime='07:00:00',
                                                endTime='18:00:00',
                                                walk=0,
                                                timezone='lt',
                                                nOsamp = 1,
                                                nChannels=nChannels,
                                                margin_days=0,
                                                nFFT=nFFT,
                                                online=0)
    proc_volts = controllerObj.addProcUnit(datatype='VoltageProc', inputId=readUnitConfObj.getId())
    #
    opObj03 = proc_volts.addOperation(name='selectChannels', optype='other')
    opObj03.addParameter(name='channelList', value=[channel], format='list')
    opObj02 = proc_volts.addOperation(name='SSheightProfiles2', optype='other')
    opObj02.addParameter(name='step', value=1, format='int')
    opObj02.addParameter(name='nsamples', value=60, format='int')

    proc_spc = controllerObj.addProcUnit(datatype='SpectraProc', inputId=proc_volts.getId())
    proc_spc.addParameter(name='nFFTPoints', value=60, format='int')
    #proc_spc.addParameter(name='zeroPad', value=True)

    opObj13 = proc_spc.addOperation(name='IntegrationFaradaySpectra', optype='other')
    opObj13.addParameter(name='avg', value='1.0', format='int') #0.95 a 10 o 1 min
    opObj13.addParameter(name='minHei', value='100', format='int')
    opObj13.addParameter(name='maxHei', value='950', format='int')
    opObj13.addParameter(name='timeInterval', value=60, format='int')
    #opObj13.addParameter(name='n', value=1000, format='int')
    # # #
    opObj13 = proc_spc.addOperation(name='IncohInt', optype='other')
    opObj13.addParameter(name='n', value='5', format='int')
    # opObj13.addParameter(name='timeInterval', value='20', format='int')
    
    opObj03 = proc_spc.addOperation(name='getNoiseB', optype='other')
    opObj03.addParameter(name='offset', value='0.225', format='float')
    opObj03.addParameter(name='minHei', value='200', format='int')
    opObj03.addParameter(name='maxHei', value='350', format='int')
    opObj03.addParameter(name='minFreq', value='-40000', format='int')
    opObj03.addParameter(name='maxFreq', value='40000', format='int')

    rti_plot = proc_spc.addOperation(name='NoiselessRTIPlot', optype='external')
    rti_plot.addParameter(name='wintitle', value='RTI AMISR', format='str')
    rti_plot.addParameter(name='showprofile', value='1', format='int')
    rti_plot.addParameter(name='zmin', value=-0.01, format='int')
    rti_plot.addParameter(name='zmax', value=0.3, format='int')
    rti_plot.addParameter(name='xmin', value=xmin, format='int')
    rti_plot.addParameter(name='xmax', value=xmax, format='int')
    rti_plot.addParameter(name='localtime', value=1,format='int')
    rti_plot.addParameter(name='save', value=Outdata, format='str')
    rti_plot.addParameter(name='t_units', value='h', format='str')


    controllerObj.start()
    controllerObj.join()
    time.sleep(60)


if __name__=="__main__":
   fpathOut = outPath+"d"+l[0]+doy
   outPaths = [outPath+l[0]+doy +"CH{}".format(ch) for ch in range(nChannels)]
   dataList = ['data_spc','nIncohInt','utctime']
   ##########################################################
   ##########################################################
   pool=[]
   for ch in range(nChannels):
      print(f"[WORKING ON----------------------------------------------{ch}]")
      p= Process(target=schain,args=(ch,outPaths[ch], factors[ch]))
      pool.append(p)
      p.start()
   wait(p.sentinel for p in pool)
   time.sleep(45)
   ##########################################################
