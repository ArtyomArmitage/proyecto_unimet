import json
from typing import List, Dict
from reactivos import Reactivo
from recetas import Recetas
from experimentos import Experimento

#En este archivo coloco las funciones que sirven para leer y sobreescribir información de archivos .json


#Leer la info del archivo .json y retornar una lista con objetos de la clase Reactivos
def read_files(reactivos_f: str,experimentos_f: str,recetas_f: str):
  try:
    info_r: List[Dict[str, any]] = []
    info_ex: List[Dict[str, any]] = []
    info_rec: List[Dict[str, any]] = []
    with open(reactivos_f, 'rb') as file:
      info_r = json.load(file) #info almacena los datos del .json en una lista de diccionarios
    with open(experimentos_f, 'rb') as file:
      info_ex = json.load(file)
    with open(recetas_f, 'rb') as file:
      info_rec = json.load(file)
    reactivos: List[Reactivo] = [] #reactivos es una lista de instancias de la clase Reactivo
    recetas: List[Recetas] = [] #lista de instancias de la clase Recetas
    experimentos: List[Experimento] = [] #lista de instancias de la clase Experimento
    for reactivo in info_r:
      r = Reactivo.r_from_dic(reactivo) #Lee la lista "info" y convierte cada elemento en una instancia de la clase Reactivo
      reactivos.append(r) #guarda los objetos en la lista "reactivos"
    for experimento in info_ex:
      exp=Experimento.exp_from_dic(experimento)
      experimentos.append(exp)
    for receta in info_rec:
      rec=Recetas.rec_from_dic(receta)
      recetas.append(rec)
    return reactivos, experimentos, recetas
  except FileNotFoundError: #significa que si el archivo no se lee, se retorna una lista vacía
    return []

#Leer la lista de objetos y retornar una lista de diccionarios para almacenarla en el archivo .json
def write_file(file_name: str, objects, code: int):
  result = []
  if code==1:
    objects: List[Reactivo]
    for reactivo in objects:
      result.append(Reactivo.r_to_dict(reactivo)) #r_to_dict() convierte la información de una clase en un diccionario
  if code==2:
    objects: List[Experimento]
    for experimento in objects:
      result.append(Experimento.exp_to_dict(experimento)) #ya lo demás se sobreentiende
  if code==3:
    objects: List[Recetas]
    for receta in objects:
      result.append(Recetas.rec_to_dict(receta))
  with open(file_name, 'w') as file:
    json.dump(result, file)