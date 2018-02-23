import os

def update_DAT(DAT,returnperiod,duration):
    f=open(DAT)
    lines=f.readlines()

    t = list(lines[13])
    rp = list(lines[16])

    pp = [' '] * 6
    pp[(6-len(list(str(duration)))):6] = list(str(duration))
    t[10:16] = pp
    t = ''.join(t)
    lines[13] = t

    lp = [' '] * 6
    lp[(6-len(list(str(returnperiod)))):6] = list(str(returnperiod))
    rp[10:16] = lp
    rp = ''.join(rp)
    lines[16] = rp

    f.close()

    w=open(DAT, 'w')
    for item in lines:
        w.write(item)
    w.close()
	
def run_ISIS(ief):
    os.system('C:\isis\bin\isisf32_nw.exe "'+ief+'"')
	
def export_ISIS_results(tcs,zzn):
    os.system('C:\isis\bin\Tabularcsv.exe -silent -tcs "'+tcs+'" "'+zzn+'"')
	
def update_ief(ief,DAT):
    f=open(ief)
    lines=f.readlines()
    lines[1] = "Datafile="+DAT+"\n"
    f.close()
    w=open(ief, 'w')
    for item in lines:
        w.write(item)
    w.close()

def rename_DAT(DAT,name):
    x = DAT.split("\\")
    zzn = DAT.split("\\")
    x[len(x)-1] = name+".DAT"
    zzn[len(zzn)-1] = name+".zzn"
    x = '\\'.join(x)
    zzn = '\\'.join(zzn)
    os.rename(DAT, x)
    return x,zzn

def retrieve_ISIS_results(DAT):
    csv = DAT.replace(".DAT",".csv")
    f = open('Dolwen_Master.csv')
    lines=f.readlines()
    x = lines[1]
    x = x.split(",")
    return float(x[1])
	
DAT = r"C:\Users\james.runnalls\Documents\Jupyter\ISISbatch\testing.DAT"
ief = r"C:\Users\james.runnalls\Documents\Jupyter\ISISbatch\Dolwen_Master.ief"
tcs = r"C:\Users\james.runnalls\Documents\Jupyter\ISISbatch\Dolwen_Master.tcs"
criticallevel = 160.2
durationlist = [1]

for returnperiod in range(10,20,10):
    for duration in durationlist:
        name = "rp"+str(returnperiod)+"_d"+str(duration)
        DAT,zzn = rename_DAT(DAT,name)
        update_ief(ief,DAT)
        update_DAT(DAT,returnperiod,duration)
        run_ISIS(ief)
        export_ISIS_results(tcs,zzn)
        level = retrieve_ISIS_results(DAT)
        if level > criticallevel:
            print("Storm exceeds critical level "+str(criticallevel)+" with return period 1 in "+str(returnperiod)+" years and a period of "+str(duration)+" hours.")
            break
    else:
        continue
    break  