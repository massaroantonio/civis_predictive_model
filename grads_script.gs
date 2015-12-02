* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
*
function main(args)
say "Inizio script ..."
*
*
* argomenti (latitudine, longitudine, fileinput, fileoutput)
lat=subwrd(args,1) 
lon=subwrd(args,2) 
infile=subwrd(args,3)
outfile=subwrd(args,4)

*
'open ' infile
'q time'
dtr=subwrd(result,3)
say 'dtrun:'dtr
orarun=substr(dtr,1,2)
say 'ora:'orarun
annorun=substr(dtr,9,4)
meserun=substr(dtr,6,3)
meserun=month_number(meserun)
giornorun=substr(dtr,4,2)
*
*
* prendo le coordinate da argomenti script
'set lat 'lat' 'lat
'set lon 'lon' 'lon
*
*
fmt = '%-.1f'
*
*
'd 'tmp2m' - 273.15'
retval=subwrd(result,4)
retval=math_format(fmt,retval)
write(outfile,annorun%'-'%meserun%'-'%giornorun%' '%orarun%' T:'%retval)
*
'd DSWRFsfc'
retval=subwrd(result,4)
retval=math_format(fmt,retval)
write(outfile,annorun%'-'%meserun%'-'%giornorun%' '%orarun%' R:'%retval)

*
say "Fine script."
return

* ritorna il mese in formato numerico
function month_number(monstr)
mn=''
*say 'MON:'monstr
if monstr='JAN';  mn='01'; endif
if monstr='FEB';  mn='02'; endif
if monstr='MAR';  mn='03'; endif
if monstr='APR';  mn='04'; endif
if monstr='MAY';  mn='05'; endif
if monstr='JUN';  mn='06'; endif
if monstr='JUL';  mn='07'; endif
if monstr='AUG';  mn='08'; endif
if monstr='SEP';  mn='09'; endif
if monstr='OCT';  mn='10'; endif
if monstr='NOV';  mn='11'; endif
if monstr='DEC';  mn='12'; endif
*say 'MON:'mn
return(mn)


