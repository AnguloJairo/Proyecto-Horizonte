import numpy as np
import rasterio
from rasterio.transform import rowcol
from pyproj import Geod

# Inicializar el geodésico
geod = Geod(ellps='WGS84')

def cargar_elevacion(ruta_archivo):
    """
    Carga el archivo .hgt y retorna la matriz de elevaciones y su transformación geográfica.
    
    Args:
        ruta_archivo (str): Ruta al archivo .hgt
        
    Returns:
        tuple: (elevacion, transform) donde elevacion es la matriz de elevaciones
               y transform es la transformación geográfica
    """
    try:
        with rasterio.open(ruta_archivo) as src:
            elevacion = src.read(1)
            transform = src.transform
            bounds = src.bounds
        return elevacion, transform, bounds
    except Exception as e:
        raise Exception(f"Error al cargar el archivo {ruta_archivo}: {str(e)}")

def obtener_elevacion(lat, lon, elevacion, transform):
    """
    Devuelve la elevación para coordenadas específicas de lat/lon.
    
    Args:
        lat (float): Latitud
        lon (float): Longitud
        elevacion (numpy.array): Matriz de elevaciones
        transform (rasterio.transform): Transformación geográfica
        
    Returns:
        float: Elevación en metros
    """
    try:
        fila, columna = rowcol(transform, lon, lat)
        
        # Verificar que los índices estén dentro de los límites
        if (0 <= fila < elevacion.shape[0] and 0 <= columna < elevacion.shape[1]):
            return float(elevacion[fila, columna])
        else:
            raise IndexError("Coordenadas fuera del rango de datos")
    except Exception as e:
        raise Exception(f"Error al obtener elevación: {str(e)}")

def verificar_coordenadas_en_rango(lat, lon, bounds):
    """
    Verifica si las coordenadas están dentro del rango de datos disponibles.
    
    Args:
        lat (float): Latitud
        lon (float): Longitud
        bounds (rasterio.coords.BoundingBox): Límites del dataset
        
    Returns:
        bool: True si las coordenadas están en rango
    """
    return (bounds.left <= lon <= bounds.right and 
            bounds.bottom <= lat <= bounds.top)

def calcular_horizonte(lat, lon, elevacion, transform, bounds, azimut, pasos=1000, distancia_max=100000):
    """
    Calcula la línea de horizonte desde un punto dado y una orientación (azimut).
    
    Args:
        lat (float): Latitud del observador
        lon (float): Longitud del observador
        elevacion (numpy.array): Matriz de elevaciones
        transform (rasterio.transform): Transformación geográfica
        bounds (rasterio.coords.BoundingBox): Límites del dataset
        azimut (float): Azimut en grados (0=Norte, 90=Este, 180=Sur, 270=Oeste)
        pasos (int): Número de puntos a calcular
        distancia_max (float): Distancia máxima en metros
        
    Returns:
        tuple: (distancias, angulos_horizonte) listas con las distancias y ángulos
    """
    # Verificar que el punto del observador esté en rango
    if not verificar_coordenadas_en_rango(lat, lon, bounds):
        raise ValueError("Las coordenadas del observador están fuera del rango de datos disponibles")
    
    # Obtener elevación del observador
    try:
        alt_observador = obtener_elevacion(lat, lon, elevacion, transform)
    except Exception as e:
        raise Exception(f"No se pudo obtener la elevación del observador: {str(e)}")
    
    distancias = np.linspace(100, distancia_max, pasos)  # Empezar desde 100m para evitar divisiones por cero
    angulos_horizonte = []
    max_angulo = -90.0  # Inicializar con ángulo muy bajo
    
    for d in distancias:
        try:
            # Calcular coordenadas del punto a distancia d en dirección azimut
            lon_d, lat_d, _ = geod.fwd(lon, lat, azimut, d)
            
            # Verificar si el punto está dentro del rango de datos
            if not verificar_coordenadas_en_rango(lat_d, lon_d, bounds):
                # Si salimos del rango, mantener el último ángulo válido
                angulos_horizonte.append(max_angulo)
                continue
            
            # Obtener elevación del punto
            alt_d = obtener_elevacion(lat_d, lon_d, elevacion, transform)
            
            # Calcular ángulo de elevación
            angulo = np.degrees(np.arctan2(alt_d - alt_observador, d))
            
            # Actualizar el ángulo máximo (línea de horizonte)
            if angulo > max_angulo:
                max_angulo = angulo
            
            angulos_horizonte.append(max_angulo)
            
        except Exception as e:
            # Si hay error en un punto, mantener el último ángulo válido
            angulos_horizonte.append(max_angulo)
            continue
    
    return distancias, angulos_horizonte

def calcular_horizonte_360(lat, lon, elevacion, transform, bounds, pasos_azimut=360, distancia_max=100000):
    """
    Calcula la línea de horizonte para todos los azimuts (vista panorámica 360°).
    
    Args:
        lat (float): Latitud del observador
        lon (float): Longitud del observador
        elevacion (numpy.array): Matriz de elevaciones
        transform (rasterio.transform): Transformación geográfica
        bounds (rasterio.coords.BoundingBox): Límites del dataset
        pasos_azimut (int): Número de direcciones a calcular
        distancia_max (float): Distancia máxima en metros
        
    Returns:
        tuple: (azimuts, angulos_horizonte) listas con los azimuts y ángulos máximos
    """
    azimuts = np.linspace(0, 360, pasos_azimut, endpoint=False)
    angulos_horizonte_360 = []
    
    for azimut in azimuts:
        try:
            _, angulos = calcular_horizonte(lat, lon, elevacion, transform, bounds, 
                                          azimut, pasos=200, distancia_max=distancia_max)
            # Tomar el ángulo máximo para esta dirección
            angulos_horizonte_360.append(max(angulos))
        except:
            angulos_horizonte_360.append(0)  # Si hay error, usar 0
    
    return azimuts, angulos_horizonte_360