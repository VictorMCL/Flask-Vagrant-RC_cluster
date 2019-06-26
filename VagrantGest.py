#!/usr/bin/env python
import json
import os
import envConfig
import subprocess
import ManagementDB
import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.FileHandler(envConfig.FILELOG)
f_handler = logging.FileHandler(envConfig.FILELOG)

c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

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

#-----------------------------------Gestion de VM-----------------------------------------

# Este metodo es instanciado por medio de un Hilo.
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
    ManagementDB.WriteElemt(NameProyect, VagrantStatus(NameProyect))
    os.chdir(envConfig.HOME)
    return myCmd

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

