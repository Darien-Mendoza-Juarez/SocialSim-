import csv
import random
from datetime import datetime
import os

class Usuario:
    def __init__(self, nombre, edad, correo, password, conexiones, arbol):
        self.nombre = nombre
        self.edad = edad
        self.correo = correo
        self.password = password
        self.publicaciones =[]
        self.conexiones = conexiones
        self.seguidores = []
        self. arbol = arbol

    def user_sesion(self):
        while True:
            print("1)Perfil\n2)Personas\n3)Publicaciones\n4)Cerrar sesión")
            op = int(input())
            match op:
                case 1:
                    self.perfil()
                case 2:
                    self.personas()
                case 3:
                    self.publics()
                case 4:
                    print("Saliendo...")
                    return
                case _:
                    print("Opción inválida, intente de nuevo")

    def perfil(self):
        while True:
            print("Elija una ocpion por favor\n1)Ver perfil\n2)Editar perfil\n3)Salir")
            try:
                op = int(input())
            except ValueError:
                    print("Error: Por favor ingresa un numero.")
                    op = 0
            match op:
                case 1:
                    print(f"Nombre: {self.nombre}, Edad: {self.edad}, Correo: {self.correo}")
                case 2:
                    self.editar_perfil()
                case 3:
                    return
                case _:
                    print("Opcion invalida, intente de nuevo")

    def editar_perfil(self):
        while True:
            opcion = input("Que desea cambiar?\n1)Nombre\n2)Edad\n3)Password\n4)Cancelar")
            match opcion:
                case "1":
                    nuevo_nombre = input("Ingrese el nuevo nombre: ")
                    if self.arbol.search(nuevo_nombre):
                        print("Error: El nombre de usuario ya esta en uso. Elija otro nombre.")  
                    else:
                        if self.nombre in self.conexiones.adyacencias:
                            self.conexiones.agregar_nodo(nuevo_nombre)
                            for conexion in self.conexiones.adyacencias[self.nombre]:
                                self.conexiones.agregar_arista(nuevo_nombre, conexion)
                            self.conexiones.adyacencias.pop(self.nombre)
                        with open("BaseDeDatos.csv", mode='r', newline='', encoding='utf-8') as archivo:
                            lector = csv.reader(archivo)
                            lineas =[linea for linea in lector if linea[0] != self.nombre]
                        with open("BaseDeDatos.csv", mode='w', newline='', encoding='utf-8') as archivo:
                            escritor = csv.writer(archivo)
                            for linea in lineas:
                                escritor.writerow(linea)
                        with open("BaseDeDatos.csv", mode='a', newline='', encoding='utf-8') as archivo:
                            escritor = csv.writer(archivo)
                            escritor.writerow([nuevo_nombre, self.edad, self.correo, self.password])

                        self.arbol.delete(self.nombre)
                        self.guardar_nombre(nuevo_nombre)
                        self.nombre = nuevo_nombre
                        self.arbol.insert(self.nombre, self)                         
                        
                case "2":
                    try:
                        self.edad = int(input("Ingresa la nueva edad: "))
                    except ValueError:
                        print("Error: Por favor ingresa un numero.")
                case "3":
                    self.password = input("Ingrese el nuevo pasword: ")
                case "4":
                    return
                case _:
                    print("Opcion invalida, intente una opcion dentro de las que se ofrecen")

    def guardar_nombre(self, new_name):
      
        try:
            os.rename(self.nombre, new_name)
            print(f"La carpeta ha sido renombrada a '{new_name}'.")
        except FileNotFoundError:
            print(f"La carpeta '{self.nombre}' no existe.")
        except Exception as e:
            print(f"Error al renombrar la carpeta: {e}")
        os.chdir(new_name)
        data =[]
        with open(self.nombre+".csv", mode='r', newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for linea in lector:
                seguido = linea[0]
                data.append(seguido)
        
        if os.path.exists(self.nombre+".csv"):
            os.remove(self.nombre+".csv")
        else:
            print(f"El archivo de'{self.nombre}' no existe.")

        with open(new_name+".csv", mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            for seguido in data:
                escritor.writerow([seguido])
        os.chdir('..')

    def personas(self):
        while True:
            print("1)Ver seguidores\n2)Ver seguidos\n3)Seguir usuario\n4)Dejar de seguir usuario\n5)Sugerencias de amistad\n6)Salir")
            try:
                op = int(input())
            except ValueError:
                    print("Error: Por favor ingresa un numero.")
                    op = 0
            match op:
                case 1:
                    self.ver_seguidores()
                case 2:
                    self.ver_seguidos()
                case 3:
                    usuario_destino = input("Escriba el nombre del usuario a seguir: ") 
                    self.seguir_usuario(usuario_destino)
                case 4:
                    usuario_destino = input("Escriba el nombre del usuario: ") 
                    self.dejar_de_seguir(usuario_destino)                
                case 5:    
                    print("Sugerencias de amistad:")
                    self.conexiones.sugerencias_amistad(self.nombre)                
                case 6:
                    return
                case _:
                    print("Opción inválida, intente de nuevo")
    
    def ver_seguidos(self):
        if self.nombre in self.conexiones.adyacencias:
            seguidos = self.conexiones.adyacencias[self.nombre]
            if len(seguidos) > 0:
                print("Seguidos:", seguidos)
            else:
                print("No sigues a nadie actualmente.")
        else:
            print("Error, no esta este usuario en el conexiones")

    def ver_seguidores(self):
        print("Seguidores:", self.seguidores)

    def seguir_usuario(self, destino):
            self.conexiones.agregar_arista(self.nombre, destino)
            os.chdir(self.nombre) 
            with open(self.nombre+".csv", mode='a', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow([destino])
            
            os.chdir('..')

    def dejar_de_seguir(self, destino):
        self.conexiones.eliminar_arista(self.nombre, destino)
        os.chdir(self.nombre) 
        with open(self.nombre+".csv", mode='r', newline='') as archivo:
            lector = csv.reader(archivo)
            lineas = [linea for linea in lector if linea[0] != destino]

        with open(self.nombre+".csv", mode='w', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(lineas)
        
        os.chdir('..')
    
    def publics(self):
        while True:
            print("1)Crear publicación\n2)Ver publicaciones de otro usuario\n3) Ver mis publicaciones\n4)Buscar publicacion\n5)Ordenar mis publicaciones\n6)Salir\n7)Borrar Publicacion\n")
            try:
                op = int(input())
            except ValueError:
                    print("Error: Por favor ingresa un numero.")
                    op = 0
            match op:
                case 1:
                    self.crear_publicacion()
                case 2:
                    destino =input("Escriba el nombre del usuario a buscar: ")
                    usuario = self.arbol.search(destino)
                    if usuario:
                        usuario.mostrar_publicaciones()
                    else:
                        print("Usuario no encontrado")
                case 3:
                    self.mostrar_publicaciones()
                case 4:
                    destino = input("Escriba el nombre del usuario a buscar: ")
                    usuario = self.arbol.search(destino)
                    if usuario:
                        op = input("Elija 1) para titulo o 2) para nombre")
                        if op =="1":
                            titulo = input("Ingrese el titulo: ")
                            usuario.buscar_publicacion_por_titulo(titulo)
                        elif op == "2":
                            fecha = input("Ingrese year, month y day de la creación de su publicación (YYYY-MM-DD):")
                            usuario.buscar_publicacion_por_fecha(fecha)
                        else: 
                            print("opcion invalida")
                    else:
                        print("Usuario no encontrado")
                case 5:
                    op = input("Elija 1) para fecha o 2) para titulo")
                    if op =="1":
                        self.ordenar_por_fecha()
                    elif op == "2":
                        self.ordenar_por_titulo()
                    else: 
                        print("opcion invalida")
                case 6:
                    return
                case 7:
                    self.borrar_publicacion()
                case _:
                    print("Opción inválida, intente de nuevo")

    def crear_publicacion(self):
        titulo = input("Ingrese un encabezado: ")
        if self.buscar_publicacion_por_titulo(titulo) != None:
            print("Error, encabezado ya existente en tus publicaciones")
            return
        contenido = input("Ingrese su mensaje: ")
        nueva_publicacion = Publicacion(self.nombre, titulo, contenido)
        self.publicaciones.append(nueva_publicacion)
        self.ordenar_por_fecha()
        nombre_archivo = os.path.join(self.nombre, nueva_publicacion.titulo + ".txt")
        with open(nombre_archivo, "w") as archivo:
            archivo.write(nueva_publicacion.contenido)
            print(f"publicacion de titulo'{nueva_publicacion.titulo}' creada.")

    def borrar_publicacion(self):
        eliminar = input("Escriba el titulo de la publicacion por favor: ")
        index= self.buscar_publicacion_por_titulo(eliminar)
        self.publicaciones.pop(index)


        os.chdir(self.nombre)
        archivo_a_borrar = eliminar+".txt"
        if os.path.exists(archivo_a_borrar):
            os.remove(archivo_a_borrar)
            print(f"Publicacion '{archivo_a_borrar}' borrado exitosamente.")
        else:
            print(f"El archivo '{archivo_a_borrar}' no existe.")
        os.chdir('..')


    def ordenar_por_titulo(self):
        self.publicaciones = self.merge_sort(self.publicaciones, key=lambda pub: pub.titulo)

    def ordenar_por_fecha(self):
        self.publicaciones = self.merge_sort(self.publicaciones, key=lambda pub: pub.fecha_creacion, reverse=True)

    def merge_sort(self, arr, key=lambda x: x, reverse=False):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid], key=key, reverse=reverse)
        right = self.merge_sort(arr[mid:], key=key, reverse=reverse)
        return self.merge(left, right, key, reverse)

    def merge(self, left, right, key, reverse):
        sorted_list = []
        while left and right:
            if (key(left[0]) > key(right[0])) if reverse else (key(left[0]) < key(right[0])):
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))
        sorted_list.extend(left or right)
        return sorted_list

    def buscar_publicacion_por_titulo(self, titulo):
        self.ordenar_por_titulo()  
        izquierda, derecha = 0, len(self.publicaciones) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if self.publicaciones[medio].titulo == titulo:
                return medio
            elif self.publicaciones[medio].titulo < titulo:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return None

    def buscar_publicacion_por_fecha(self, fecha):
        self.ordenar_por_fecha()  
        izquierda, derecha = 0, len(self.publicaciones) - 1
        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if self.publicaciones[medio].fecha_creacion == fecha:
                return medio
            elif self.publicaciones[medio].fecha_creacion < fecha:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        return None

    def editar_publicacion(self):
        op = 0
        while op != 1 and op != 2:
            try:
                op = int(input("Desea buscar por 1)titulo o 2)fecha: "))
            except ValueError:
                op = 0
                print("Opcion invalida, por favor ingresa un numero.")
                
        match op:
            case 1:
                titulo = input("Ingrese el encabezado: ")
                index = self.buscar_publicacion_por_titulo(titulo)
            case 2:
                fecha = input("Ingrese year, month y day de la creación de su publicación (YYYY-MM-DD): ")
                index = self.buscar_publicacion_por_fecha(fecha)

        if index is not None:
            if self.publicaciones[index].propietario == self.nombre:
                nuevo_titulo = input("Ingrese el nuevo título: ")
                nuevo_contenido = input("Ingrese el nuevo contenido: ")
                self.publicaciones[index].editar_publicacion(nuevo_titulo, nuevo_contenido)
                print("Publicación editada con éxito.")
            else:
                print("Error, no eres el dueño de la publicación.")
        else:
            print("Publicación no encontrada.")

    def mostrar_publicaciones(self):
        total_publicaciones = len(self.publicaciones)
        if total_publicaciones == 0:
            print("No hay publicaciones disponibles.")
            return

        inicio = 0
        while True:
            fin = min(inicio + 10, total_publicaciones)
            for i in range(inicio, fin):
                print(f"Publicación:\n{self.publicaciones[i].mostrar_publicacion()}\n")

            if fin == total_publicaciones:
                print("No hay más publicaciones para mostrar.")
                break

            print("Seleccione una opción:\n1)Cargar las siguientes 10 publicaciones\n2)Salir")
            opcion = 0
            while opcion != 1 and opcion != 2:
                try:
                    opcion = int(input())
                except ValueError:
                    opcion = 0
                    print("Entrada invalida, por favor ingresa un numero.")

            if opcion == 1:
                inicio += 10
            elif opcion == 2:
                return
            else:
                print("Opción inválida.")

    def cargar_publicaciones(self):
        nombre_carpeta = self.nombre 

        if not os.path.exists(nombre_carpeta):
            os.makedirs(nombre_carpeta)
            print(f"Carpeta '{nombre_carpeta}' creada.")
        else:
            print(f"La carpeta '{nombre_carpeta}' ya existe. Leyendo archivos...")

            for nombre_archivo in os.listdir(nombre_carpeta):
                if nombre_archivo.endswith(".txt"):
                    nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
                    ruta_archivo = os.path.join(nombre_carpeta, nombre_archivo)
                    with open(ruta_archivo, "r") as archivo:
                        contenido = archivo.read()
                        nueva_publicacion = Publicacion(self.nombre, nombre_sin_extension, contenido)
                        self.publicaciones.append(nueva_publicacion)
            self.ordenar_por_fecha()

    def cargar_conexiones(self):
        os.chdir(self.nombre)
        with open(self.nombre+".csv", mode='a', newline='', encoding='utf-8') as archivo:
            pass
        with open(self.nombre+".csv", mode='r', newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            for linea in lector:
                origen = self.nombre
                seguido = linea[0]
                self.conexiones.agregar_arista(origen,seguido)
        os.chdir('..')

class Publicacion:
    def __init__(self,propietario, titulo, contenido):
        self.propietario = propietario # creado para usarse como apuntador al dueño,
                                       #garantizara que solo el que hizo la publicacion la edite 
        self.titulo = titulo
        self.contenido = contenido
        self.fecha_creacion = datetime.now()
        self.likes = 0

    def dar_like(self):
        self.likes += 1

    def editar_publicacion(self, nuevo_titulo, nuevo_contenido):
        self.titulo = nuevo_titulo
        self.contenido = nuevo_contenido

    def mostrar_publicacion(self):
        fecha_formateada = self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        return (f"Título: {self.titulo}\n"
                f"Contenido: {self.contenido}\n"
                f"Fecha de creación: {fecha_formateada}\n"
                f"Likes: {self.likes}")
    
    def guardar_publicacion(self):
        with open(self.titulo + ".csv", mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([self.titulo, self.contenido, self.fecha_creacion])


class BPlusTreeNode:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf
        self.next_leaf = None 


class BPlusTree:
    def __init__(self, order):
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order
    
    def insert(self, key, user_obj):
        node = self.root
        if len(node.keys) == self.order - 1:
            new_root = BPlusTreeNode()
            new_root.children.append(self.root)
            self._split_child(new_root, 0, self.root)
            self.root = new_root
        self._insert_non_full(self.root, key, user_obj)
    
    def _insert_non_full(self, node, key, user_obj):
        if node.is_leaf:
            index = 0
            while index < len(node.keys) and key > node.keys[index][0]:
                index += 1
            node.keys.insert(index, (key, user_obj))
        else:
            # Busca donde insertar si no es una hoja 
            index = 0
            while index < len(node.keys) and key > node.keys[index]:
                index += 1
            if len(node.children[index].keys) == self.order - 1:
                self._split_child(node, index, node.children[index])
                if key > node.keys[index]:
                    index += 1
            self._insert_non_full(node.children[index], key, user_obj)
    
    def _split_child(self, parent, index, child):
        new_child = BPlusTreeNode(is_leaf=child.is_leaf)
        mid = self.order // 2
        
        new_child.keys = child.keys[mid:]
        child.keys = child.keys[:mid]
        
        if not child.is_leaf:
            new_child.children = child.children[mid:]
            child.children = child.children[:mid]
        
        parent.children.insert(index + 1, new_child)
        parent.keys.insert(index, child.keys[-1] if not child.is_leaf else new_child.keys[0][0])
        
        if child.is_leaf:
            new_child.next_leaf = child.next_leaf
            child.next_leaf = new_child

    def search(self, name):
        return self._search(self.root, name)
    
    def _search(self, node, name):
        if node.is_leaf:
            for key, user_obj in node.keys:
                if key == name:
                    return user_obj
            return None
        else:
            index = 0
            while index < len(node.keys) and name > node.keys[index]:
                index += 1
            return self._search(node.children[index], name)
    
    def delete(self, key):
        self._delete(self.root, key)
        
        # Si la raíz queda vacía y no es una hoja, se ajusta el árbol.
        if len(self.root.keys) == 0 and not self.root.is_leaf:
            self.root = self.root.children[0]

    def _delete(self, node, key):
        if node.is_leaf:
            # Eliminar clave en una hoja
            for i, (k, obj) in enumerate(node.keys):
                if k == key:
                    node.keys.pop(i)
                    return True
            return False  # Clave no encontrada en la hoja
        else:
            # Encontrar el índice del hijo por donde proceder con la eliminación
            index = 0
            while index < len(node.keys) and key > node.keys[index]:
                index += 1
            
            child = node.children[index]
            if child.is_leaf:
                # Caso especial de eliminar clave en un nodo hoja
                for i, (k, obj) in enumerate(child.keys):
                    if k == key:
                        child.keys.pop(i)
                        # Verificar si necesita fusionarse o redistribuirse
                        self._fix_delete(node, index)
                        return True
                return False
            else:
                # Llamada recursiva para eliminar en nodo interno
                if self._delete(child, key):
                    # Si el hijo se queda con menos claves de las necesarias
                    self._fix_delete(node, index)
                    return True
                return False

    def _fix_delete(self, parent, index):
        """Función para manejar la redistribución y fusión después de eliminar"""
        child = parent.children[index]
        
        # Si el hijo tiene suficientes claves, no hacer nada
        if len(child.keys) >= (self.order + 1) // 2:
            return
        
        # Caso de redistribución o fusión
        if index > 0 and len(parent.children[index - 1].keys) > (self.order + 1) // 2:
            # Tomar prestado del nodo izquierdo
            left_sibling = parent.children[index - 1]
            child.keys.insert(0, parent.keys[index - 1])
            if not child.is_leaf:
                child.children.insert(0, left_sibling.children.pop())
            parent.keys[index - 1] = left_sibling.keys.pop()
        elif index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > (self.order + 1) // 2:
            # Tomar prestado del nodo derecho
            right_sibling = parent.children[index + 1]
            child.keys.append(parent.keys[index])
            if not child.is_leaf:
                child.children.append(right_sibling.children.pop(0))
            parent.keys[index] = right_sibling.keys.pop(0)
        else:
            # Fusionar con el hermano izquierdo o derecho
            if index > 0:
                # Fusionar con el hermano izquierdo
                left_sibling = parent.children[index - 1]
                left_sibling.keys.extend(child.keys)
                if not child.is_leaf:
                    left_sibling.children.extend(child.children)
                parent.keys.pop(index - 1)
                parent.children.pop(index)
                left_sibling.next_leaf = child.next_leaf
            else:
                # Fusionar con el hermano derecho
                right_sibling = parent.children[index + 1]
                child.keys.extend(right_sibling.keys)
                if not child.is_leaf:
                    child.children.extend(right_sibling.children)
                parent.keys.pop(index)
                parent.children.pop(index + 1)
                child.next_leaf = right_sibling.next_leaf



def cargar_datos(filename, datos, conexiones):
    registros = []
    with open(filename, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for linea in lector:
            if len(linea) == 4: 
                    nombre = linea[0]
                    edad =  int(linea[1])
                    correo = linea[2]
                    password =  linea[3]
                    usuario = Usuario(nombre, edad, correo, password, conexiones, datos)
                    usuario.cargar_publicaciones()
                    datos.insert(nombre,usuario)
                    conexiones.agregar_nodo(nombre)
                    registros.append(usuario)
            else: 
                print("Error linea incompleta")
    
    for usuario in registros:
        usuario.cargar_conexiones()
    return 

def verificar_correo(filename, correo):
    with open(filename, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        for linea in lector:
            if len(linea) == 4: 
                    if correo == linea[2]:
                        return True
            else: 
                print("Error linea incompleta")
        return False
    
    return registros

def guardar_datos(filename, usuario):
    with open(filename, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([usuario.nombre, usuario.edad, usuario.correo, usuario.password])

        
class Conexiones:
    def __init__(self, arbol):
        self.adyacencias = {}
        self.arbol =arbol

    def agregar_nodo(self, nodo):
        if nodo not in self.adyacencias:
            self.adyacencias[nodo] = []

    def agregar_arista(self, origen, destino):
        if origen in self.adyacencias and destino in self.adyacencias:
            if destino not in self.adyacencias[origen]:
                self.adyacencias[origen].append(destino)
                destino_usuario = self.obtener_usuario(destino)
                if destino_usuario:
                    destino_usuario.seguidores.append(origen)
                print(f"Ahora sigues a {destino}.")
            else:
                print(f"Ya sigues a {destino}")
        else:
            print("No es posible realizar la operación.")

    def obtener_usuario(self, nombre):
        return self.arbol.search(nombre)
    
    def eliminar_arista(self, origen, destino):
        if origen in self.adyacencias and destino in self.adyacencias:
            if destino in self.adyacencias[origen]:
                self.adyacencias[origen].remove(destino)
                destino_usuario = self.obtener_usuario(destino)
                if destino_usuario and origen in destino_usuario.seguidores:
                    destino_usuario.seguidores.remove(origen)
                print(f"Dejaste de seguir a {destino}.")
            else:
                print(f"No sigues a {destino}.")
        else:
            print("No es posible realizar la operación.")

    def mostrar_grafo(self):
        for nodo, vecinos in self.adyacencias.items():
            print(f"{nodo} -> {', '.join(vecinos)}")

    def sugerencias_amistad(self, origen):
        if origen not in self.adyacencias:
            print("Usuario no encontrado en el grafo de conexiones.")
            return

        sugerencias = set()
        seguidos = list(self.adyacencias[origen])
    
        intentos = 0
        while len(sugerencias) < 10 and intentos < 5:
            seguido = random.choice(seguidos)
        
            if seguido in self.adyacencias:
                amigos_de_amigos = list(self.adyacencias[seguido])
                amigos_agregados = 0
            
                random.shuffle(amigos_de_amigos)
                for amigo in amigos_de_amigos:
                    if amigo != origen and amigo not in seguidos and amigo not in sugerencias:
                        sugerencias.add(amigo)
                        amigos_agregados += 1
                        if amigos_agregados >= 3:
                            break
        
            intentos += 1  #se hace maximo 5 veces o hasta que se llene sugerencias con 10 elementos
        if sugerencias:
            print(f"Te sugerimos seguir a {', '.join(sugerencias)}")
        else:
            print("No hay nuevas sugerencias de amistad.")



def red_Social():
    bplus_tree = BPlusTree(order=4)  
    conexiones = Conexiones(bplus_tree)
    cargar_datos("BaseDeDatos.csv", bplus_tree, conexiones)
    
    while True:
        print("Bienvenido, por favor escoja una opción.")
        print("1) Iniciar sesión\n2) Registrarse\n3) Salir")    
        try:
            op = int(input())
        except ValueError:
            op = 0
            print("Entrada invalida, por favor ingresa un numero.")

        match op:
            case 1:
                nombre = input("Ingrese su nombre de usuario: ")
                usuario = bplus_tree.search(nombre)
                if usuario:
                    print("Usuario encontrado.")
                    password = input("Ingrese su pasword: ")
                    if password == usuario.password:
                        usuario.user_sesion()
                    else:
                        print("Password incorrecto, intente de nuevo") 
                else:
                    print("Usuario no encontrado.")
            case 2:
                nombre = input("Nombre: ")
                if bplus_tree.search(nombre):
                    print("Error: El nombre de usuario ya esta en uso. Elija otro nombre.")  
                    continue 

                edad = int(input("Edad: "))
                correo = input("Correo: ")
                if verificar_correo("BaseDeDatos.csv", correo):
                    print("Error: Correo ya en uso, favor de utilizar otro.")  
                    continue
                password = input("Contraseña: ")
                usuario = Usuario(nombre, edad, correo, password,conexiones,bplus_tree)
                bplus_tree.insert(nombre, usuario)
                guardar_datos("BaseDeDatos.csv", usuario)
                nombre_carpeta = usuario.nombre
                if not os.path.exists(nombre_carpeta):
                    os.makedirs(nombre_carpeta)
                    print(f"Carpeta de'{nombre_carpeta}' creada.")
                ruta_archivo = os.path.join(nombre_carpeta, usuario.nombre+".csv")
                if not os.path.exists(ruta_archivo):
                    with open(ruta_archivo, mode='w', newline='') as archivo:
                        pass
                print("Usuario registrado exitosamente.")
            case 3:
                print("Hasta pronto")
                return
            case _:
                print("Opción inválida, intente de nuevo")

red_Social()