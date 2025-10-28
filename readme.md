# 🧊 Control de Aires Acondicionados (ESP32 + Django)

Sistema IoT para la **gestión remota de aires acondicionados** mediante **ESP32**.
Cada dispositivo se comunica con el servidor Django a través de **API REST**, reporta su estado (`encendido/apagado`) y recibe **comandos de control** (incluyendo códigos IR personalizados).

## Estructura del proyecto

accontrol/
├─ manage.py
├─ requirements.txt
├─ README.md
├─ accontrol/
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
└─ devices/
   ├─ models.py
   ├─ views.py
   ├─ urls.py
   ├─ admin.py
   └─ templates/
      └─ devices/
         └─ dashboard.html

## 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/accontrol.git
cd accontrol
```

## 2. Crear entorno virtual

```bash
python -m venv .venv
# Activar entorno
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Migrar las bases de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Crear un superusuario

```bash
python manage.py createsuperuser
```

## 6. Ejecutar el servidor

```bash
python manage.py runserver
```

## Rutas Principales

| Ruta            | Descripción                                                                          |
| --------------- | ------------------------------------------------------------------------------------- |
| /               | Dashboard con tarjetas de control para los dispositivos de aire acondicionado (esp32) |
| /admin/         | Panel administrativo de Django                                                        |
| /api/heartbeat/ | Recibe estado de los ESP32                                                            |
| /api/command/   | Envía el comando IR deseado al ESP32                                                 |
