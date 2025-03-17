from typing import Dict, List

class Recetas:
  def __init__(self, id: int, name: str, objective: str, procedure: List, not_done):
      self.id=id 
      self.name=name
      self.objective=objective
      self.r_used: List[Dict] = []
      self.procedimiento=procedure
      self.v_medir: List[Dict] = []
      self.not_done: int=not_done

    
  #convierte diccionarios en instancias de la clase Recetas  
  def rec_from_dic(dict: Dict[str,any]):
    receta = Recetas(dict.get("id"), dict.get("nombre"), dict.get("objetivo"), dict.get("procedimiento"), dict.get("veces_no_realizado"))
    for r in dict.get("reactivos_utilizados",[]):
      receta.r_used.append(r)
    for v in dict.get("valores_a_medir",[]):
      receta.v_medir.append(v)
    if receta.not_done==None:
      receta.not_done=0
    return receta

  #convierte instancias de la clase Recetas en diccionarios para el archivo .json
  def rec_to_dict(self):
    result = {
      "id": self.id,
      "nombre": self.name,
      "objetivo": self.objective,
      "reactivos_utilizados": [],
      "procedimiento": self.procedimiento,
      "valores_a_medir": [],
      "veces_no_realizado": self.not_done
    }
    for r in self.r_used:
      result["reactivos_utilizados"].append(r)
    for v in self.v_medir:
      result["valores_a_medir"].append(v)
    return result