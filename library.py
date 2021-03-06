import urllib2
import numpy as np
import os
from datetime import datetime,timedelta
from socket import error as SocketError
import httplib


#root='/home/amassaro/civis/CIVIS_repository/civis_predictive_model/civis_predictive_model/'
#some functions need absolute paths, insert the absolute path of the current folder here
root=os.getcwd()+'/'
#root='/home/amassaro/civis/civis_predictive_model/'
forwards=['03','06','09']+[str(i*3) for i in range(4,17)]
time_offset=1
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
    k=0
    f=open(file_name,'r')
    for l in f:
        if k:
            l=l.split(',')
            if int(l[0])==month and int(l[1])==(weekday+1)%7:
                consumption+=[float(x) for x in l[2:-1]]
                break
        k+=1
    return np.array(consumption)

def get_hydro_ceis(file_name,date):
    k=0
    f=open(file_name,'r')
    hydro=[]
    for l in f:
        if k:
            l=l.split(',')
            if datetime.strptime(l[1],'%d/%m/%Y') in [date, date+timedelta(1)]:
                hydro+=[float(x) for x in l[2:-1]]
        k+=1
    return np.array(hydro)

def get_hydro_cedis(file_name,date):
    k=0
    f=open(file_name,'r')
    hydro=[]
    for l in f:
        if k:
            l=l.split(',')
            if datetime.strptime(l[1],'%d/%m/%Y') in [date, date+timedelta(1)]:
                hydro+=[float(x) for x in l[2:-1]]
        k+=1
    return np.array(hydro)


#def get_hydro_cedis(file_name,date):
    #k=0
    #f=open(file_name,'r')
    #for l in f:
        #if k:
            #l=l.split(',')
            #hydro=[float(x) for x in l]
        #k+=1
    #return np.array(hydro+hydro)

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
def forecast_production(path_to_radiation_forecast,path_to_production_forecast,intercept,slope):
    #note: the meteo model returns radiation flux in J/m^2 per second: it has to be integrated on 3 hours, and divided by 1000 to get kW/m^2
    inFile=open(path_to_radiation_forecast,'r')
    outFile=open(path_to_production_forecast,'w')
    for l in inFile:
        l=l.split(' ')
        rad=float(l[-1].split(':')[-1])
        outFile.write(l[0]+' '+l[1]+' Production:'+str(intercept+slope*((rad*3600*3)/1000.))+'\n')
    return
def adjust_production(Production,offset):
    Production_h=[]
    for p in Production:
        Production_h+=[p/3. for k in range(3)]
    Production_h=Production_h[:offset]+Production_h[:-offset]
    return Production_h
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
    
    #url='http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t'+run_hour+'z.pgrb2.0p25.f0'+forward+'&all_lev=on&all_var=on&subregion=&leftlon=8&rightlon=12&toplat=48&bottomlat=43&dir=%2Fgfs.'+year+month+day+run_hour
    url='c'
    #grib = urllib2.urlopen(url)
    try:
        response=urllib2.urlopen(url)
    except SocketError, e:
        print 'Socket error'
        return 2
    except urllib2.URLError, e:
        print 'URL error'
        return 3
    except httplib.HTTPException, e:
        print 'HTTPException'
        return 4
    except Exception:
        print 'Exception'
        return 5

    filename=year+'_'+month+'_'+day+'_'+run_hour+'_'+forward
    output = open(download_directory+filename,'wb')
    output.write(response.read())
    output.close()
    create_ctl_file(path_to_perl_script,download_directory+filename)
    create_idx_file(download_directory+filename+'.ctl')
    return 1
#def get_signal(path_to_production_forecast,hydro_forecast,consumption_forecast,path_to_signal_file,time_offset):
#    inFile=open(path_to_production_forecast,'r')
#    outFile=open(path_to_signal_file,'w')
#    time=[]
#    Time=[]
#    production=[]
#    Production=[]
#    for l in inFile:
#        l=l.split('Production:')
#        Production.append(float(l[1]))
#    inFile.close()
    #print Production
    #time-shift of Production data and rescaling of initial and final time-window
#    Production=adjust_production(Production,time_offset)    
#    Production=np.array(Production)
#    Delta=Production+hydro_forecast-consumption_forecast
#    Delta3=[]
#    for i in range(16):
#        Delta3.append(sum(Delta[3*i:3*(i+1)]))
#    for i in range(len(Delta3)):
        # outFile.write(str((i+1)*3)+','+str(Delta3[i]>0)+'\n')
        # modified by DM to account for the requirements of the Web APIs
#        outTariff='Low' if (Delta3[i]>0) else 'High'
#        outFile.write(str((i+1)*3)+','+outTariff+'\n')
#    outFile.close()
#    return

def check_if_signal_is_trivial(v):
    output=[0,0]
    if sum(v[:8])==0 or sum(v[:8])==8:
        output[0]=1
    if sum(v[8:])==0 or sum(v[8:])==8:
        output[1]=1
    return output

def alternative_signal(Delta3,check):
    delta=np.array(Delta3)
    delta0=delta[:8]
    delta1=delta[8:]
    output0=delta0>0
    output1=delta1>0
    if check[0]:
        indexesTrue=np.argsort(-delta0)[:3]
        indexesFalse=np.argsort(-delta0)[3:]
        output0[indexesTrue]=True
        output0[indexesFalse]=False
    if check[1]:
        indexesTrue=np.argsort(-delta1)[:3]
        indexesFalse=np.argsort(-delta1)[3:]
        output1[indexesTrue]=True
        output1[indexesFalse]=False
    return np.concatenate((output0,output1))


