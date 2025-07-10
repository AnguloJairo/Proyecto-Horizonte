#!/usr/bin/env python3
"""
Proyecto Horizonte - Visualización de Línea de Horizonte
========================================================

Este proyecto permite visualizar la línea de horizonte desde cualquier punto
geográfico utilizando datos de elevación del Ecuador.

Uso:
    python main.py

Requisitos:
    - numpy
    - rasterio
    - pyproj
    - matplotlib
    - tkinter (incluido en Python)
    
Datos necesarios:
    - Archivo .hgt con datos de elevación del Ecuador
    - Se puede descargar de: https://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm

Autor: [Tu nombre]
Fecha: [Fecha actual]
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = {
        'numpy': 'numpy',
        'rasterio': 'rasterio',
        'pyproj': 'pyproj',
        'matplotlib': 'matplotlib'
    }
    
    faltantes = []
    for nombre, paquete in dependencias.items():
        try:
            __import__(paquete)
        except ImportError:
            faltantes.append(paquete)
    
    if faltantes:
        print("Error: Las siguientes dependencias no están instaladas:")
        for dep in faltantes:
            print(f"  - {dep}")
        print("\nInstale las dependencias con:")
        print(f"pip install {' '.join(faltantes)}")
        return False
    
    return True

def crear_estructura_directorio():
    """Crea la estructura de directorios necesaria"""
    if not os.path.exists('datos'):
        os.makedirs('datos')
        print("Directorio 'datos' creado.")
        print("Coloque sus archivos .hgt en el directorio 'datos/'")

def mostrar_informacion_inicial():
    """Muestra información inicial del proyecto"""
    print("=" * 60)
    print("PROYECTO HORIZONTE - Visualización de Línea de Horizonte")
    print("=" * 60)
    print()
    print("Este proyecto permite visualizar la línea de horizonte desde")
    print("cualquier punto geográfico del Ecuador continental.")
    print()
    print("Características:")
    print("- Cálculo de horizonte para una dirección específica")
    print("- Vista panorámica 360°")
    print("- Interfaz gráfica interactiva")
    print("- Soporte para archivos .hgt")
    print()
    print("Coordenadas de ejemplo (Ecuador):")
    print("- Ambato: Lat: -1.2544, Lon: -78.6269")
    print("- Quito: Lat: -0.1807, Lon: -78.4678")
    print("- Guayaquil: Lat: -2.1894, Lon: -79.8890")
    print()
    print("Para mejores resultados, descargue los datos de elevación desde:")
    print("https://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm")
    print("=" * 60)
    print()

def main():
    """Función principal"""
    # Mostrar información inicial
    mostrar_informacion_inicial()
    
    # Verificar dependencias
    if not verificar_dependencias():
        input("Presione Enter para salir...")
        return
    
    # Crear estructura de directorios
    crear_estructura_directorio()
    
    # Verificar si hay archivos .hgt disponibles
    archivos_hgt = []
    if os.path.exists('datos'):
        archivos_hgt = [f for f in os.listdir('datos') if f.endswith('.hgt')]
    
    if not archivos_hgt:
        respuesta = input("No se encontraron archivos .hgt en el directorio 'datos'.\n¿Desea continuar de todos modos? (s/n): ")
        if respuesta.lower() not in ['s', 'si', 'y', 'yes']:
            print("Coloque sus archivos .hgt en el directorio 'datos' y ejecute nuevamente.")
            return
    else:
        print(f"Archivos .hgt encontrados: {len(archivos_hgt)}")
        for archivo in archivos_hgt:
            print(f"  - {archivo}")
        print()
    
    try:
        # Importar y ejecutar la interfaz
        from interfaz import InterfazHorizonte
        
        root = tk.Tk()
        app = InterfazHorizonte(root)
        
        print("Iniciando interfaz gráfica...")
        print("La aplicación se ejecutará en una ventana separada.")
        print("Cierre esta ventana de consola para terminar completamente.")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"Error al importar módulos: {e}")
        print("Verifique que todos los archivos estén en el directorio correcto:")
        print("  - main.py (este archivo)")
        print("  - interfaz.py")
        print("  - horizonte.py")
        input("Presione Enter para salir...")
        
    except Exception as e:
        print(f"Error inesperado: {e}")
        input("Presione Enter para salir...")

if __name__ == "__main__":
    main()