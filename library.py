import urllib2
import numpy as np
import os

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
    assert run_hour in ['00','06','12','18'],'run_hour must be one of the following: '+str(['00','06','12','18'])
    assert forward in ['03','06','09','12','15','18','21','24'],'forward must be one of the following: '+str(['03','06','09','12','15','18','21','24'])
    url='http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t'+str(run_hour)+'z.pgrb2.0p25.f0'+str(forward)+'&all_lev=on&all_var=on&subregion=&leftlon=8&rightlon=12&toplat=48&bottomlat=43&dir=%2Fgfs.'+str(year)+str(month)+str(day)+str(run_hour)
    grib = urllib2.urlopen(url)
    filename=str(year)+'_'+str(month)+'_'+str(day)+'_'+str(run_hour)+'_'+str(forward)
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
        outFile.write(l[0]+' '+l[1]+' Production:'+str(intercept+slope*rad)+'\n')
    return

def get_signal(path_to_production_forecast,path_to_consuption_forecast,path_to_signal_file):
    inFile1=open(path_to_production_forecast,'r')
    inFile2=open(path_to_consuption_forecast,'r')
    outFile=open(path_to_signal_file,'w')
    time1=[]
    time2=[]
    Production=[]
    Consumption=[]
    for l in inFile1:
        l=l.split('Production:')
        time1.append(l[0])
        Production.append(float(l[1]))
    inFile1.close()
    for l in inFile2:
        l=l.split('Consumption:')
        time2.append(l[0])
        Consumption.append(float(l[1]))
    inFile2.close()    

    for i in range(len(Consumption)):
        outFile.write(time1[i]+' '+str((Production[i]-Consumption[i])>0)+'\n')
    outFile.close()
    return
        


