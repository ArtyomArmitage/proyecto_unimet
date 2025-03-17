from typing import List
from gestión_reactivos import GestionReactivos
from gestión_experimentos import GestionExperimentos
from gestión_recetas import GestionRecetas
from reactivos import Reactivo
from recetas import Recetas
from experimentos import Experimento
from estadísticas import Estadísticas
import utils

reactivos_f="reactivos.json"
experimentos_f="experimentos.json"
recetas_f="recetas.json"

#COSAS PENDIENTES:
#Evitar que un usuario pueda colocar un valor negativo al crear un nuevo reactivo

class Admin:
    def __init__(self):
        materiales,experimentos,recetas=utils.read_files(reactivos_f,experimentos_f,recetas_f)
        self.materiales: List[Reactivo] = materiales
        self.experimentos: List[Experimento] = experimentos
        self.recetas: List[Recetas] = recetas
        utils.write_file(recetas_f,self.recetas,3)
        utils.write_file(reactivos_f,self.materiales,1)


    def eliminate(self,n,group): 
        keys={1:GestionReactivos,2:GestionExperimentos}
        result=keys[n].search(group)
        for thing in result:
            if n==1:
                ans=str(input(f"¿Desea eliminar el reactivo {thing.name}? (y/n): "))
            if n==2:
                ans=str(input(f"¿Desea eliminar el experimento {thing.id}? (y/n): "))
            if ans=="y":
                group.remove(thing)


    def main_menu(self):
        valid_answers=[1,2,3,4]
        module=input("""
        1. GESTIÓN DE REACTIVOS
        2. GESTIÓN DE EXPERIMENTOS
        3. GESTIÓN DE RESULTADOS
        4. ESTADÍSTICAS
    \n""")
        try:
            if int(module)==1:
                print("\n###MÓDULO DE GESTIÓN DE REACTIVOS###")
                reached_min,are_expired=GestionReactivos.check_inventory(self.materiales)
                print(f"""\nBienvenido, 
Tiene {len(reached_min)} reactivo(s) que han llegado al mínimo recomendado: {reached_min}
Tiene {len(are_expired)} reactivo(s) expirado(s): {are_expired}""")
                options=int(input("""
        1. Nuevo reactivo
        2. Editar reactivo(s)
        3. Eliminar reactivo(s)
        4. Buscar reactivo(s) (mostrar información)
        \n"""))
                if options==1:
                    idvalue=(self.materiales[-1].id+1)
                    name, description, cost, category, inventory, unit, date, min=GestionReactivos.new_r()
                    new=Reactivo(idvalue, name, description, cost, category, inventory, unit, date, min,0)
                    new=GestionReactivos.conversiones(new)
                    Reactivo.is_expired(new)
                    Reactivo.check_fechas(new)
                    self.materiales.append(new)
                    print("\n¡Reactivo creado con éxito!")
                elif options==2:
                    result=GestionReactivos.search(self.materiales)
                    for reactivo in result:
                        check=input(f"¿Desea modificar el reactivo {reactivo.name}? (y/n): ").lower()
                        if check=="y":
                            GestionReactivos.modify(reactivo)
                elif options==3:
                    self.eliminate(1,self.materiales)
                elif options==4:
                    result=GestionReactivos.search(self.materiales)
                    for r in result:
                        GestionReactivos.display(r)
                else:
                    print("El valor ingresado es inválido")
                utils.write_file(reactivos_f,self.materiales,1)
            elif int(module)==2:
                print("\n###MÓDULO DE GESTIÓN DE EXPERIMENTOS###")
                options=int(input("""
        1. Nuevo experimento
        2. Editar experimento(s)
        3. Eliminar experimento(s)
        4. Buscar experimento(s) (mostrar información)
        \n"""))
                if options==1:
                    id_exp=(self.experimentos[-1].id+1)
                    new_exp=GestionExperimentos.new_exp(id_exp,self.recetas,self.materiales)
                    if new_exp==None:
                        print("No se creó ningún experimento nuevo\n")
                    else:
                        self.experimentos.append(new_exp)
                        utils.write_file(reactivos_f,self.materiales,1)
                        utils.write_file(recetas_f,self.recetas,3)
                elif options==2:
                    result=GestionExperimentos.search(self.experimentos)
                    if result==[]:
                        print("No existe ningún experimento con el valor indicado.\n")
                    for experimento in result:
                        check=input(f"¿Desea modificar el experimento {experimento.id}? (y/n): ").lower()
                        if check=="y":
                            GestionExperimentos.modify(experimento)
                elif options==3:
                    self.eliminate(2,self.experimentos)
                elif options==4:
                    result=GestionExperimentos.search(self.experimentos)
                    if result==[]:
                        print("No existe ningún experimento con el valor indicado.\n")
                    for exp in result:
                        GestionExperimentos.display(exp)
                else:
                    print("El valor ingresado es inválido")
                utils.write_file(experimentos_f,self.experimentos,2)
            elif int(module)==3:
                print("\n###MÓDULO DE GESTIÓN DE RESULTADOS###")
                options=int(input("""
        1. Validar resultados.
        2. Buscar recetas.
        \n"""))
                if options==1:
                    num=int(input("""\nBienvenido. Aquí podrá comparar sus resultados experimentales con los teóricos.
        Para comenzar, ingrese el ID del experimento que desea validar: """))
                    GestionRecetas.evaluate_result(num,self.experimentos,self.recetas)
                elif options==2:
                    result=GestionRecetas.search(self.recetas)
                    if result==[]:
                        print("No existe ninguna receta con el valor especificado\n")
                    for r in result:
                        GestionRecetas.display(r)
                else:
                    print("El valor ingresado es inválido")
            elif int(module)==4:
                print("\nINVESTIGADORES QUE MÁS USAN EL LAB:\n")
                Estadísticas.investigadores(self.experimentos)
                print("\nEXPERIMENTO MÁS HECHO Y MENOS HECHO:\n")
                Estadísticas.experimentos(self.experimentos,self.recetas)
                print("\n5 REACTIVOS MÁS USADOS:\n")
                Estadísticas.reactivos_us(self.materiales,self.experimentos,self.recetas)
                print("\n3 REACTIVOS CON MÁS DESPERDICIO:\n")
                Estadísticas.reac_desperdicio(self.materiales)
                print("\nREACTIVOS QUE MÁS SE VENCEN:\n")
                Estadísticas.reac_vencidos(self.materiales)
                print("\nN° DE VECES QUE NO SE REALIZÓ UN EXPERIMENTO POR FALTA DE REACTIVOS:\n")
                Estadísticas.experimentos_not_done(self.recetas)
            elif(int(module)) not in valid_answers:
                print("\nEl valor ingresado es inválido\n")
        except:
            print("\nEl valor ingresado es inválido.\n")


    def start(self):
        process="y"
        #Esto para que el programa se ejecute hasta que el usuario diga lo contrario
        while process=="y":
            self.main_menu()
            process=input("¿Desea continuar? (y/n): ").lower()

admin=Admin()
admin.start()

