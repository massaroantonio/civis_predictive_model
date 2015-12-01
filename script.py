import urllib2
import numpy as np
import os
import library as lib

forwards=['03','06','09','12','15','18','21','24']
lat='46.2'
lon='10.1'
path_to_perl_script='/home/amassaro/civis/civis_data/previsioni/g2ctl.pl'
path_to_grads_script='/home/amassaro/civis/civis_data/previsioni/grads_script_short_long_wave.gs'
path_to_consumption_forecast='/home/amassaro/civis/civis_data/previsioni/consumption.txt'
intercept=10
slope=.33
def update(year,month,day,run_hour):
    current_dir=str(day)+'_'+str(month)+'_'+str(year)+'_'+run_hour
    os.system('mkdir '+current_dir)
    download_directory='/home/amassaro/civis/civis_data/previsioni/'+current_dir+'/'
    path_to_rad_fc='/home/amassaro/civis/civis_data/previsioni/radiazione_fc_'+str(day)+'_'+str(month)+'_'+str(year)+'.txt'
    path_to_elec_fc='/home/amassaro/civis/civis_data/previsioni/electricity_fc_'+str(day)+'_'+str(month)+'_'+str(year)+'.txt'
    path_to_signal_file='/home/amassaro/civis/civis_data/previsioni/signal_'+str(day)+'_'+str(month)+'_'+str(year)+'.txt'
    
    #for forward in forwards:
        #download_and_create_ctl_idx_files(run_hour,year,month,day,forward,download_directory,path_to_perl_script)

    files=os.listdir(current_dir+'/')
    files=[f for f in files if '.ctl' in f]
    files.sort()
    for f in files:
        path_to_ctl_file='/home/amassaro/civis/civis_data/previsioni/'+current_dir+'/'+f
        lib.print_radiation_to_file(path_to_grads_script,lat,lon,path_to_ctl_file,path_to_rad_fc)
    lib.forecast_production(path_to_rad_fc,path_to_elec_fc,intercept,slope)
    lib.get_signal(path_to_elec_fc,path_to_consumption_forecast,path_to_signal_file)
    return