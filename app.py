#!/usr/bin/env python
import os
import threading
import envConfig
import ManagementDB
import VagrantGest
from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
from shutil import rmtree

# instancia del objeto Flask
app = Flask(__name__)

#curl -F 'file=@/home/cherno/Vagrantfile' http://localhost:8000/CrearProyecto
@app.route('/CrearProyecto', methods=['POST'])
@app.route('/CrearProyecto/<NameProyect>', methods=['POST'])
def upProyect(NameProyect='default'):
    path = envConfig.VAGRANTPROJECT + NameProyect
    if request.method == 'POST':
        if ManagementDB.ReadElemt(NameProyect) == True:
            #susceptible a mejoras
            return jsonify('Existe el proyeto: ' + NameProyect + '\n')
        else:
            #1) Creacion de folder
            os.mkdir(path)
            #2) Almacenaciento de Vagrantfile
            f = request.files['file']
            filename = secure_filename(f.filename)
            f.save(os.path.join(path, filename))
            #3) Registro en DB json
            # - VagrantGest.VagrantStatus(NameProyect) => devuelve el estado de VM en forma de Dicc.
            ManagementDB.WriteElemt(NameProyect, VagrantGest.VagrantStatus(NameProyect))
            return jsonify('Se creo proyecto: ' + NameProyect + '\n')

#curl http://localhost:8000/BorrarProyecto
@app.route('/BorrarProyecto')
@app.route('/BorrarProyecto/<NameProyect>')
def deleteProyect(NameProyect='default'):
    path = envConfig.VAGRANTPROJECT + NameProyect
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            if VagrantGest.VmCreated(NameProyect)!='0':
                VagrantGest.VagrantDestroyProyect(NameProyect)
                rmtree(path)
                ManagementDB.DeleteElemt(NameProyect)
            else:
                rmtree(path)
                ManagementDB.DeleteElemt(NameProyect)
            return jsonify('El proyecto: ' + NameProyect + ' se elimino de DB\n')
        else:
            return jsonify('Existe en DB y pero no hay Vagrantfile\n')
    else:
        return jsonify('No existe en DB\n')

#curl http://localhost:8000/StatusProyect
@app.route('/StatusProyect')
@app.route('/StatusProyect/<NameProyect>')
def statusProyect(NameProyect='default'):
    return  jsonify(ManagementDB.StatusElemt(NameProyect))

#curl http://localhost:8000/LevantarVM
@app.route('/LevantarVM')
@app.route('/LevantarVM/<NameProyect>')
@app.route('/LevantarVM/<NameProyect>/<VMs>')
def levantarVM(NameProyect='default', VMs=''):
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            threadUP = threading.Thread(target=VagrantGest.VagrantUP, args=(NameProyect, VMs))
            threadUP.start()
            return jsonify('Levantando maquinas virtuales...\n')
        else:
            return jsonify('Existe en DB y pero no hay Vagrantfile\n')
    else:
        return jsonify('No existe en DB\n')

#curl http://localhost:8000/ApagarVM
@app.route('/ApagarVM')
@app.route('/ApagarVM/<NameProyect>')
@app.route('/ApagarVM/<NameProyect>/<VMs>')
def ApagarVM(NameProyect='default', VMs=''):
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            ApagarVM = threading.Thread(target=VagrantGest.VagrantHalt, args=(NameProyect, VMs))
            ApagarVM.start()
            return jsonify('Apagando maquinas virtuales...\n')
        else:
            return jsonify('Existe en DB y pero no hay Vagrantfile\n')
    else:
        return jsonify('No existe en DB\n')

#curl http://localhost:8000/BorrarVM
@app.route('/BorrarVM')
@app.route('/BorrarVM/<NameProyect>')
@app.route('/BorrarVM/<NameProyect>/<VMs>')
def deleteVM(NameProyect='default', VMs=''):
    if ManagementDB.ReadElemt(NameProyect) == True:
        if VagrantGest.CheckVagrant(NameProyect):
            if VagrantGest.VmCreated(NameProyect)!='0':
            #1) Se destruyen maquinas
                DestroyVM = threading.Thread(target=VagrantGest.VagrantDestroy, args=(NameProyect, VMs))
                DestroyVM.start()
            #3) Respuesta
                return jsonify('Borrando maquinas virtualies...')
            else:
            #3) Respuesta
                return jsonify('El proyecto: ' + NameProyect + ' no tiene VM creadas\n')
        else:
            return jsonify('Existe en DB y pero no hay Vagrantfile\n')
    else:
        return jsonify('No existe en DB\n')

#curl http://localhost:8000/StatusDB
@app.route('/StatusDB')
def statuDB():
    return  jsonify(ManagementDB.Readjson())

#curl http://localhost:8000/VagrantVersion
@app.route('/VagrantVersion')
def VagrantVersion():
    return  jsonify(VagrantGest.VagrantVersion())

#curl http://localhost:8000/VagrantBoxList
@app.route('/VagrantBoxList')
def VagrantBoxList():
    return  jsonify(VagrantGest.VagrantBoxList())

#curl http://localhost:8000/VagrantBoxAdd/ubuntu/trusty64
@app.route('/VagrantBoxAdd/<path:Box>')
def VagrantBoxAdd(Box=''):
    threadBoxAdd = threading.Thread(target=VagrantGest.VagrantBoxAdd, args=(Box, ))
    threadBoxAdd.start()
    return  jsonify("Se lanzo un hilo ejecutando la tarea\n")

#curl http://localhost:8000/VagrantBoxRemove/ubuntu/trusty64
@app.route('/VagrantBoxRemove/<path:Box>')
def VagrantBoxRemove(Box=''):
    return  jsonify(VagrantGest.VagrantBoxRemove(Box))

#curl http://localhost:8000/ObtenerRAM
@app.route('/ObtenerRAM')
def ObtenerRAM():
    return jsonify(VagrantGest.GetMemRAM())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",  port=8000)