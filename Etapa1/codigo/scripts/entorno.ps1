# Script para crear/activar entorno virtual y gestionar archivos

# Ejemplos ejecucion:

# Crear entorno y copiar archivos
#.\scrips\entorno.ps1 -accion crear

# Sincronizar cambios de vuelta
#.\scripts\entorno.ps1 -accion sync

# Eliminar entorno
#.\scripts\entorno.ps1 -accion eliminar


param(
    [string]$accion
)

# Variables
$venvName = "mi_entorno"
$srcDir = "src"
$contenidoDir = "contenidoBruto"

switch ($accion) {
    "crear" {
        Write-Host "Creando entorno virtual..."
        python -m venv $venvName
        
        Write-Host "Activando entorno..."
        .\$venvName\Scripts\activate
        
        Write-Host "Creando directorio src..."
        New-Item -Path "$venvName\$srcDir" -ItemType Directory -Force
        
        Write-Host "Copiando contenido..."
        Copy-Item -Path "$contenidoDir\*" -Destination "$venvName\$srcDir\" -Recurse
        
        Write-Host "Entorno creado y archivos copiados!"
    }
    "sync" {
        Write-Host "Sincronizando contenido de src a contenidoBruto..."
        Copy-Item -Path "$venvName\$srcDir\*" -Destination "$contenidoDir\" -Recurse -Force
        Write-Host "Sincronización completada!"
    }
    "eliminar" {
        Write-Host "Eliminando entorno virtual..."
        Remove-Item -Path $venvName -Recurse -Force
        Write-Host "Entorno eliminado!"
    }
    default {
        Write-Host "Uso: .\entorno.ps1 -accion {crear|sync|eliminar}"
        exit 1
    }
}