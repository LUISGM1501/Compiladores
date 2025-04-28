#!/bin/bash

#Ejemplos ejecucion:

# Crear entorno y copiar archivos
#./scripts/entorno.sh crear

# Sincronizar cambios de vuelta
#./scripts/entorno.sh sync

# Eliminar entorno
#./scripts/entorno.sh eliminar




# Script para crear/activar entorno virtual y gestionar archivos

# Gestion de permisos
chmod +x scripts/entorno.sh

# Variables
VENV_NAME="mi_entorno"
SRC_DIR="src"
CONTENIDO_DIR="contenidoBruto"

case "$1" in
    "crear")
        echo "Creando entorno virtual..."
        python3 -m venv $VENV_NAME
        
        echo "Activando entorno..."
        source $VENV_NAME/bin/activate
        
        echo "Creando directorio src..."
        mkdir -p $VENV_NAME/$SRC_DIR
        
        echo "Copiando contenido..."
        cp -r $CONTENIDO_DIR/* $VENV_NAME/$SRC_DIR/
        
        echo "Entorno creado y archivos copiados!"
        ;;
    "sync")
        echo "Sincronizando contenido de src a contenidoBruto..."
        cp -r $VENV_NAME/$SRC_DIR/* $CONTENIDO_DIR/
        echo "Sincronización completada!"
        ;;
    "eliminar")
        echo "Eliminando entorno virtual..."
        rm -rf $VENV_NAME
        echo "Entorno eliminado!"
        ;;
    *)
        echo "Uso: $0 {crear|sync|eliminar}"
        exit 1
        ;;
esac