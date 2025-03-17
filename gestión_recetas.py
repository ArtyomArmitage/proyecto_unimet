from recetas import *
from gestión_experimentos import GestionExperimentos
from experimentos import Experimento
from typing import List

class GestionRecetas:
    def search(recetas:List[Recetas]):
        num=int(input("""Buscar por...\n
        1. Id
        2. Nombre
        \n"""))
        results=[]
        value=input("Ingrese el valor de búsqueda: ")
        for receta in recetas:
            if num==1:
                if int(value)==receta.id:
                    return [receta]
            if num==2:
                if str(value) in receta.name:
                    results.append(receta)
        return results
    
    
    def display(receta: Recetas):
        print(f"""\nInformación de la receta de {receta.name}:
        Id: {receta.id}
        Nombre: {receta.name}
        Objetivo: {receta.objective}
        Id de reactivos usados: {[value.get("reactivo_id") for value in receta.r_used]}
        Procedimiento: 
            {"\n            ".join(receta.procedimiento)}
        Valores a medir:""")
        for value in receta.v_medir:
            print(f"""          Nombre: {value.get("nombre")}
            Fórmula: {value.get("formula")}
            Mínimo: {value.get("minimo")}
            Máximo: {value.get("maximo")}""")
        print("       -----------------------------------------------")


    def search_experimento(num: int, experimentos: List[Experimento]):
        for ex in experimentos:
            if ex.id==num:
                return ex


    def evaluate_result(num: int, experimentos: List[Experimento], recetas: List[Recetas]):
        experimento: Experimento=GestionRecetas.search_experimento(num,experimentos)
        if experimento==None:
            print("\nNo existe un experimento con la id ingresada.\n")
        else: 
            receta=GestionExperimentos.search_receta(experimento.receta_id,recetas)
            print(f"""\nId de la receta: {receta.id}.\nObjetivo del experimento: {receta.objective}.\nResultado del experimento: {experimento.resultado}\nValores a medir:\n""")
            for value in receta.v_medir:
                min=value.get("minimo")
                max=value.get("maximo")
                print(f"""  Nombre: {value.get("nombre")}
        Fórmula: {value.get("formula")}""")
                resultado_experimental=int(input("\nIngrese el valor que usted obtuvo: "))
                if min<=resultado_experimental<=max:
                    print("\nSu resultado se encuentra dentro de los parámetros aceptables\n")
                else:
                    print("\nSu resultado está fuera de los parámetros aceptables\n")
        
