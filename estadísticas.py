from collections import Counter
from reactivos import Reactivo
from experimentos import Experimento
from recetas import Recetas
from gestión_experimentos import GestionExperimentos
from typing import List

class Estadísticas():
    def investigadores(experimentos: List[Experimento]):
        personas=[]
        for experimento in experimentos:
            personas.append(experimento.experimentadores)
        result=Counter(x for xs in personas for x in set(xs))
        for key,value in result.most_common(3):
            print(f"    {key}: {value}.")

    def experimentos(experimentos: List[Experimento], recetas: List[Recetas]):
        recipes=[]
        for experimento in experimentos:
            recipes.append(experimento.receta_id)
        result=Counter(recipes)
        highest_recipe_num=max(result,key=result.get)
        least_recipe_num=min(result,key=result.get)
        highest=GestionExperimentos.search_receta(highest_recipe_num,recetas)
        least=GestionExperimentos.search_receta(least_recipe_num,recetas)
        print(f"""    Experimento más hecho: {highest.name}
    Nro. de veces realizado: {result[highest_recipe_num]}
              
    Experimento menos hecho: {least.name}
    Nro. de veces realizado: {result[least_recipe_num]}""")

    def reactivos_us(reactivos: List[Reactivo], experimentos: List[Experimento], recetas: List[Recetas]):
        r_used=[]
        rec_used_num=[]
        rec_used=[]
        for experimento in experimentos:
            rec_used_num.append(experimento.receta_id)
        rec_used_num=Counter(rec_used_num)
        for key in rec_used_num.keys():
            for i in range(0,rec_used_num[key]):
                recipe=next((item for item in recetas if item.id==key), None)
                rec_used.append(recipe)
        for rec in rec_used:
            for i in rec.r_used:
                r_used.append(i["reactivo_id"])
        result=Counter(r_used)
        for key,value in result.most_common(5):
            reactivo=GestionExperimentos.obtain_reactivo(key,reactivos)
            print(f"    {reactivo.name}. Nro. de veces usado: {value}")

    def experimentos_not_done(recetas: List[Recetas]):
        experimentos=[]
        for receta in recetas:
            if receta.not_done!=0:
                experimentos.append(receta)
        experimentos.sort(key=lambda x: x.not_done, reverse=True)
        if experimentos==[]:
            print("      No existe un experimento que no se haya realizado por falta de reactivos.")
        else:
            for experimento in experimentos:
                print(f"    {experimento.name}. Nro de veces no realizado: {experimento.not_done}")
        print("")
    
    def reac_desperdicio(reactivos: List[Reactivo]):
        check=[]
        percentages=[]
        for reactivo in reactivos:
            if reactivo.errores!=[]:
                check.append(reactivo)
            else:
                print("      Ningún reactivo se ha desperdiciado")
                return
        for reactivo in check:
            for i in reactivo.errores:
                percentage=((sum(i["cantidades"])/len(i["cantidades"]))/i["teórico"])*100
                percentages.append(percentage)
        data=list(zip(check,percentages))
        data.sort(key=lambda x:x[1], reverse=True)
        for key,value in data[0:2]:
            print(f"    {key.name}. Porcentaje de desperdicio: {value:.2f}%")

    def reac_vencidos(reactivos:List[Reactivo]):
        check=[]
        number=[]
        for reactivo in reactivos:
            if reactivo.n_vencimientos!=0:
                check.append(reactivo)
                number.append(reactivo.n_vencimientos)
        data=list(zip(check,number))
        data.sort(key=lambda x:x[1], reverse=True)
        for key,value in data:
            print(f"    {key.name}. Nro de veces que se ha vencido: {value}")
