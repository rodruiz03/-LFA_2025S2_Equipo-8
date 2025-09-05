"""
Sistema de Gestión de Biblioteca Digital
Proyecto 1 - Lenguajes Formales y Autómatas
"""
#solo son librerias que se utilizan una es para la fecha en este caso datetime y por ultimo la libreria
#os pero esas se utiliza para operaciones logicas y las 2 provienen de python 
#no se utilizaron json ni nada parecido porque pues no se permite y ya esta la verdad

from datetime import datetime, date
import os

class Usuario:
    """Clase para representar un usuario de la biblioteca"""
    def __init__(self, id_usuario, nombre_usuario):
        self.id_usuario = int(id_usuario)
        self.nombre_usuario = nombre_usuario.strip()
    
    def __str__(self):
        return f"Usuario({self.id_usuario}, {self.nombre_usuario})"

class Libro:
    """Clase para representar un libro en el catálogo"""
    def __init__(self, id_libro, titulo_libro):
        self.id_libro = id_libro.strip()
        self.titulo_libro = titulo_libro.strip()
    
    def __str__(self):
        return f"Libro({self.id_libro}, {self.titulo_libro})"

class Prestamo:
    """Clase para representar un préstamo de libro"""
    def __init__(self, id_usuario, nombre_usuario, id_libro, titulo_libro, 
                 fecha_prestamo, fecha_devolucion=None):
        self.id_usuario = int(id_usuario)
        self.nombre_usuario = nombre_usuario.strip()
        self.id_libro = id_libro.strip()
        self.titulo_libro = titulo_libro.strip()
        self.fecha_prestamo = self._parsear_fecha(fecha_prestamo.strip())
        self.fecha_devolucion = self._parsear_fecha(fecha_devolucion.strip()) if fecha_devolucion and fecha_devolucion.strip() else None
        self.devuelto = self.fecha_devolucion is not None
    
    def _parsear_fecha(self, fecha_str):
        """Convierte string de fecha a objeto date"""
        try:
            return datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return None
    
    def esta_vencido(self):
        """Verifica si el préstamo está vencido"""
        if self.devuelto:
            return False
        if not self.fecha_devolucion:
            return False
        return date.today() > self.fecha_devolucion
    
    def __str__(self):
        return f"Prestamo({self.id_usuario}, {self.id_libro}, {self.fecha_prestamo})"

