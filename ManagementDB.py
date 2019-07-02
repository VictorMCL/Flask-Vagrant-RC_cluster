#!/usr/bin/env python
import json
import os
import envConfig
from pprint import pprint

def Readjson():
    if os.path.isfile(envConfig.JSONFILE) == True:
        if checkDB():
            return("Base de datos vacia")
        else:
            with open(envConfig.JSONFILE) as data_file:    
                data = json.load(data_file)
                if not data:
                    return("Base de datos vacia")
                else:
                    return(data)
    else:
        return("No se encontro DB. Restaurar DB")

def WriteElemt(elementNEW, VM_status):
    data = {}
    if os.path.isfile(envConfig.JSONFILE) == True:
        if checkDB():
            data[elementNEW] = {}
            data[elementNEW] = {'Proyecto': elementNEW, 'Ruta': envConfig.VAGRANTPROJECT + elementNEW, 'VMs': VM_status}    
            with open(envConfig.JSONFILE, 'w') as file_dest:
                json.dump(data, file_dest, sort_keys=True, indent=4)
        else:
            with open(envConfig.JSONFILE, 'r') as file_orig:    
                data = json.load(file_orig)
                data[elementNEW] = {}
                data[elementNEW] = {'Proyecto': elementNEW, 'Ruta': envConfig.VAGRANTPROJECT + elementNEW, 'VMs': VM_status}    
            with open(envConfig.JSONFILE, 'w') as file_dest:
                json.dump(data, file_dest, sort_keys=True, indent=4)
    else:
        return "No se encontro DB. Restaurar DB"

def DeleteElemt(element):
    if os.path.isfile(envConfig.JSONFILE) == True:
        with open(envConfig.JSONFILE, 'r') as file_check:    
            data = json.load(file_check)
            if element in data:
                del data[element]
                with open(envConfig.JSONFILE, 'w') as file_dest:
                    json.dump(data, file_dest, sort_keys=True, indent=4)
                    print ('Se elimino el proyecto: ' + element) 
            else:
                print ('El proyecto: ' + element + ', no existe en la DB')
    else:
        print ("No se encontro DB. Restaurar DB")

def ModifyElemt(elementDEL, elementNEW, VM_status):
    if os.path.isfile(envConfig.JSONFILE) == True:
        with open(envConfig.JSONFILE, 'r') as file_check:    
            data = json.load(file_check)
            if elementDEL in data:
                del data[elementDEL]
                data[elementNEW] = {}
                data[elementNEW] = {'Proyecto': elementNEW, 'Ruta': envConfig.VAGRANTPROJECT + elementNEW, 'VMs': VM_status}    
                with open(envConfig.JSONFILE, 'w') as file_dest:
                    json.dump(data, file_dest, sort_keys=True, indent=4)
                if elementDEL == elementNEW:
                    print ('Se modifico el proyecto: ' + elementDEL) 
                else:
                    print ('Se modifico proyecto: ' + elementDEL + '\nPor proyecto: ' +elementNEW)
            else:
                print ('El proyecto: ' + elementDEL + ', no existe en la DB')
    else:
        print ("No se encontro DB. Restaurar DB")

def StatusElemt(element):
    if os.path.isfile(envConfig.JSONFILE) == True:
        if checkDB == True:
            return 'El proyecto: ' + element + ', no existe en la DB'
        else:
            with open(envConfig.JSONFILE, 'r') as file_check:    
                data = json.load(file_check)
                if element in data:
                    return data[element] 
                else:
                    return 'El proyecto: ' + element + ', no existe en la DB'
    else:
        return "No se encontro DB. Restaurar DB"

def ReadElemt(NameProyect):
    if checkDB():
            return False
    else:
        with open(envConfig.JSONFILE, 'r') as file_check:    
            data = json.load(file_check)
            if NameProyect in data:
                return True
            else:
                return False

def RestoreDB():
    if os.path.isfile(envConfig.JSONFILE) == True:
        print ('Ya existe una base de datos')
        return True
    else:
        json_file = open(envConfig.JSONFILE, "w")
        json_file.close()
        print ('Se restauro base de datos')
        # Crear log de que se crea base de datos

def checkDB():
    if os.stat(envConfig.JSONFILE).st_size == 0:
        return True
    else:
        return False
