#!/usr/bin/env python
import json
import os
import envConfig
import subprocess
import ManagementDB
import LogGest

# Los posibles estados de una maquina son
# not created, running, saved, poweroff

#-----------------------------------Chequeo de VM-----------------------------------------
    
def CheckVagrant(NameProyect):
    if os.path.isfile(envConfig.VAGRANTPROJECT+NameProyect+"/Vagrantfile") == True:
        return True
    else:
        return False

#Este metodo permite verificar si hay maquinas corriendo en un proyecto
def VmRunning(NameProyect):
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    myCmd = os.popen("vagrant status | grep running | wc -l").read()
    lineas = myCmd.split("\n")
    os.chdir(envConfig.HOME)
    return lineas[0]

def VmCreated(NameProyect):
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    myCmd = os.popen("vagrant status | grep 'running\|poweroff\|saved' | wc -l").read()
    lineas = myCmd.split("\n")
    os.chdir(envConfig.HOME)
    return lineas[0]

#-----------------------------------General vagrant-----------------------------------------

def VagrantVersion():
    myCmd = os.popen("vagrant version").read()
    return myCmd

def VagrantBoxList():
    myCmd = os.popen("vagrant box list").read()
    return myCmd

def VagrantBoxAdd(VM):
    command = subprocess.Popen(["vagrant","box","add",VM],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        lines = command.stdout.readline()
        if not lines:
            break
        print(lines.rstrip())

def VagrantBoxRemove(VM):
    myCmd = os.popen("vagrant box remove " + VM).read()
    return myCmd

def IDVM(NameProyect, VM):
    with open(envConfig.VAGRANTPROJECT+NameProyect+"/.vagrant/machines/"+VM+"/virtualbox/action_provision", 'r') as file_proyect:
        for linea in file_proyect.readlines():
            id = linea.split(":")
            return (id[1]) 

def InfoVM(NameProyect, VM):
    Datos_Json={}
    dic = {}
    Port_Forwar = {}
    Port = {}
    i = 1
    x = 0
    StatusGlobal = os.popen("vboxmanage showvminfo " + IDVM(NameProyect, VM) +
     " | egrep 'Name|Guest OS|Memory size|CPU exec cap|Number of CPUs|NIC|Rule' "+
     "| egrep -v 'disable|Storage Controller|machine mapping|Settings' | tr -s ' '").read()
    lineas = StatusGlobal.split("\n")
    lineas.pop(len(lineas)-1)
    for linea in lineas:
        if "NIC " in linea:
            if "NIC "+str(i)+": " in linea:
                v = linea.split("NIC "+str(i)+": ")[1]
                c = v.split(",")
                for dato in c:
                    if "Attachment" in dato:
                        llave_r = dato.split(":")[0]
                        valor_r = dato.split(":")[1]
                        dic["NIC "+str(i)]={"Attachment": valor_r.split(' ', 1)[1]}
                i += 1
            if "Rule" in linea:
                f = linea.split(" Rule("+str(x)+"): ")
                for dato_r in f[1].split(", "):
                    llave_w = dato_r.split(" = ")[0]
                    valor_w = dato_r.split(" = ")[1]
                    Port.update({llave_w: valor_w})
                Port_Forwar["Port forwarding "+str(x+1)]={}
                Port_Forwar["Port forwarding "+str(x+1)].update(Port)
                dic[f[0]].update(Port_Forwar)
                x += 1
        else:
            llave = linea.split(":")[0]
            valor = linea.split(":")[1]
            Datos_Json.setdefault(llave, valor.split(' ', 1)[1])
    Datos_Json.update({"Red":dic})
    return (Datos_Json)
 
def VagrantStatus(NameProyect):
    VMs = {}
    info_VM = {}
    info_VM = info_VM.fromkeys(['Name','Guest OS','Machine status',
    'Hipervisor','Memory size','Number of CPUs','CPU exec cap','Red'],'pending')
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    myCmd = os.popen("vagrant status | grep \) | tr -s ' '").read()
    lineas = myCmd.split("\n")
    lineas.pop(len(lineas)-1)
    for linea in lineas:
        data = linea.split()
        if 'not created' in linea:
            info_VM['Name']="pending"
            info_VM['Guest OS']="pending"
            info_VM['Memory size']="pending"
            info_VM['Number of CPUs']="pending"
            info_VM['CPU exec cap']="pending"
            info_VM['Red']="pending"
            info_VM['Machine status']="not created"
            info_VM["Hipervisor"]=data[3]
            VMs[data[0]]={}
            VMs[data[0]].update(info_VM)
        else:
            info_VM=(InfoVM(NameProyect, data[0]))
            info_VM["Machine status"]=data[1]
            info_VM["Hipervisor"]=data[2]
            VMs[data[0]]={}
            VMs[data[0]].update(info_VM)
    os.chdir(envConfig.HOME)
    return VMs

#-----------------------------------Gestion de VM-----------------------------------------

# Este metodo es instanciado por medio de un Hilo.
def VagrantUP(NameProyect, VM):
    LogGest.WarningMSG("Levantamiento de VM: "+VM)
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    command = subprocess.Popen(["vagrant","up",VM],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        lines = command.stdout.readline()
        if not lines:
            break
        print(lines.rstrip())        
    os.chdir(envConfig.HOME)
    ManagementDB.WriteElemt(NameProyect, VagrantStatus(NameProyect))    

def VagrantHalt(NameProyect, VM):
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    command = subprocess.Popen(["vagrant","halt",VM],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        lines = command.stdout.readline()
        if not lines:
            break
        print(lines.rstrip())   
    os.chdir(envConfig.HOME)
    ManagementDB.WriteElemt(NameProyect, VagrantStatus(NameProyect))

def VagrantDestroy(NameProyect, VMs):
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    if (VMs == ''):
        myCmd = os.popen("vagrant destroy -f").read()
    else:
        myCmd = os.popen("vagrant destroy " + VMs + " -f").read()
    ManagementDB.WriteElemt(NameProyect, VagrantStatus(NameProyect))
    os.chdir(envConfig.HOME)
    # Organizar retorno de respuestas
    return myCmd

#VagrantStatus("ubuntu")   