from typing import Dict, List
from datetime import *

class Reactivo:
  #Acá defino las propiedades de todos los reactivos
  def __init__(self, id: int, name: str, description: str, cost: float, category: str, storage: float, unit: str, due_date: str, min: float, n_expired: int):
      self.id=id #esto no lo ingresa el usuario, lo define el programa
      self.name=name
      self.description=description
      self.cost=cost
      self.category=category
      self.storage=storage
      self.unit=unit
      self.due_date=due_date
      self.min=min
      self.conversions: List[Dict] = []
      self.expired=False
      self.errores: List[Dict] = []
      self.vencimientos: List = []
      self.n_vencimientos= n_expired
  

  #convierte diccionarios en instancias de la clase Reactivo  
  def r_from_dic(dict: Dict[str,any]):
    reactivo = Reactivo(dict.get("id"), dict.get("nombre"), dict.get("descripcion"), dict.get("costo"), 
                        dict.get("categoria"), dict.get("inventario_disponible"),dict.get("unidad_medida"),
                        dict.get("fecha_caducidad"),dict.get("minimo_sugerido"),dict.get("veces_expirado"))
    if reactivo.n_vencimientos==None:
      reactivo.n_vencimientos=0
    for con in dict.get("conversiones_posibles",[]):
      reactivo.conversions.append(con)
    for err in dict.get("errores",[]):
      reactivo.errores.append(err)
    reactivo.expired=Reactivo.is_expired(reactivo)
    for dates in dict.get("fechas_vencimiento",[]):
      reactivo.vencimientos.append(dates)
    Reactivo.check_fechas(reactivo)
    return reactivo
  

  def check_fechas(reactivo):
    if reactivo.vencimientos==[] or reactivo.due_date not in reactivo.vencimientos:
      reactivo.vencimientos.append(reactivo.due_date)
    if reactivo.expired==True:
      if reactivo.n_vencimientos<len(reactivo.vencimientos):
        reactivo.n_vencimientos+=1
  

  def is_expired(reactivo):
    present=date.today()
    if reactivo.due_date=="N/A":
      return False
    else:
      expiration=datetime.strptime(reactivo.due_date, "%Y-%m-%d").date()
      return expiration<present #Con esto se valida si el reactivo está vencido


  #convierte instancias de la clase Reactivo en diccionarios para el archivo .json
  def r_to_dict(self):
    result = {
      "id": self.id,
      "nombre": self.name,
      "descripcion": self.description,
      "costo": self.cost,
      "categoria": self.category,
      "inventario_disponible": self.storage,
      "unidad_medida": self.unit,
      "fecha_caducidad": self.due_date,
      "minimo_sugerido": self.min,
      "conversiones_posibles": [],
      "expirado": self.expired,
      "errores": [],
      "fechas_vencimiento": [],
      "veces_expirado": self.n_vencimientos
    }
    for con in self.conversions:
      result["conversiones_posibles"].append(con)
    for err in self.errores:
      result["errores"].append(err)
    for dates in self.vencimientos:
      result["fechas_vencimiento"].append(dates)
    return result