def get_signal(path_to_production_forecast,hydro_forecast,consumption_forecast,path_to_signal_file,time_offset):
    inFile=open(path_to_production_forecast,'r')
    outFile=open(path_to_signal_file,'w')
    time=[]
    Time=[]
    production=[]
    Production=[]
    for l in inFile:
        l=l.split('Production:')
        Production.append(float(l[1]))
    inFile.close()
    #print Production
    #time-shift of Production data and rescaling of initial and final time-window
    Production=adjust_production(Production,time_offset)    
    Production=np.array(Production)
    Delta=Production+hydro_forecast-consumption_forecast
    Delta3=[]
    for i in range(16):
        Delta3.append(sum(Delta[3*i:3*(i+1)]))
    Delta3_signal=np.array(Delta3)>0
    check=check_if_signal_is_trivial(Delta3_signal)
    if sum(check):
        Delta3_signal=alternative_signal(Delta3,check)

    for i in range(len(Delta3_signal)):
        # modified by DM to account for the requirements of the Web APIs
        outTariff='Low' if Delta3_signal[i] else 'High'
        outFile.write(str((i+1)*3)+','+outTariff+'\n')
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
        hydro=get_hydro_cedis(hydro_storo,current_date)
    elif place=='San_Lorenzo':
        intercept=interceptSLorenzo
        slope=slopeSLorenzo
        lat=latSLorenzo
        lon=lonSLorenzo
        consumption_forecast=get_avg_consumption(consumption_forecast_sLorenzo,weekday,month)
        hydro=get_hydro_ceis(hydro_sLorenzo,current_date)
    current_dir=str(day)+'_'+str(month)+'_'+str(year)+'_'+run_hour+'_'+place
    os.system('rm -r '+'outputs/'+current_dir)
    os.system('mkdir '+'outputs/'+current_dir)
    os.system('mkdir '+'outputs/'+current_dir+'/gribs')
    
    download_directory=root+'outputs/'+current_dir+'/gribs/'
    rad_fc=root+'outputs/'+current_dir+'/radiazione_fc_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(run_hour)+'_'+place+'.txt'
    pv_fc=root+'outputs/'+current_dir+'/pv_fc_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(run_hour)+'_'+place+'.txt'
    signal_file=root+'outputs/'+current_dir+'/signal_'+str(day)+'_'+str(month)+'_'+str(year)+'_'+str(run_hour)+'_'+place+'.txt'
    #the directories entered into download_and_create_ctl_idx_files must be ABSOLUTE
    for forward in forwards:
         allfine=download_and_create_ctl_idx_files(run_hour,year,month,day,forward,download_directory,perl_script)
         if allfine in [2,3,4,5]:
            print 'error in downloading file'
            return allfine

    files=os.listdir(download_directory)
    files=[f for f in files if '.ctl' in f]
    files.sort()
    for f in files:
        ctl_file=download_directory+f
        #ctl_file and grads_script must be ABSOLUTE directories
        print_radiation_to_file(grads_script,lat,lon,ctl_file,rad_fc)
    forecast_production(rad_fc,pv_fc,intercept,slope)
    get_signal(pv_fc,hydro,consumption_forecast,signal_file,time_offset)
    return 1
# new function that updates for the current date
def updateToday(place):
    currentDate=datetime.today()
    #roundedHour = int(6*round(currentDate.hour/6))
    run_hour='00'
    #print(str(roundedHour))
    check=update(currentDate.year,currentDate.month,currentDate.day,run_hour,place)
    if check in [2,3,4,5]:
        return check
    return 1
# new function that updates for both pilot sites
def updateTodayBothPlaces():
    checkStoro=updateToday('Storo')
    if checkStoro in [2,3,4,5]:
        return checkStoro
    checkSanLorenzo=updateToday('San_Lorenzo')
    if checkSanLorenzo in [2,3,4,5]:
        return checkSanLorenzo
    return 1
#returns the nearest signal (nearest with respect to the current time)
#note: it does not take care of timezones. it has to be launched from a computer that is sync with the italian timeshift



# everyday at midnioght utc check is set to 0 and as soon as updatebothplaces succedes, it is turned to 1 and job does not updatebothplaces any more
# updatebothplaces runs between 3 am utc and 12 am utc
# siris is on UTC, therefore the check variable needs to be reset at  00 pm machine time

errors=['Socket error','URL error','HTTPException','Exception']

check_all_good=0
def job():
    global check_all_good
    now=datetime.now()
    if now.hour==0:
        check_all_good=0
        f=open('logfile.txt','a')
        f.write(str(now)+','+str(check_all_good)+',check_all_good set to 0\n')
        f.close()

    if check_all_good==0 and now.hour in [h for h in range(3,15)]:
        check_all_good=updateTodayBothPlaces()
        if check_all_good==1:
            f=open('logfile.txt','a')
            f.write(str(now)+','+str(check_all_good)+',updateTodayBothPlaces has ran succesfully\n')
            f.close()
        else:
            f=open('logfile.txt','a')
            f.write(str(now)+','+str(check_all_good)+',updateTodayBothPlaces has not ran succesfully,'+'error_code: '+errors[check_all_good-2]+' \n')
            f.close()
            check_all_good=0
    else:
        f=open('logfile.txt','a')
        f.write(str(now)+','+str(check_all_good)+',updateTodayBothPlaces has been skipped\n')
        f.close()

    return