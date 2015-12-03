import urllib2
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

root=''#some funciotns need absolute paths, insert the absolute path of the current folder here
forwards=['03','06','09']+[str(i*3) for i in range(4,17)]
latStoro='45.8491806'
lonStoro='10.5740091'
latSLorenzo='46.0760384'
lonSLorenzo='10.9018553'

perl_script=root+'g2ctl.pl'
grads_script=root+'grads_script.gs'
consumption_forecast_storo='data/cedis_ceis/cedis/cedis_avg_consumption.csv'
consumption_forecast_sLorenzo='data/cedis_ceis/ceis/ceis_avg_consumption.csv'
hydro_storo='data/cedis_ceis/cedis/cedis_hydro.csv'
hydro_sLorenzo='data/cedis_ceis/ceis/ceis_hydro.csv'

interceptStoro=12.8284854363
slopeStoro=0.174498858848 
 
interceptSLorenzo=21.9910225252
slopeSLorenzo=0.238609245923 


def get_avg_consumption(file_name,weekday,month):
    k=0
    f=open(file_name,'r')
    for l in f:
        if k:
            l=l.split(',')
            if int(l[0])==month and int(l[1])==weekday:
                consumption=[float(x) for x in l[2:-1]]
                break
        k+=1
    return np.array(consumption)

def get_hydro(file_name):
    k=0
    f=open(file_name,'r')
    for l in f:
        if k:
            l=l.split(',')[:-1]
            hydro=np.array([float(x) for x in l])
        k+=1
    return hydro

def create_ctl_file(path_to_perl_script,path_to_grib_file):
    command='perl '+path_to_perl_script+' '+path_to_grib_file+'>'+path_to_grib_file+'.ctl' 
    os.system(command)
    return

def create_idx_file(path_to_ctl_file):
    command='gribmap -i '+path_to_ctl_file
    os.system(command)
    return

def print_radiation_to_file(path_to_grads_script,lat,lon,path_to_ctl_file,path_to_out_file):
    command="grads -blcx '"+path_to_grads_script+' '+str(lat)+' '+str(lon)+' '+path_to_ctl_file+' '+path_to_out_file+"'"
    os.system(command)

def download_and_create_ctl_idx_files(run_hour,year,month,day,forward,download_directory,path_to_perl_script):
    month=str(month)
    day=str(day)
    year=str(year)
    if len(month)<2:
        month='0'+month
    if len(day)<2:
        day='0'+day
    assert run_hour in ['00','06','12','18'],'run_hour must be one of the following: '+str(['00','06','12','18'])
    assert forward in forwards,'forward must be one of the following: '+str(forwards)
    
    url='http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t'+run_hour+'z.pgrb2.0p25.f0'+forward+'&all_lev=on&all_var=on&subregion=&leftlon=8&rightlon=12&toplat=48&bottomlat=43&dir=%2Fgfs.'+year+month+day+run_hour
    grib = urllib2.urlopen(url)
    filename=year+'_'+month+'_'+day+'_'+run_hour+'_'+forward
    output = open(download_directory+filename,'wb')
    output.write(grib.read())
    output.close()
    create_ctl_file(path_to_perl_script,download_directory+filename)
    create_idx_file(download_directory+filename+'.ctl')
    return

 def forecast_production(path_to_radiation_forecast,path_to_production_forecast,intercept,slope):
    inFile=open(path_to_radiation_forecast,'r')
    outFile=open(path_to_production_forecast,'w')
    for l in inFile:
        l=l.split(' ')
        rad=float(l[-1].split(':')[-1])
        outFile.write(l[0]+' '+l[1]+' Production:'+str(intercept+slope*(rad*3600*3))+'\n')
    return

def get_signal(path_to_production_forecast,path_to_consuption_forecast,path_to_signal_file):
    inFile1=open(path_to_production_forecast,'r')
    inFile2=open(path_to_consuption_forecast,'r')
    outFile=open(path_to_signal_file,'w')
    time=[]
    Production=[]
    Consumption=[]
    for l in inFile1:
        l=l.split('Production:')
        time.append(l[0])
        Production.append(float(l[1]))
    inFile1.close()
    for l in inFile2:
        l=l.split('Consumption:')
        Consumption.append(float(l[1]))

    Consumption+=Consumption
    inFile2.close()    
    assert len(Consumption)==len(Production), 'Production and Consumption vector have different lengths'
    for i in range(len(Consumption)):
        outFile.write(time[i]+' '+str((Production[i]-Consumption[i])>0)+'\n')
    outFile.close()
    return

def update(year,month,day,run_hour,place):
    assert len(str(year))==4, 'year format must be yyyy'
    assert month in [1,2,3,4,5,6,7,8,9,10,11,12], 'month must be an int between 1 and 12'
    assert run_hour in ['00','06','12','18'], 'run hour must be in '+str(['00','06','12','18'])
    current_date=datetime.strptime(str(day)+' '+str(month)+' '+str(year),'%d %m %Y')
    weekday=current_date.weekday()
    if place=='Storo':
        intercept=interceptStoro
        slope=slopeStoro
        lat=latStoro
        lon=lonStoro
        consumption_forecast=get_avg_consumption(consumption_forecast_storo,weekday,month)
        hydro=get_hydro(hydro_storo)
    elif place=='San_Lorenzo':
        intercept=interceptSLorenzo
        slope=slopeSLorenzo
        lat=latSLorenzo
        lon=lonSLorenzo
        consumption_forecast=get_avg_consumption(consumption_forecast_sLorenzo,weekday,month)
        hydro=get_hydro(hydro_sLorenzo)
    current_dir=str(day)+'_'+str(month)+'_'+str(year)+'_'+run_hour+'_'+place
    os.system('mkdir '+'outputs/'+current_dir)
    os.system('mkdir '+'outputs/'+current_dir+'/gribs')
    
    download_directory=root+'outputs/'+current_dir+'/gribs/'
    rad_fc=root+'outputs/'+current_dir+'/radiazione_fc_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(run_hour)+'_'+place+'.txt'
    elec_fc=root+'outputs/'+current_dir+'/electricity_fc_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(run_hour)+'_'+place+'.txt'
    signal_file=root+'outputs/'+current_dir+'/signal_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(run_hour)+'_'+place+'.txt'
    #the directories entered into download_and_create_ctl_idx_files must be ABSOLUTE
    for forward in forwards:
        download_and_create_ctl_idx_files(run_hour,year,month,day,forward,download_directory,perl_script)

    files=os.listdir(download_directory)
    files=[f for f in files if '.ctl' in f]
    files.sort()
    for f in files:
        ctl_file=download_directory+f
        #ctl_file and grads_script must be ABSOLUTE directories
        print_radiation_to_file(grads_script,lat,lon,ctl_file,rad_fc)
    forecast_production(rad_fc,elec_fc,intercept,slope)
    #get_signal(elec_fc,consumption_forecast,signal_file)
    return
