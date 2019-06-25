#!/usr/bin/env python
import json
import os
import envConfig
import subprocess
import ManagementDB

# Los posibles estados de una maquina son
# not created, running, saved, poweroff
def VagrantStatus(NameProyect):
    VMs = {}
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    myCmd = os.popen("vagrant status | grep \) | tr -s ' '").read()
    lineas = myCmd.split("\n")
    lineas.pop(len(lineas)-1)
    for linea in lineas:
        data = linea.split()
        if 'not created' in linea:
            VM = {data[0]:{"Status" : "not created", "Hipervisor" : data[3]}}
            VMs.update(VM) 
        else:
            VM = {data[0]:{"Status" : data[1], "Hipervisor" : data[2]}}
            VMs.update(VM)
    os.chdir(envConfig.HOME)
    return VMs

def VagrantUP(NameProyect, VM):
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    command = subprocess.Popen(["vagrant","up",VM],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        lines = command.stdout.readline()
        if not lines:
            break
        print(lines.rstrip())
    ManagementDB.WriteElemt(NameProyect, VagrantStatus(NameProyect))
    os.chdir(envConfig.HOME)

def VagrantHalt(NameProyect, VMs):
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    myCmd = os.popen("vagrant halt " + VMs).read()
    os.chdir(envConfig.HOME)
    return myCmd

def VagrantDestroy(NameProyect, VMs):
    os.chdir(envConfig.VAGRANTPROJECT+NameProyect)
    if (VMs == ''):
        myCmd = os.popen("vagrant destroy -f").read()
    else:
        myCmd = os.popen("vagrant destroy " + VMs + " -f").read()
    os.chdir(envConfig.HOME)
    # Organizar retorno de respuestas
    return myCmd
    
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


#VagrantDestroy('ubuntu', '')
#CheckVagrant("centos")
#ManagementDB.WriteElemt('ubuntu', VagrantStatus('ubuntu'))
#VmRunning('default')
#VmNotCreates('default')
#VagrantUP('default', 'node-1')