from reactivos import *
import json
import datetime

class GestionReactivos():
    def new_r():
        name=str(input("Nombre del reactivo: "))
        description=(input("Descripción: "))
        cost=GestionReactivos.input_validation_float("Costo: ")
        category=str(input("Categoría: "))
        inventory=GestionReactivos.input_validation_float("Cantidad disponible (sin unidad): ")
        unit=str(input("Unidad de la cantidad: "))
        date=str(input("Fecha de caducidad (y-m-d) (si no aplica, escribir N/A): "))
        min=GestionReactivos.input_validation_float("Mínimo sugerido: ")
        return name, description, cost, category, inventory, unit, date, min

    def conversiones(self: Reactivo):
        num=int(input("N° de conversiones que desea añadir: "))
        for i in range(0,num):
            new_unit=str(input("Unidad de la conversión: "))
            factor=float(input("Factor de conversión: "))
            change={"unidad":new_unit,"factor":factor}
            self.conversions.append(change)
        return self

    def modify(self: Reactivo):
        num=int(input("""\n¿Qué elemento desea modificar?\n
        1. Nombre
        2. Descripción
        3. Costo
        4. Categoría
        5. Inventario disponible
        6. Unidad medida
        7. Fecha de caducidad
        8. Mínimo sugerido
        9. Conversiones posibles
        \n"""))
        options={1:"name", 2:"description", 3:"cost", 4:"category", 5:"storage", 7:"due_date", 8:"min"}
        if num in [1,2,4,7]:
            print(f"Valor viejo: {getattr(self,options[num])}")
            new=input("Valor nuevo: ")
            setattr(self,options[num],new)
            print("Valores actualizados\n")
            if num==7:
                self.expired=Reactivo.is_expired(self)
        elif num in [3,5,8]:
            print(f"Valor viejo: {getattr(self,options[num])}")
            new=float(input("Valor nuevo: "))
            setattr(self,options[num],new)
            print("Valores actualizados\n")
        elif num==6:
            if len(self.conversions)>=1:
                print(f"Conversiones disponibles: {self.conversions}")
                n=int(input("Ingrese el número de la unidad que desea: "))-1
                new_unit=self.conversions.pop(n)
                old_unit={"unidad":self.unit,"factor":(1/new_unit["factor"])}
                self.conversions.append(old_unit)
                self.unit=new_unit["unidad"]
                self.storage=self.storage*new_unit["factor"]
                self.min=self.min*new_unit["factor"]
                self.cost=self.cost/new_unit["factor"]
                print("Unidad cambiada con éxito\n")
            else: #si la lista de conversiones está vacía
                print("No hay conversiones disponibles.\n")
        elif num==9:
            print(f"Conversiones posibles: {self.conversions}")
            n1=int(input("""¿Qué desea hacer?\n
        1. Añadir una nueva conversión.
        2. Modificar una existente
        3. Eliminar una conversión
            \n"""))
            if n1==1:
               GestionReactivos.conversiones(self)
            elif n1==2:
                n=int(input("Ingrese el número de la conversión que desea modificar: "))-1
                uni=str(input("Nueva unidad: "))
                factor=float(input("Nuevo factor de conversión: "))
                self.conversions[n]["unidad"]=uni
                self.conversions[n]["factor"]=factor
            elif n1==3:
                n=int(input("Ingrese el número de la conversión que desea eliminar: "))-1
                self.conversions.pop(n)
            print("Acción completada\n")

    def display(self: Reactivo):
        print(f"""Información del Reactivo {self.name}:
        Id: {self.id}
        Nombre: {self.name}
        Descripción: {self.description}
        Costo: {self.cost}
        Categoría: {self.category}
        Inventario disponible: {self.storage}
        Unidad medida: {self.unit}
        Fecha de caducidad: {self.due_date}
        Mínimo sugerido: {self.min}
        Conversiones posibles: {self.conversions}
        Expirado: {self.expired}
        -----------------------------------------------""")

    def search(reactivos: List[Reactivo]):
        num=int(input("""Buscar por...\n
        1. Id
        2. Nombre
        3. Categoría
        \n"""))
        value=input("Ingrese el valor de búsqueda: ")
        results=[]
        for reactivo in reactivos:
            if num==1:
                if int(value)==reactivo.id:
                    return [reactivo]
            if num==2:
                if value in reactivo.name:
                    results.append(reactivo)
            if num==3:
                if value in reactivo.category:
                    results.append(reactivo)
        names=[reactivo.name for reactivo in results] #Me encanta esto de comprensión de listas
        print(f"Reactivos encontrados: {names}")
        return results
        
    def check_inventory(reactivos: List[Reactivo]):
        min=[]
        expired=[]
        for reactivo in reactivos:
            if float(reactivo.min)>=float(reactivo.storage):
                min.append(reactivo.name)
            if reactivo.expired==True:
                expired.append(reactivo.name)
        return min,expired


    def input_validation_float(text):
        while True:
            try:
                value=float(input(f"{text}"))
                if value>0:
                    return value
                else:
                    print("\nEl valor no puede ser negativo. Inténtalo otra vez\n")
            except ValueError:
                print("El valor ingresado no es válido. Inténtalo otra vez\n")

