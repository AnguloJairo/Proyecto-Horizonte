import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os
from horizonte import cargar_elevacion, calcular_horizonte, calcular_horizonte_360

class InterfazHorizonte:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Horizonte - Visualización de Línea de Horizonte")
        self.root.geometry("1000x800")
        
        # Variables para almacenar los datos
        self.elevacion = None
        self.transform = None
        self.bounds = None
        self.ruta_archivo = None
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Intentar cargar un archivo por defecto
        self.cargar_archivo_por_defecto()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Sección de archivo
        ttk.Label(main_frame, text="Archivo de elevación:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        
        self.archivo_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.archivo_var, state="readonly").grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(file_frame, text="Seleccionar archivo", command=self.seleccionar_archivo).grid(row=0, column=1)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Sección de parámetros
        ttk.Label(main_frame, text="Parámetros del observador:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 5))
        
        params_frame = ttk.Frame(main_frame)
        params_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Latitud
        ttk.Label(params_frame, text="Latitud:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_lat = ttk.Entry(params_frame, width=15)
        self.entry_lat.grid(row=0, column=1, padx=5, pady=5)
        self.entry_lat.insert(0, "-1.2544")  # Ambato por defecto
        
        # Longitud
        ttk.Label(params_frame, text="Longitud:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_lon = ttk.Entry(params_frame, width=15)
        self.entry_lon.grid(row=0, column=3, padx=5, pady=5)
        self.entry_lon.insert(0, "-78.6269")  # Ambato por defecto
        
        # Azimut
        ttk.Label(params_frame, text="Azimut (°):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_az = ttk.Entry(params_frame, width=15)
        self.entry_az.grid(row=1, column=1, padx=5, pady=5)
        self.entry_az.insert(0, "0")  # Norte por defecto
        
        # Distancia máxima
        ttk.Label(params_frame, text="Distancia máx (km):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_dist = ttk.Entry(params_frame, width=15)
        self.entry_dist.grid(row=1, column=3, padx=5, pady=5)
        self.entry_dist.insert(0, "100")  # 100 km por defecto
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Calcular Horizonte", command=self.calcular_horizonte).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Vista 360°", command=self.calcular_horizonte_360).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar Gráfico", command=self.limpiar_grafico).pack(side=tk.LEFT, padx=5)
        
        # Área de gráfico
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, main_frame)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Listo - Seleccione un archivo .hgt para comenzar")
        ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def cargar_archivo_por_defecto(self):
        """Intenta cargar un archivo por defecto si existe"""
        rutas_posibles = [
            "datos/S01W079.hgt",
            "S01W079.hgt",
            "./datos/S01W079.hgt"
        ]
        
        for ruta in rutas_posibles:
            if os.path.exists(ruta):
                self.cargar_archivo(ruta)
                break
    
    def seleccionar_archivo(self):
        """Permite al usuario seleccionar un archivo .hgt"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de elevación",
            filetypes=[("Archivos HGT", "*.hgt"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.cargar_archivo(filename)
    
    def cargar_archivo(self, ruta):
        """Carga el archivo de elevación seleccionado"""
        try:
            self.status_var.set("Cargando archivo...")
            self.root.update()
            
            self.elevacion, self.transform, self.bounds = cargar_elevacion(ruta)
            self.ruta_archivo = ruta
            self.archivo_var.set(os.path.basename(ruta))
            
            self.status_var.set(f"Archivo cargado: {os.path.basename(ruta)} - Dimensiones: {self.elevacion.shape}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo:\n{str(e)}")
            self.status_var.set("Error al cargar archivo")
    
    def validar_parametros(self):
        """Valida los parámetros ingresados por el usuario"""
        if self.elevacion is None:
            raise ValueError("Debe cargar un archivo de elevación primero")
        
        try:
            lat = float(self.entry_lat.get())
            lon = float(self.entry_lon.get())
            azimut = float(self.entry_az.get())
            dist_max = float(self.entry_dist.get()) * 1000  # convertir a metros
            
            if not (-90 <= lat <= 90):
                raise ValueError("La latitud debe estar entre -90 y 90 grados")
            if not (-180 <= lon <= 180):
                raise ValueError("La longitud debe estar entre -180 y 180 grados")
            if not (0 <= azimut <= 360):
                raise ValueError("El azimut debe estar entre 0 y 360 grados")
            if dist_max <= 0:
                raise ValueError("La distancia máxima debe ser mayor que 0")
            
            return lat, lon, azimut, dist_max
            
        except ValueError as e:
            if "could not convert" in str(e):
                raise ValueError("Todos los parámetros deben ser números válidos")
            else:
                raise e
    
    def calcular_horizonte(self):
        """Calcula y dibuja la línea de horizonte para una dirección específica"""
        try:
            lat, lon, azimut, dist_max = self.validar_parametros()
            
            self.status_var.set("Calculando horizonte...")
            self.root.update()
            
            # Calcular horizonte
            distancias, angulos = calcular_horizonte(
                lat, lon, self.elevacion, self.transform, self.bounds, 
                azimut, pasos=1000, distancia_max=dist_max
            )
            
            # Dibujar gráfico
            self.ax.clear()
            self.ax.plot(np.array(distancias)/1000, angulos, 'b-', linewidth=2, label=f'Azimut {azimut}°')
            self.ax.set_xlabel('Distancia (km)')
            self.ax.set_ylabel('Ángulo de elevación (°)')
            self.ax.set_title(f'Línea de Horizonte - Lat: {lat:.4f}, Lon: {lon:.4f}, Azimut: {azimut}°')
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            
            # Añadir línea horizontal en 0°
            self.ax.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Horizonte teórico')
            
            self.canvas.draw()
            self.status_var.set(f"Horizonte calculado - Ángulo máximo: {max(angulos):.2f}°")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular el horizonte:\n{str(e)}")
            self.status_var.set("Error en el cálculo")
    
    def calcular_horizonte_360(self):
        """Calcula y dibuja la línea de horizonte para todas las direcciones (360°)"""
        try:
            lat, lon, azimut, dist_max = self.validar_parametros()
            
            self.status_var.set("Calculando horizonte 360°...")
            self.root.update()
            
            # Calcular horizonte 360°
            azimuts, angulos = calcular_horizonte_360(
                lat, lon, self.elevacion, self.transform, self.bounds, 
                pasos_azimut=360, distancia_max=dist_max
            )
            
            # Dibujar gráfico polar
            self.ax.clear()
            
            # Convertir a radianes para el gráfico polar
            theta = np.radians(azimuts)
            
            # Crear gráfico polar
            self.ax = plt.subplot(111, projection='polar')
            self.ax.plot(theta, angulos, 'b-', linewidth=2)
            self.ax.fill(theta, angulos, alpha=0.3)
            self.ax.set_theta_zero_location('N')
            self.ax.set_theta_direction(-1)
            self.ax.set_title(f'Horizonte 360° - Lat: {lat:.4f}, Lon: {lon:.4f}')
            self.ax.set_ylim(0, max(angulos) * 1.1)
            
            # Actualizar el canvas
            self.canvas.figure.clear()
            self.ax = self.canvas.figure.add_subplot(111, projection='polar')
            self.ax.plot(theta, angulos, 'b-', linewidth=2)
            self.ax.fill(theta, angulos, alpha=0.3)
            self.ax.set_theta_zero_location('N')
            self.ax.set_theta_direction(-1)
            self.ax.set_title(f'Horizonte 360° - Lat: {lat:.4f}, Lon: {lon:.4f}')
            self.ax.set_ylim(0, max(angulos) * 1.1)
            
            self.canvas.draw()
            self.status_var.set(f"Horizonte 360° calculado - Ángulo máximo: {max(angulos):.2f}°")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al calcular el horizonte 360°:\n{str(e)}")
            self.status_var.set("Error en el cálculo")
    
    def limpiar_grafico(self):
        """Limpia el gráfico actual"""
        self.ax.clear()
        self.ax.set_xlabel('Distancia (km)')
        self.ax.set_ylabel('Ángulo de elevación (°)')
        self.ax.set_title('Línea de Horizonte')
        self.ax.grid(True, alpha=0.3)
        
        # Restaurar gráfico normal si estaba en modo polar
        if hasattr(self.ax, 'projection') and self.ax.projection.name == 'polar':
            self.canvas.figure.clear()
            self.ax = self.canvas.figure.add_subplot(111)
            self.ax.set_xlabel('Distancia (km)')
            self.ax.set_ylabel('Ángulo de elevación (°)')
            self.ax.set_title('Línea de Horizonte')
            self.ax.grid(True, alpha=0.3)
        
        self.canvas.draw()
        self.status_var.set("Gráfico limpiado")

def main():
    root = tk.Tk()
    app = InterfazHorizonte(root)
    root.mainloop()

if __name__ == "__main__":
    main()