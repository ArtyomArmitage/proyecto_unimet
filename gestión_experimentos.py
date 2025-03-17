from experimentos import *
from recetas import *
from reactivos import *
from datetime import *
import random

class GestionExperimentos():
    def new_exp(id_exp,recetas: List[Recetas], reactivos: List[Reactivo]):
        num=int(input("Ingrese el id de la receta que va a utilizar: "))
        receta=GestionExperimentos.search_receta(num,recetas)
        if receta==None:
            print("No existe una receta con el id ingresado\n")
        else:
            print(f"Se creará un experimento en base a la receta de {receta.name}:")
            result=GestionExperimentos.validate_all(id_exp,num,receta,reactivos)
            return result


    def validate_all(id_exp,id_receta:int, receta: Recetas, reactivos: List[Reactivo]):
        cost=0
        personas=[]
        usado=[]
        reactivos_experimento=[]
        error_reactivos=[]
        for i in receta.r_used:
            reactivo=GestionExperimentos.obtain_reactivo(i["reactivo_id"],reactivos)
            print(f"\n#Validación del reactivo {reactivo.name}#\n")
            if reactivo.expired==True:
                print(f"El experimento no se puede realizar porque el reactivo {reactivo.name} está vencido")
                return None
            elif reactivo.expired==False: #una vez verifico que el reactivo no está vencido:
                print(f"[\u2713] El reactivo {reactivo.name} no está vencido")
                if reactivo.unit!=i["unidad_medida"]: #si la unidad de la receta no es la del reactivo
                    GestionExperimentos.change_units(reactivo,i) #modifico la unidad de la receta

                error=random.uniform(0.001,0.225)*i["cantidad_necesaria"]
                used=i["cantidad_necesaria"]+error
                print(f"\nCantidad necesaria: {used}{i["unidad_medida"]}\nCantidad disponible: {reactivo.storage}{reactivo.unit}")
                if used>reactivo.storage:
                    print(f"El experimento no se puede realizar porque no hay suficiente {reactivo.name}")
                    receta.not_done+=1
                    return None
                else: #si hay suficiente reactivo para realizar el experimento
                    print(f"\n[\u2713] Hay suficiente {reactivo.name} para realizar el experimento\n")
                    error_reactivos.append(error)
                    reactivos_experimento.append(reactivo)
                    usado.append(used)
                    print("--------------------------------------")
        for i in range(len(usado)):
            GestionExperimentos.add_error(reactivos_experimento[i],error_reactivos[i],usado[i],receta)
            reactivos_experimento[i].storage-=usado[i] #se resta lo usado (que ya tiene en cuenta el error) del inventario
            cost+=usado[i]*reactivos_experimento[i].cost #acá se calcula el costo del experimento.
        num_people=int(input("\nIngrese el número de personas que trabajaron en el experimento: "))
        for i in range(0,num_people):
            name=input(f"Ingrese el nombre de la persona {i+1}: ")
            personas.append(name)
        date_exp=input("Ingrese la fecha en la que se realizó el experimento (y-m-d): ")
        result=input("Ingrese el resultado del experimento: ")
        print("\n¡Experimento creado con éxito!\n")
        return Experimento(id_exp,id_receta,personas,date_exp,cost,result)
    

    def add_error(reactivo: Reactivo, error: float, usado: float,receta: Recetas):
        teórico=usado-error
        for i in reactivo.errores:
                if i["receta_id"]==receta.id:
                    i["cantidades"].append(error)
                    return
        reactivo.errores.append({"receta_id":receta.id,"cantidades":[error],"teórico":teórico})



    def change_units(reactivo: Reactivo,receta_r_used):
        for units in reactivo.conversions:
            if units["unidad"]==receta_r_used["unidad_medida"]:
                receta_r_used["cantidad_necesaria"]/=units["factor"]
        receta_r_used["unidad_medida"]=reactivo.unit
        

    def obtain_reactivo(num, reactivos: List[Reactivo]):
        for reactivo in reactivos:
            if reactivo.id==num:
                return reactivo


    def search_receta(num, recetas: List[Recetas]):
        for receta in recetas:
            if receta.id==num:
                return receta
        return None
            

    def modify(self: Experimento):
        num=int(input("""\n¿Qué elemento desea modificar?\n
        1. Personas responsables.
        2. Fecha.
        3. Costo asociado.
        4. Resultado
        \n"""))
        if num==1:
            GestionExperimentos.modify_personas(self)
        if num==2:
            date=input(f"""Fecha vieja: {self.fecha}
            Ingrese la nueva fecha (y/m/d): """)
            self.fecha=date
        if num==3:
            cost=float(input(f"""Costo asociado viejo: {self.costo}\nCosto asociado nuevo: """))
            self.costo=cost
        if num==4:
            res=input(f"""Resultado viejo: {self.resultado}\nResultado nuevo: """)
            self.resultado=res


    def modify_personas(self: Experimento):
        print(f"Personas responsables: {self.experimentadores}")
        n=int(input("""¿Qué desea hacer?\n
        1. Agregar personas
        2. Eliminar personas\n\n"""))
        if n==1:
            n2=int(input("Ingrese el número de personas que agregará: "))
            for i in range(0,n2):
                name=input(f"Ingrese el nombre y apellido de la persona {i+1}: ")
                self.experimentadores.append(name.title())
            print("Experimentadores agregados con éxito\n")
        elif n==2:
            n=int(input("Ingrese el número de la persona que desea eliminar: "))-1
            self.experimentadores.pop(n)
            print("Experimentador eliminado con éxito\n")
        else:
            print("El valor ingresado es inválido\n")

    
    def display(self: Experimento): #Completado
        print(f"""Información del Experimento:
        Id: {self.id}
        Id de receta: {self.receta_id}
        Personas responsables: {self.experimentadores}
        Fecha: {self.fecha}
        Costo asociado: {self.costo}
        Resultado: {self.resultado}
        -----------------------------------------------""")


    def search_people(number: int, experimentos: List[Experimento]): #Completado
        names=[]
        result=[]
        for i in range(0,number):
            name=str(input(f"Ingrese el nombre y apellido del experimentador {i+1}: "))
            names.append(name.title())
        typ=int(input("""\n¿Qué tipo de búsqueda desea realizar?
        1. Experimentos donde hayan trabajado todos los experimentadores
        2. Experimentos donde haya trabajado al menos uno de los experimentadores
        \n"""))
        if typ==1:
            for experimento in experimentos:
                if set(names)==set(experimento.experimentadores):
                    result.append(experimento)
        if typ==2:
            for experimento in experimentos:
                common=set(names) & set(experimento.experimentadores)
                if common:
                    result.append(experimento)
        return(result)


    def search(experimentos: List[Experimento]): #Completado
        num=int(input("""Buscar por...\n
        1. Id
        2. Id de la receta
        3. Nombre(s) de experimentador(es)
        4. Fecha
        \n"""))
        results=[]
        if num==3:
            n=int(input("Ingrese el número de experimentadores que desea buscar: "))
            result=GestionExperimentos.search_people(n,experimentos)
            return result
        value=input("Ingrese el valor de búsqueda: ")
        for experimento in experimentos:
            if num==1:
                if int(value)==experimento.id:
                    return [experimento]
            if num==2:
                if int(value)==experimento.receta_id:
                    results.append(experimento)
            if num==4: #Para esto debería agregarle un mensaje al usuario para que sepa el formato de fecha
                #Después veré si puedo usar algún tipo de formato importado de datetime porque como lo tengo ahorita es un pupú
                if str(value)==experimento.fecha:
                    results.append(experimento)
        return results
