# 🎮 SuperPSX PS4 Game Scraper

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue?logo=github-actions)](https://github.com/features/actions)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Sistema automatizado de scraping para extraer enlaces de descarga de juegos PS4 desde SuperPSX.com con priorización inteligente de servidores y ejecución automática mediante GitHub Actions.

## 🚀 Características Principales

- **🤖 Automatización Completa**: Ejecución automática 2 veces al día via GitHub Actions
- **📊 Procesamiento Masivo**: Procesa 1781+ juegos de PS4 automáticamente
- **🎯 Priorización Inteligente**: VikingFile > Akirabox > 1fichier > MediaFire
- **🛡️ Filtrado Avanzado**: Evita automáticamente servidores problemáticos (filecrypt.cc)
- **📈 Logging Detallado**: Seguimiento completo del progreso y errores
- **💾 Recuperación de Errores**: Capacidad de reanudar desde interrupciones
- **📋 Reportes Automáticos**: Generación de estadísticas y resúmenes

## 📁 Estructura del Proyecto

```
superpsx-scraper/
├── scrape_superpsx.py          # Script principal de scraping
├── requirements.txt            # Dependencias de Python
├── .github/workflows/
│   └── scraper.yml            # Workflow de GitHub Actions
├── ps4_games_list.json        # Lista de juegos (requerido)
├── descargas-ps4.json         # Archivo de salida generado
├── scraper_progress.json      # Progreso del scraping
├── scraping_summary.txt       # Reporte de resumen
└── README.md                  # Esta documentación
```

## 🛠️ Configuración Inicial

### 1. Preparar el Repositorio

1. **Fork o clona este repositorio**
2. **Añade el archivo `ps4_games_list.json`** en la raíz del repositorio:

```json
{
  "timestamp": "2025-07-20",
  "source": "https://www.superpsx.com/ps4-fake-pkgs-game-list/",
  "total_games": 1781,
  "games": [
    {
      "name": "10 Second Ninja X",
      "url": "https://www.superpsx.com/10-second-ninja-x-ps4-fpkg/"
    },
    {
      "name": "13 Sentinels Aegis Rim",
      "url": "https://www.superpsx.com/13-sentinels-aegis-rim-ps4-fpkg/"
    }
    // ... más juegos
  ]
}
```

### 2. Configurar GitHub Actions

1. **Habilitar GitHub Actions** en tu repositorio:
   - Ve a `Settings` → `Actions` → `General`
   - Selecciona "Allow all actions and reusable workflows"

2. **Configurar permisos de escritura**:
   - Ve a `Settings` → `Actions` → `General`
   - En "Workflow permissions", selecciona "Read and write permissions"
   - Marca "Allow GitHub Actions to create and approve pull requests"

3. **El workflow se ejecutará automáticamente**:
   - ⏰ **Automático**: Todos los días a las 6:00 AM y 6:00 PM UTC
   - 🖱️ **Manual**: Ve a `Actions` → `SuperPSX PS4 Game Scraper` → `Run workflow`

## 🎯 Funcionamiento del Scraper

### Proceso de Extracción

1. **Carga de Juegos**: Lee `ps4_games_list.json` con la lista de juegos
2. **Detección de Páginas DLL**: Encuentra botones de descarga que redirigen a páginas DLL
3. **Extracción de Enlaces**: Analiza tablas HTML para extraer enlaces de descarga
4. **Priorización**: Ordena enlaces según preferencia de servidor
5. **Filtrado**: Elimina servidores bloqueados automáticamente
6. **Generación JSON**: Crea `descargas-ps4.json` con formato estandarizado

### Prioridad de Servidores

| Prioridad | Servidor | Razón |
|-----------|----------|-------|
| 🥇 **1** | VikingFile | Velocidad alta, enlaces directos |
| 🥈 **2** | Akirabox | Confiable, buena disponibilidad |
| 🥉 **3** | 1fichier | Estable, ampliamente soportado |
| 4 | MediaFire | Backup confiable |
| 5 | BuzzHeavier | Alternativa adicional |
| ❌ | filecrypt.cc | **BLOQUEADO** - Problemas de acceso |

## 📊 Formato de Salida

El archivo `descargas-ps4.json` generado tiene este formato:

```json
{
  "https://vikingfile.com/f/ecm961G6Oj": {
    "region": "EUR",
    "name": "Assassin's Creed Mirage",
    "version": "1.00",
    "release": null,
    "size": null,
    "min_fw": null,
    "cover_url": null
  },
  "https://akirabox.com/2WVGr61wqGkx/file": {
    "region": "EUR", 
    "name": "Assassin's Creed Mirage",
    "version": "1.07",
    "release": null,
    "size": null,
    "min_fw": null,
    "cover_url": null
  }
}
```

## 🖥️ Uso Local

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/superpsx-scraper.git
cd superpsx-scraper

# Instalar dependencias
pip install -r requirements.txt

# Asegurar que ps4_games_list.json existe
ls -la ps4_games_list.json
```

### Ejecución

```bash
# Ejecutar scraper completo
python scrape_superpsx.py

# Los archivos se generarán automáticamente:
# - descargas-ps4.json (resultado principal)
# - scraper_progress.json (progreso)
# - scraper.log (logs detallados)
```

## 📈 Monitoreo y Logs

### Archivos de Seguimiento

- **`scraper.log`**: Logs detallados de ejecución
- **`scraper_progress.json`**: Progreso actual del scraping
- **`scraping_summary.txt`**: Reporte de resumen con estadísticas

### Ejemplo de Log

```
2025-07-20 11:08:39 - INFO - Starting SuperPSX scraper...
2025-07-20 11:08:40 - INFO - Found 1781 games to process
2025-07-20 11:08:41 - INFO - Processing: 10 Second Ninja X
2025-07-20 11:08:42 - INFO - Found DLL page: https://www.superpsx.com/dll-10snxps4/
2025-07-20 11:08:43 - INFO - Successfully processed 10 Second Ninja X: 2 links found
2025-07-20 11:08:44 - INFO - Progress: 10/1781 (0.6%)
```

## 🔧 Troubleshooting

### Problemas Comunes

#### ❌ "ps4_games_list.json not found"
**Solución**: Asegúrate de que el archivo JSON esté en la raíz del repositorio.

```bash
# Verificar archivo
ls -la ps4_games_list.json

# Verificar formato JSON
jq '.games | length' ps4_games_list.json
```

#### ❌ "No DLL page found"
**Causa**: Algunos juegos pueden no tener páginas DLL o la estructura cambió.
**Solución**: El scraper continúa automáticamente con el siguiente juego.

#### ❌ "Rate limiting errors"
**Causa**: Demasiadas requests muy rápidas.
**Solución**: El scraper incluye delays automáticos de 1 segundo entre requests.

#### ❌ GitHub Actions falla
**Verificar**:
1. Permisos de escritura habilitados
2. Archivo `ps4_games_list.json` presente
3. Sintaxis correcta en `scraper.yml`

### Logs de Debugging

```bash
# Ver últimas 50 líneas del log
tail -50 scraper.log

# Buscar errores específicos
grep -i "error" scraper.log

# Verificar progreso
cat scraper_progress.json | jq '.'
```

## ⚙️ Configuración Avanzada

### Modificar Frecuencia de Ejecución

Edita `.github/workflows/scraper.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Cada 6 horas
  - cron: '0 0 * * 0'    # Solo domingos a medianoche
```

### Añadir Nuevos Servidores

En `scrape_superpsx.py`, modifica:

```python
self.server_priority = {
    'vikingfile.com': 1,
    'akirabox.com': 2,
    '1fichier.com': 3,
    'tu-nuevo-servidor.com': 4  # Añadir aquí
}
```

### Filtrar Servidores Adicionales

```python
self.blocked_servers = [
    'filecrypt.cc',
    'servidor-problematico.com'  # Añadir aquí
]
```

## 📊 Estadísticas del Proyecto

- **🎮 Juegos Procesados**: 1781+ juegos de PS4
- **🔗 Enlaces Extraídos**: Miles de enlaces de descarga
- **🏆 Servidores Priorizados**: 5+ servidores confiables
- **⚡ Velocidad**: ~1 juego por segundo (con rate limiting)
- **🔄 Automatización**: 2 ejecuciones diarias automáticas

## 🤝 Contribuciones

### Cómo Contribuir

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crea** un Pull Request

### Áreas de Mejora

- 🔍 **Detección de nuevos servidores**
- 📊 **Métricas adicionales de calidad**
- 🛡️ **Mejor manejo de anti-bot**
- 🎨 **Dashboard web para visualización**
- 📱 **Notificaciones móviles**

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Disclaimer

Este proyecto es solo para fines educativos y de investigación. Los usuarios son responsables de cumplir con las leyes de derechos de autor y términos de servicio de los sitios web scrapeados.

## 🔗 Enlaces Útiles

- [SuperPSX.com](https://www.superpsx.com/) - Sitio web fuente
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://requests.readthedocs.io/)

---

**🤖 Desarrollado con ❤️ para la comunidad PS4**

*Última actualización: Julio 2025*