class AnalizadorLexico:
    """Clase para analizar léxicamente el archivo de préstamos"""
    
    @staticmethod
    def validar_linea(linea, numero_linea):
        """Valida una línea del archivo y reporta errores"""
        errores = []
        
        # Verificar caracteres válidos (letras, números, espacios, comas, guiones)
        caracteres_validos = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.-ñÑáéíóúÁÉÍÓÚüÜ')
        
        for i, caracter in enumerate(linea):
            if caracter not in caracteres_validos:
                errores.append(f"Línea {numero_linea}, posición {i+1}: carácter inválido '{caracter}'")
        
        return errores
    
    @staticmethod
    def parsear_linea(linea, numero_linea):
        """Parsea una línea del archivo de préstamos"""
        # Validar caracteres
        errores = AnalizadorLexico.validar_linea(linea, numero_linea)
        if errores:
            for error in errores:
                print(f"ERROR: {error}")
            return None
        
        # Dividir por comas
        campos = linea.split(',')
        
        # Validar número de campos (mínimo 5, máximo 6)
        if len(campos) < 5 or len(campos) > 6:
            print(f"ERROR: Línea {numero_linea}: número incorrecto de campos ({len(campos)})")
            return None
        
        try:
            # Extraer campos y retorna cual podria ser el campo no encontrado en el formato de la Ingeniera 
            id_usuario = campos[0].strip()
            nombre_usuario = campos[1].strip()
            id_libro = campos[2].strip()
            titulo_libro = campos[3].strip()
            fecha_prestamo = campos[4].strip()
            fecha_devolucion = campos[5].strip() if len(campos) == 6 else ""
            
            # Validar que id_usuario sea numérico
            if not id_usuario.isdigit():
                print(f"ERROR: Línea {numero_linea}: ID de usuario debe ser numérico")
                return None
            
            # Validar formato de fechas
            if not AnalizadorLexico._validar_fecha(fecha_prestamo):
                print(f"ERROR: Línea {numero_linea}: formato de fecha de préstamo inválido")
                return None
            
            if fecha_devolucion and not AnalizadorLexico._validar_fecha(fecha_devolucion):
                print(f"ERROR: Línea {numero_linea}: formato de fecha de devolución inválido")
                return None
            
            return Prestamo(id_usuario, nombre_usuario, id_libro, titulo_libro, 
                          fecha_prestamo, fecha_devolucion)
            
        except Exception as e:
            print(f"ERROR: Línea {numero_linea}: error al procesar - {str(e)}")
            return None
    
    @staticmethod
    def _validar_fecha(fecha_str):
        """Valida el formato de fecha YYYY-MM-DD"""
        try:
            datetime.strptime(fecha_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

class BibliotecaDigital:
    """Clase principal del sistema de biblioteca digital"""
    
    def __init__(self):
        self.usuarios = {}  # id_usuario -> Usuario
        self.libros = {}    # id_libro -> Libro
        self.prestamos = [] # Lista de préstamos
    
    def cargar_usuarios(self, archivo_usuarios=None):
        """Carga usuarios desde archivo o permite agregar manualmente"""
        if archivo_usuarios and os.path.exists(archivo_usuarios):
            try:
                with open(archivo_usuarios, 'r', encoding='utf-8') as file:
                    for linea in file:
                        linea = linea.strip()
                        if linea and ',' in linea:
                            partes = linea.split(',', 1)
                            if len(partes) == 2:
                                id_usuario, nombre = partes
                                self.usuarios[int(id_usuario)] = Usuario(id_usuario, nombre)
                print(f"Usuarios cargados desde {archivo_usuarios}")
            except Exception as e:
                print(f"Error al cargar usuarios: {e}")
        else:
            print("Funcionalidad de carga manual de usuarios disponible")
    
    def cargar_libros(self, archivo_libros=None):
        """Carga libros desde archivo o permite agregar manualmente"""
        if archivo_libros and os.path.exists(archivo_libros):
            try:
                with open(archivo_libros, 'r', encoding='utf-8') as file:
                    for linea in file:
                        linea = linea.strip()
                        if linea and ',' in linea:
                            partes = linea.split(',', 1)
                            if len(partes) == 2:
                                id_libro, titulo = partes
                                self.libros[id_libro] = Libro(id_libro, titulo)
                print(f"Libros cargados desde {archivo_libros}")
            except Exception as e:
                print(f"Error al cargar libros: {e}")
        else:
            print("Funcionalidad de carga manual de libros disponible")
    
    def cargar_prestamos(self, archivo_prestamos):
        """Carga y procesa el archivo de préstamos"""
        if not os.path.exists(archivo_prestamos):
            print(f"Error: El archivo {archivo_prestamos} no existe")
            return False
        
        try:
            with open(archivo_prestamos, 'r', encoding='utf-8') as file:
                lineas = file.readlines()
                
            prestamos_cargados = 0
            
            for numero_linea, linea in enumerate(lineas, 1):
                linea = linea.strip()
                if not linea:  # Saltar líneas vacías
                    continue
                
                # Saltar header si existe
                if numero_linea == 1 and 'id_usuario' in linea.lower():
                    continue
                
                prestamo = AnalizadorLexico.parsear_linea(linea, numero_linea)
                if prestamo:
                    # Agregar usuario si no existe
                    if prestamo.id_usuario not in self.usuarios:
                        self.usuarios[prestamo.id_usuario] = Usuario(prestamo.id_usuario, prestamo.nombre_usuario)
                    
                    # Agregar libro si no existe
                    if prestamo.id_libro not in self.libros:
                        self.libros[prestamo.id_libro] = Libro(prestamo.id_libro, prestamo.titulo_libro)
                    
                    self.prestamos.append(prestamo)
                    prestamos_cargados += 1
            
            print(f"Préstamos procesados exitosamente: {prestamos_cargados}")
            return True
            
        except Exception as e:
            print(f"Error al procesar archivo: {e}")
            return False
    
    def generar_historial_prestamos(self):
        """Genera reporte del historial de préstamos"""
        if not self.prestamos:
            return "No hay préstamos registrados."
        
        reporte = "\n=== HISTORIAL DE PRÉSTAMOS ===\n"
        reporte += f"{'ID Usuario':<10} {'Nombre':<20} {'ID Libro':<10} {'Título':<30} {'F. Préstamo':<12} {'F. Devolución':<12} {'Estado':<10}\n"
        reporte += "=" * 120 + "\n"
        
        for prestamo in self.prestamos:
            fecha_dev = prestamo.fecha_devolucion.strftime('%Y-%m-%d') if prestamo.fecha_devolucion else "Pendiente"
            estado = "Devuelto" if prestamo.devuelto else "Prestado"
            
            reporte += f"{prestamo.id_usuario:<10} {prestamo.nombre_usuario:<20} {prestamo.id_libro:<10} "
            reporte += f"{prestamo.titulo_libro:<30} {prestamo.fecha_prestamo.strftime('%Y-%m-%d'):<12} {fecha_dev:<12} {estado:<10}\n"
        
        return reporte
    
    def generar_listado_usuarios(self):
        """Genera reporte de usuarios únicos"""
        if not self.usuarios:
            return "No hay usuarios registrados."
        
        reporte = "\n=== LISTADO DE USUARIOS ===\n"
        reporte += f"{'ID Usuario':<10} {'Nombre':<30}\n"
        reporte += "=" * 42 + "\n"
        
        for usuario in self.usuarios.values():
            reporte += f"{usuario.id_usuario:<10} {usuario.nombre_usuario:<30}\n"
        
        return reporte
    
    def generar_listado_libros(self):
        """Genera reporte de libros prestados (sin duplicados)"""
        if not self.libros:
            return "No hay libros registrados."
        
        reporte = "\n=== LISTADO DE LIBROS PRESTADOS ===\n"
        reporte += f"{'ID Libro':<10} {'Título':<50}\n"
        reporte += "=" * 62 + "\n"
        
        for libro in self.libros.values():
            reporte += f"{libro.id_libro:<10} {libro.titulo_libro:<50}\n"
        
        return reporte
    
    def generar_estadisticas(self):
        """Genera estadísticas de préstamos"""
        if not self.prestamos:
            return "No hay datos para generar estadísticas."
        
        # Contar préstamos por libro
        conteo_libros = {}
        for prestamo in self.prestamos:
            if prestamo.id_libro in conteo_libros:
                conteo_libros[prestamo.id_libro] += 1
            else:
                conteo_libros[prestamo.id_libro] = 1
        
        # Contar préstamos por usuario
        conteo_usuarios = {}
        for prestamo in self.prestamos:
            if prestamo.id_usuario in conteo_usuarios:
                conteo_usuarios[prestamo.id_usuario] += 1
            else:
                conteo_usuarios[prestamo.id_usuario] = 1
        
        # Encontrar más prestado y más activo
        libro_mas_prestado = max(conteo_libros, key=conteo_libros.get) # type: ignore
        usuario_mas_activo = max(conteo_usuarios, key=conteo_usuarios.get) # type: ignore
        
        reporte = "\n=== ESTADÍSTICAS DE PRÉSTAMOS ===\n"
        reporte += f"Total de préstamos: {len(self.prestamos)}\n"
        reporte += f"Total de usuarios únicos: {len(self.usuarios)}\n"
        reporte += f"Total de libros diferentes: {len(self.libros)}\n"
        reporte += f"Libro más prestado: {self.libros[libro_mas_prestado].titulo_libro} ({conteo_libros[libro_mas_prestado]} veces)\n"
        reporte += f"Usuario más activo: {self.usuarios[usuario_mas_activo].nombre_usuario} ({conteo_usuarios[usuario_mas_activo]} préstamos)\n"
        
        return reporte
    
    def generar_prestamos_vencidos(self):
        """Genera reporte de préstamos vencidos"""
        prestamos_vencidos = [p for p in self.prestamos if p.esta_vencido()]
        
        if not prestamos_vencidos:
            return "No hay préstamos vencidos."
        
        reporte = "\n=== PRÉSTAMOS VENCIDOS ===\n"
        reporte += f"{'ID Usuario':<10} {'Nombre':<20} {'ID Libro':<10} {'Título':<30} {'F. Vencimiento':<15}\n"
        reporte += "=" * 90 + "\n"
        
        from datetime import timedelta
        for prestamo in prestamos_vencidos:
            # Si tiene fecha de devolución específica, usarla; sino usar 15 días después del préstamo
            fecha_vencimiento = prestamo.fecha_devolucion if prestamo.fecha_devolucion else (prestamo.fecha_prestamo + timedelta(days=15))
            reporte += f"{prestamo.id_usuario:<10} {prestamo.nombre_usuario:<20} {prestamo.id_libro:<10} "
            reporte += f"{prestamo.titulo_libro:<30} {fecha_vencimiento.strftime('%Y-%m-%d'):<15}\n"
        
        return reporte
    
    def exportar_html(self, nombre_archivo="reportes_biblioteca.html"):
        #Formato de HTML improvisado pero reciclado de cuadno hacias paginas web
        """Exporta todos los reportes a formato HTML"""
        html_content = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reportes de Biblioteca Digital</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2 { color: #333; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .section { margin-bottom: 40px; }
                .stats { background-color: #f9f9f9; padding: 15px; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>Sistema de Biblioteca Digital - Reportes</h1>
        """
        
        # Agregar cada reporte como sección HTML
        reportes = [
            ("Historial de Préstamos", self.generar_historial_prestamos()),
            ("Listado de Usuarios", self.generar_listado_usuarios()),
            ("Listado de Libros", self.generar_listado_libros()),
            ("Estadísticas", self.generar_estadisticas()),
            ("Préstamos Vencidos", self.generar_prestamos_vencidos())
        ]
        
        for titulo, contenido in reportes:
            html_content += f'<div class="section"><h2>{titulo}</h2><pre>{contenido}</pre></div>'
        
        html_content += """
        </body>
        </html>
        """
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as file:
                file.write(html_content)
            print(f"Reportes exportados exitosamente a {nombre_archivo}")
            return True
        except Exception as e:
            print(f"Error al exportar HTML: {e}")
            return False

def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("    SISTEMA DE BIBLIOTECA DIGITAL")
    print("="*50)
    print("1. Cargar usuarios")
    #preguntar si tiene que poder ingresar solamente personas y nada mas sin libros y si es asi cual es el formato
    print("2. Cargar libros") 
    #preguntar si se necesitan cargar libros y estos donde se mostrarian si solamente en las estadisticas o donde
    print("3. Cargar registro de préstamos desde archivo")
    #en caso de que no se llenen todos los campos en alguno de los imputs entonces solo salta esa entrada
    print("4. Mostrar historial de préstamos")
    #preguntar a la ingeniera si son todos los libros prestados a lo largo de la historia del programa o solo los actuales
    print("5. Mostrar listado de usuarios únicos")
    print("6. Mostrar listado de libros prestados")
    #libros prestados a lo largo de todo el programa o actualmente
    print("7. Mostrar estadísticas de préstamos")
    print("8. Mostrar préstamos vencidos")
    print("9. Exportar todos los reportes a HTML")
    print("0. Salir")
    print("="*50)

def main():
    """Función principal del programa"""
    biblioteca = BibliotecaDigital()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            archivo = input("Ingrese ruta del archivo de usuarios (Enter para modo manual): ").strip()
            biblioteca.cargar_usuarios(archivo if archivo else None)
            
        elif opcion == "2":
            archivo = input("Ingrese ruta del archivo de libros (Enter para modo manual): ").strip()
            biblioteca.cargar_libros(archivo if archivo else None)
            
        elif opcion == "3":
            archivo = input("Ingrese ruta del archivo de préstamos (.lfa): ").strip()
            biblioteca.cargar_prestamos(archivo)
            
        elif opcion == "4":
            print(biblioteca.generar_historial_prestamos())
            
        elif opcion == "5":
            print(biblioteca.generar_listado_usuarios())
            
        elif opcion == "6":
            print(biblioteca.generar_listado_libros())
            
        elif opcion == "7":
            print(biblioteca.generar_estadisticas())
            
        elif opcion == "8":
            print(biblioteca.generar_prestamos_vencidos())
            
        elif opcion == "9":
            nombre = input("Nombre del archivo HTML (default: reportes_biblioteca.html): ").strip()
            biblioteca.exportar_html(nombre if nombre else "reportes_biblioteca.html")
            
        elif opcion == "0":
            print("¡Gracias por usar el Sistema de Biblioteca Digital!")
            break
            
        else:
            print("Opción no válida. Por favor, seleccione una opción del menú.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()