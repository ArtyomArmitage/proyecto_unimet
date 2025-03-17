from typing import Dict, List

class Experimento:
  def __init__(self, id: int, receta_id: int, personas_responsables: List, fecha: str, costo_asociado: float, resultado: str):
      self.id=id 
      self.receta_id=receta_id
      self.experimentadores=personas_responsables
      self.fecha=fecha
      self.costo=costo_asociado
      self.resultado=resultado
    
  #convierte diccionarios en instancias de la clase Recetas  
  def exp_from_dic(dict: Dict[str,any]):
    experimento = Experimento(dict.get("id"), dict.get("receta_id"), dict.get("personas_responsables"), dict.get("fecha"), dict.get("costo_asociado"), dict.get("resultado"))
    return experimento

  #convierte instancias de la clase Experimento en diccionarios para el archivo .json
  def exp_to_dict(self):
    result = {
      "id": self.id,
      "receta_id": self.receta_id,
      "personas_responsables": self.experimentadores,
      "fecha": self.fecha,
      "costo_asociado": self.costo,
      "resultado": self.resultado,
    }
    return result