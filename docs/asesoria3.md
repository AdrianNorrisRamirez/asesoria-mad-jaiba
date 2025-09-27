
# Guía 1: Configuración Inicial - Credenciales de AWS y Verificación del Entorno

Este primer capítulo cubre los pasos fundamentales para configurar un entorno de desarrollo seguro y verificar los prerrequisitos de hardware en Windows para tecnologías de virtualización.

## 1. Verificación de la Tecnología de Virtualización en Windows

Un obstáculo común para usar herramientas de desarrollo modernas como Docker o WSL (Windows Subsystem for Linux) es la falta de soporte de virtualización en el hardware o que esta no se encuentre activada. La virtualización permite que tu sistema operativo ejecute otros sistemas operativos de forma aislada, lo cual es la base de la contenedorización con Docker.

**¿Por qué es importante?**
La virtualización de hardware (como Intel VT-x o AMD-V) es crucial porque permite una gestión eficiente y segura de las máquinas virtuales y contenedores, ofreciendo un rendimiento casi nativo. Sin ella, Docker no puede funcionar correctamente en Windows.

**Pasos para verificar la compatibilidad desde la línea de comandos (CMD):**

1.  Abre el Símbolo del sistema. Puedes hacerlo buscando `cmd` en el menú de inicio.
2.  Ejecuta el siguiente comando para obtener información detallada de tu sistema:
    ```cmd
    systeminfo.exe
    ```
3.  Espera a que el comando cargue toda la información. Al final de la salida, busca la sección **"Requisitos de Hyper-V"**. Verás algo similar a esto:

    ```
    Requisitos de Hyper-V:      Compatibilidad con la virtualización en el firmware: Sí
                               Traducción de direcciones de segundo nivel: Sí
                               Extensiones de modo de monitor de VM: Sí
                               Protección de datos ejecutable disponible: Sí
    ```

*   **`Compatibilidad con la virtualización en el firmware: Sí`**: Esta es la línea más importante. Si dice "Sí", tu procesador y hardware soportan la virtualización. Si dice "No", tu equipo no es compatible.

**¿Qué hacer si dice "Sí" pero Docker sigue sin funcionar?**

Es muy probable que la tecnología de virtualización esté desactivada en la BIOS/UEFI de tu computadora.

**Cómo activar la virtualización en la BIOS/UEFI:**

1.  **Reinicia tu computadora.**
2.  Durante el arranque, presiona la tecla para entrar a la configuración de la BIOS/UEFI. Esta tecla varía según el fabricante (comúnmente son `F2`, `F10`, `F12` o `DEL`).
3.  Busca una pestaña o sección llamada "Advanced", "Configuration" o "Security".
4.  Dentro de esa sección, busca una opción con un nombre como:
    *   `Intel(R) Virtualization Technology`
    *   `Intel VT-x`
    *   `AMD-V`
    *   `SVM Mode` (en procesadores AMD)
5.  Actívala (cámbiala a `Enabled`).
6.  Guarda los cambios y sal de la BIOS/UEFI. La computadora se reiniciará.

Una vez completado, tu sistema estará listo para herramientas como Docker. En el caso de esta asesoría, al no ser posible realizar este paso, se optó por un workaround utilizando servicios en la nube.

## 2. Creación de un Usuario Programático con AWS IAM

Para interactuar con los servicios de AWS de forma segura, nunca se deben usar las credenciales del usuario raíz. En su lugar, se crea un usuario con permisos específicos a través del servicio **Identity and Access Management (IAM)**.

**Pasos para la creación del usuario:**

1.  **Acceso a IAM**: En la consola de AWS, navega al servicio IAM.
2.  **Creación de Usuario**:
    *   Ve a la sección "Users" (Usuarios) y haz clic en "Add users" (Añadir usuarios).
    *   **Nombre de usuario**: Se asignó el nombre `asesoria`.
    *   **Tipo de acceso**: Se seleccionó únicamente **"Access key - Programmatic access"** (Clave de acceso - Acceso programático). Esto genera un `Access Key ID` y un `Secret Access Key`, que son las credenciales que usará la AWS CLI. Se dejó desmarcada la opción de acceso a la consola de AWS, ya que este usuario solo interactuará a través de la línea de comandos.
3.  **Asignación de Permisos**:
    *   Para esta sesión educativa, se asignaron permisos de administrador para simplificar las operaciones. Se seleccionó la política **`AdministratorAccess`**.
    *   **Nota importante de seguridad**: En un entorno de producción, se debe seguir el **principio de menor privilegio**, otorgando únicamente los permisos estrictamente necesarios para las tareas que el usuario debe realizar.
4.  **Revisión y Creación**: Una vez creado el usuario, AWS muestra el **`Access Key ID`** y el **`Secret Access Key`**. Es crucial guardar estas credenciales en un lugar seguro, ya que el Secret Access Key no se puede volver a ver. Generalmente, se descarga el archivo `.csv` que las contiene.

## 3. Configuración de la AWS CLI

Con las credenciales del usuario `asesoria`, el siguiente paso es configurar la AWS Command Line Interface (CLI) en la máquina local.

1.  Abre una terminal o CMD.
2.  Ejecuta el comando de configuración:
    ```bash
    aws configure
    ```
3.  La CLI te pedirá interactivamente la siguiente información:
    *   **`AWS Access Key ID`**: Pega la clave obtenida del usuario IAM.
    *   **`AWS Secret Access Key`**: Pega la clave secreta.
    *   **`Default region name`**: Especifica la región de AWS donde trabajarás (ej. `us-west-1`).
    *   **`Default output format`**: Puedes dejarlo en blanco o escribir `json`.

Este proceso guarda tus credenciales de forma segura en un archivo dentro de tu directorio de usuario (en `~/.aws/credentials`), permitiendo que todas las futuras llamadas a la AWS CLI se autentiquen automáticamente.




# Guía 2: Primer Despliegue - El Reto de las Dependencias en Windows

En este capítulo se detalla el primer intento de despliegue de una aplicación Flask utilizando el Serverless Framework. Este proceso fue diseñado para ilustrar un problema fundamental al trabajar con dependencias de Python en un entorno Windows sin Docker.

## 1. La Aplicación Flask Básica

Para comenzar, se creó una aplicación web mínima con Flask, que servirá como base para el despliegue.

**`app.py`**
```python
    from flask import Flask

    app = Flask(__name__)

    # Se define una única ruta raíz
    @app.route('/')
    def hello_world():
        return "Bienvenido al servidor de Flask"
```
Esta aplicación simplemente responde con un mensaje de bienvenida cuando se accede a su ruta principal.

## 2. Configuración de Serverless Framework v3

El despliegue se orquestó con el Serverless Framework. La versión 3 fue elegida específicamente, ya que versiones más recientes (como la v4) introducen un sistema de autenticación y un flujo de trabajo diferentes que no eran necesarios para este ejercicio.

El archivo de configuración inicial fue el siguiente:

**`serverless.yml`**
```yaml
service: mi-api-flask

frameworkVersion: '3'

provider:
  name: aws
  runtime: python3.11
  region: us-east-1

functions:
  api:
    handler: wsgi_handler.handler # El handler que conectará con Flask
    events:
      - httpApi: '*'

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: false # La configuración clave de este experimento
```

## 3. El Plugin `serverless-python-requirements`

Para gestionar las dependencias de Python (en este caso, Flask), se utilizó el popular plugin `serverless-python-requirements`. Este plugin automatiza el proceso de instalar las librerías listadas en un archivo `requirements.txt` y empaquetarlas junto con el código de la aplicación.

La configuración clave aquí fue **`dockerizePip: false`**.
*   Cuando `dockerizePip` es `true` (valor por defecto), el plugin utiliza un contenedor de Docker que simula el entorno de Amazon Linux para instalar las dependencias. Esto garantiza que los binarios compilados sean 100% compatibles con AWS Lambda.
*   Al establecerlo en `false`, le indicamos al plugin que utilice el entorno de Python y `pip` de la máquina local (en este caso, Windows) para instalar las dependencias.

## 4. El Problema: Incompatibilidad de Binarios entre Windows y Linux

Se ejecutó el comando `serverless deploy`. El framework procedió a:
1.  Leer `requirements.txt`.
2.  Instalar Flask usando el `pip` de Windows.
3.  Empaquetar el código de la aplicación y las dependencias instaladas en un archivo `.zip`.
4.  Subir el `.zip` a AWS S3 y crear la función Lambda, el rol de IAM y el API Gateway correspondientes.

El despliegue finalizó **sin errores aparentes**. Sin embargo, al invocar la URL del API Gateway, la función Lambda falló, mostrando en los logs de CloudWatch un error similar a:

`[ERROR] Runtime.ImportModuleError: Unable to import module 'wsgi_handler': No module named 'flask'`

**¿Por qué ocurrió esto?**

Este fue el resultado esperado y el propósito del ejercicio:

*   **Dependencias y Compilación**: Muchas librerías de Python no son "Python puro". Contienen código escrito en C que necesita ser compilado en binarios específicos para la arquitectura y el sistema operativo donde se van a ejecutar.
*   **El Conflicto de Sistemas Operativos**:
    *   Al correr `pip install` en **Windows**, se descargan e instalan paquetes que incluyen binarios compilados para Windows (archivos `.pyd`, que son como los `.dll`).
    *   El entorno de ejecución de **AWS Lambda**, sin embargo, está basado en **Amazon Linux**. Este entorno espera binarios compilados para Linux (archivos `.so`).
*   **El Resultado**: Aunque la carpeta de `flask` estaba presente en el paquete `.zip`, el entorno de Lambda no pudo importarla correctamente porque los archivos compilados eran incompatibles.

**Conclusión del Experimento**

Este primer despliegue demostró de manera práctica que para crear paquetes de despliegue de Lambda que incluyan dependencias con código compilado, es indispensable construirlos en un entorno compatible con Linux. Como el uso de Docker no era una opción, el siguiente paso fue buscar un workaround utilizando una máquina virtual en la nube.





# Guía 3: Workaround - Creando un Entorno de Build con Amazon EC2

Dado que el entorno local (Windows sin virtualización) no era adecuado para construir un paquete de despliegue compatible con Lambda, la solución fue utilizar una máquina virtual en la nube que simulara el entorno de destino. Amazon EC2 (Elastic Compute Cloud) es el servicio perfecto para esta tarea.

## 1. Justificación del Uso de EC2

Amazon EC2 permite lanzar servidores virtuales (llamados "instancias") con una variedad de sistemas operativos. Al lanzar una instancia con **Amazon Linux**, obtenemos un entorno casi idéntico al que utilizan las funciones de AWS Lambda. Esto nos garantiza que cualquier dependencia de Python que compilemos en esta instancia será 100% compatible.

## 2. Lanzamiento de la Instancia EC2

Se siguieron los siguientes pasos para crear la máquina virtual que servirá como nuestro "entorno de build":

1.  **Navegar a EC2**: Desde la consola de AWS, se accedió al servicio EC2.
2.  **Lanzar Instancia**:
    *   **AMI (Amazon Machine Image)**: Se seleccionó **Amazon Linux 2**, ya que es la base para muchos runtimes de Lambda.
    *   **Tipo de Instancia**: Se eligió `t3.micro`. Este tipo de instancia es elegible para la capa gratuita de AWS, por lo que no genera costos si se mantiene dentro de los límites.
    *   **Par de Claves (Key Pair)**: Se creó un nuevo par de claves con el nombre `lambda-builder-keys`. Al crearlo, se descargó automáticamente el archivo de clave privada (`lambda-builder-keys.pem`). Este archivo es esencial para conectarse a la instancia de forma segura a través de SSH.
3.  **Configuración del Grupo de Seguridad (Security Group)**

Un Grupo de Seguridad actúa como un firewall virtual para la instancia, controlando el tráfico entrante y saliente.

*   Se creó un nuevo grupo de seguridad.
*   **Regla de Entrada (Inbound Rule)**: Para poder conectarnos, se añadió una regla para permitir el tráfico SSH (protocolo TCP, puerto 22).
*   **Fuente (Source)**: Para la finalidad de este ejercicio práctico, se configuró la fuente como **`Anywhere` (`0.0.0.0/0`)**.

> **⚠️ Advertencia de Seguridad Importante**:
> Configurar el acceso SSH desde `Anywhere` es una práctica **altamente insegura** y solo debe usarse para pruebas temporales. Esto expone el puerto 22 de tu instancia a todo internet, haciéndola vulnerable a ataques de fuerza bruta.

## 3. Mejores Prácticas de Seguridad para el Acceso SSH

En un entorno real, el acceso debe ser restringido. A continuación se describe un método mucho más seguro.

**Restringir por IP:**
La opción más simple es cambiar la fuente de la regla de `Anywhere` a `My IP`. AWS detectará automáticamente tu dirección IP pública actual y la usará, pero esto es inconveniente si tu IP cambia con frecuencia.

**Una Solución Avanzada y Segura: Tailscale**

Para un acceso robusto y seguro desde cualquier lugar, se pueden utilizar herramientas como **Tailscale**.

*   **¿Qué es Tailscale?** Tailscale es un servicio que crea una red privada virtual (VPN) segura de tipo "malla" (mesh) entre tus dispositivos (computadora, servidor en la nube, teléfono, etc.) utilizando el protocolo WireGuard.
*   **¿Cómo funciona?**
    1.  Instalas el cliente de Tailscale en tu computadora local y en la instancia EC2.
    2.  Ambos dispositivos se autentican con tu cuenta y se unen a tu red privada.
    3.  Tailscale asigna a cada dispositivo una dirección IP privada y estable dentro del rango `100.x.x.x`.
    4.  En el Grupo de Seguridad de AWS, en lugar de permitir el acceso desde tu IP pública, **permites el acceso SSH únicamente desde la dirección IP de Tailscale de tu computadora local**.
*   **Ventajas**:
    *   **Seguridad Máxima**: El puerto 22 ya no está expuesto a internet, solo a tu red privada y cifrada.
    *   **IP Estable**: Puedes conectarte desde cualquier lugar del mundo, ya que tu IP de Tailscale no cambia.

## 4. Conexión a la Instancia EC2 vía SSH

Una vez que la instancia estaba en estado "running", se utilizó el archivo `.pem` descargado para establecer una conexión SSH desde la terminal de Windows.

1.  Se abrió una terminal (CMD o PowerShell).
2.  Se utilizó el siguiente comando, reemplazando los placeholders:

    ```bash
    ssh -i "C:\ruta\completa\hacia\lambda-builder-keys.pem" ec2-user@<IP_PUBLICA_DE_LA_INSTANCIA>
    ```

    *   `-i`: Especifica el archivo de identidad (la clave privada `.pem`).
    *   `ec2-user`: Es el nombre de usuario por defecto para las instancias de Amazon Linux.
    *   `<IP_PUBLICA_DE_LA_INSTANCIA>`: La dirección IPv4 pública de la instancia, visible en la consola de EC2.

Al conectarse exitosamente, se obtuvo acceso a una terminal de Linux directamente en la nube, lista para ser utilizada como nuestro entorno de compilación.


# Guía 4: Construyendo una Lambda Layer en el Entorno EC2

Con el acceso a la instancia EC2 de Amazon Linux, el siguiente paso es utilizar este entorno para construir una capa de Lambda (Lambda Layer) que contendrá nuestras dependencias de Python compiladas de forma compatible.

## 1. ¿Qué es una Lambda Layer?

Una **Lambda Layer** es un archivo `.zip` que puede contener librerías, un runtime personalizado u otras dependencias. El principal beneficio de usar Layers es que permite mantener el código de la función Lambda separado de sus dependencias. Esto resulta en:
*   **Paquetes de despliegue más pequeños**: El código de tu función es más ligero y rápido de subir.
*   **Reutilización de código**: Una misma Layer puede ser utilizada por múltiples funciones Lambda.
*   **Gestión simplificada de dependencias**: Puedes actualizar una librería en la Layer sin tener que volver a desplegar el código de todas las funciones que la usan.

## 2. Preparación del Entorno en la Instancia EC2

Antes de instalar las dependencias, es necesario instalar Python 3.11 en la instancia de Amazon Linux 2, ya que no viene preinstalado. Este proceso implica compilar Python desde su código fuente.

1.  **Instalar herramientas de desarrollo**: El primer paso es instalar el grupo de paquetes `Development Tools`, que incluye compiladores como `gcc` y otras utilidades necesarias para construir software.
    ```bash
    sudo yum groupinstall "Development Tools" -y
    sudo yum install gcc openssl-devel bzip2-devel libffi-devel -y
    ```

2.  **Descargar el código fuente de Python**: Se utilizó `curl` para descargar el archivo comprimido (`.tgz`) con el código fuente de Python 3.11 desde el sitio web oficial.
    *   **`curl`**: Es una herramienta de línea de comandos para transferir datos con URLs.
    ```bash
    # Navegamos a un directorio temporal para la compilación
    cd /usr/src
    # Descargamos el código fuente
    sudo curl -O https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz
    ```

3.  **Descomprimir el archivo**: Se usó el comando `tar` para extraer el contenido del archivo descargado.
    *   **`tar`**: Es una utilidad para manipular archivos archivados.
    ```bash
    sudo tar xzf Python-3.11.6.tgz
    cd Python-3.11.6
    ```

4.  **Configurar y compilar Python**:
    *   **`./configure`**: Este script prepara el código fuente para la compilación en el sistema actual, verificando que todas las dependencias necesarias estén presentes. La opción `--enable-optimizations` mejora el rendimiento del binario final.
    *   **`make altinstall`**: Este comando inicia el proceso de compilación. Se utiliza `altinstall` en lugar de `make install` por una razón muy importante: para evitar sobrescribir el binario de Python por defecto del sistema (`/usr/bin/python`). `altinstall` instala el ejecutable como `python3.11`, permitiendo que ambas versiones coexistan sin conflictos.

    ```bash
    sudo ./configure --enable-optimizations
    sudo make altinstall
    ```
    Este proceso puede tardar varios minutos. Al finalizar, `python3.11` y `pip3.11` estarán disponibles en el sistema.

## 3. Creación y Empaquetado de la Layer

1.  **Crear la estructura de directorios**: AWS Lambda espera que las dependencias de Python se encuentren dentro de una carpeta llamada `python` en la raíz del archivo `.zip` de la Layer.
    ```bash
    # Volvemos al directorio home del usuario
    cd /home/ec2-user
    # Creamos la estructura requerida
    mkdir -p mi-layer-flask/python
    ```
2.  **Instalar las dependencias**: Usando `pip3.11`, se instalan las librerías necesarias directamente en el directorio `python`. El flag `-t` (target) especifica la ubicación de la instalación.
    ```bash
    python3.11 -m pip install flask serverless-wsgi -t mi-layer-flask/python/
    ```
3.  **Uso de requirements.txt**: Se intentó utilizar un archivo `requirements.txt` para especificar las dependencias de manera más organizada. Sin embargo, al intentar editar el archivo con `nano`, se encontró que el atajo `Ctrl+V` para pegar no funcionaba correctamente en la terminal. Como solución alternativa, se utilizó el método de entrada de texto con `EOF<>` para introducir todo el contenido del archivo directamente desde la terminal:
    ```bash
    cat > requirements.txt << EOF
    flask
    serverless-wsgi
    EOF
    ```
3.  **Empaquetar la Layer**: Se navega al directorio `mi-layer-flask` y se crea un archivo `.zip` que contiene la carpeta `python` y todo su contenido.
    ```bash
    cd mi-layer-flask
    zip -r layer-flask.zip python
    ```
    Ahora tenemos un archivo `layer-flask.zip` listo para ser publicado.

## 4. Publicación de la Lambda Layer en AWS

Finalmente, se utiliza la AWS CLI (que también debe ser configurada en la instancia EC2 con las credenciales del usuario `asesoria`) para publicar el archivo `.zip` como una nueva Layer.

```bash
aws lambda publish-layer-version \
  --layer-name flask-dependencies-py311 \
  --description "Dependencias para Flask en Python 3.11" \
  --zip-file fileb://layer-flask.zip \
  --compatible-runtimes python3.11
```
*   `--layer-name`: Un nombre descriptivo para la Layer.
*   `--description`: Una descripción opcional.
*   `--zip-file`: La ruta al archivo `.zip`. El prefijo `fileb://` es importante para indicar que se está subiendo un archivo binario.
*   `--compatible-runtimes`: Especifica con qué runtimes de Lambda es compatible esta Layer.

Al ejecutar este comando exitosamente, la AWS CLI devuelve un objeto JSON que contiene el **`LayerVersionArn`**. Este ARN es el identificador único de la Layer que se utilizará en el archivo `serverless.yml` para asociarla a la función Lambda.

# Guía 5: Reconfigurando el Despliegue con Layers y WSGI

Con la Lambda Layer creada y publicada, el siguiente paso es modificar la configuración de Serverless Framework para que la utilice, y ajustar el código para que la comunicación entre API Gateway y Flask funcione correctamente. Esto introduce dos conceptos clave: el uso de Layers en `serverless.yml` y el protocolo WSGI.

## 1. El Rol de WSGI (Web Server Gateway Interface)

**¿Por qué necesitamos algo más que Flask y Lambda?**

*   Una aplicación **Flask** es una aplicación que sigue la especificación **WSGI**. WSGI es un estándar en Python que define una interfaz de comunicación simple y universal entre un servidor web y una aplicación web. Cuando ejecutas `flask run`, se levanta un servidor de desarrollo que sabe cómo "hablar" WSGI con tu aplicación.
*   **AWS Lambda**, por otro lado, no es un servidor web tradicional. No escucha en un puerto. En su lugar, se activa mediante "eventos". Para una API, el evento es una estructura de datos JSON enviada por API Gateway que contiene toda la información de la petición HTTP (headers, body, path, etc.).
*   El problema es que Flask no entiende este formato de evento JSON de Lambda, y Lambda no sabe cómo invocar una aplicación WSGI.

**La Solución: un Adaptador WSGI**

Necesitamos un "traductor" o "adaptador" que se sitúe entre Lambda y Flask. Este adaptador recibe el evento JSON de Lambda, lo convierte en una petición compatible con el estándar WSGI que Flask pueda entender, pasa la petición a Flask, y luego toma la respuesta de Flask y la convierte de nuevo en el formato JSON que API Gateway espera.

Para esto, se utilizó el plugin **`serverless-wsgi`**.

## 2. Introducción al Plugin `serverless-wsgi`

`serverless-wsgi` es un plugin para Serverless Framework que simplifica enormemente el despliegue de aplicaciones WSGI (como Flask o Django).
*   **A nivel de despliegue**, se encarga de configurar correctamente el handler.
*   **A nivel de ejecución**, su librería (que instalamos en la Lambda Layer) realiza la traducción de eventos mencionada anteriormente.

## 3. Modificación del Archivo `serverless.yml`

El archivo de configuración fue modificado drásticamente para reflejar el nuevo enfoque.

**Configuración ANTERIOR:**
```yaml
# ... (omitiendo partes)
plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: false
```

**Configuración NUEVA Y FINAL:**
```yaml
service: mi-api-flask
frameworkVersion: '3'

provider:
  name: aws
  runtime: python3.11
  region: us-east-1

functions:
  api:
    handler: wsgi_handler.handler
    # SECCIÓN NUEVA: Se añade la Layer
    layers:
      - arn:aws:lambda:us-east-1:1234567890:layer:flask-dependencies-py311:1 # ¡REEMPLAZAR CON TU ARN!
    events:
      - httpApi: '*'

# SECCIÓN MODIFICADA: Se cambia el plugin
plugins:
  - serverless-wsgi

# (Opcional pero recomendado) Se añade configuración para el plugin wsgi
custom:
  wsgi:
    app: app.app
    packRequirements: false # Le dice al plugin que no empaquete dependencias
```
**Cambios Clave:**

1.  **Se eliminó `serverless-python-requirements`**: Ya no es necesario porque las dependencias ahora son gestionadas por la Lambda Layer.
2.  **Se añadió `serverless-wsgi` al bloque `plugins`**: Esto activa el nuevo plugin.
3.  **Se añadió el bloque `layers` a la función**: Aquí se pegó el `LayerVersionArn` obtenido en el paso anterior. Esto le indica a AWS Lambda que debe "adjuntar" el contenido de la Layer al entorno de ejecución de la función.
4.  **Se añadió `packRequirements: false`**: Esta configuración para `serverless-wsgi` es importante. Le indica al plugin que no debe intentar instalar las dependencias por sí mismo, ya que sabemos que están en la Layer.

## 4. Modificación del Código del Handler

El archivo `wsgi_handler.py` es el punto de entrada que Lambda invoca. También fue modificado para usar la librería `serverless-wsgi`.

**`wsgi_handler.py`**
```python
# Se importa la aplicación Flask desde app.py
from app import app
# Se importa el manejador del adaptador
from serverless_wsgi import handle as wsgi_handler

# Se define el handler que Lambda ejecutará
def handler(event, context):
    return wsgi_handler(app, event, context)
```
Este código es muy simple: importa la instancia de la aplicación Flask (`app`) y la pasa al manejador de `serverless_wsgi`, que se encarga de toda la lógica de traducción.

Con estos cambios en el código y la configuración, el proyecto estaba listo para el despliegue final.



# Guía 6: Despliegue Final, Pruebas y Conclusiones

Este último capítulo detalla el despliegue final de la aplicación Flask utilizando la configuración con Lambda Layers y `serverless-wsgi`. Además, resume el flujo de trabajo completo y las lecciones aprendidas durante la asesoría.

## 1. El Proceso de Despliegue Final

Con el `serverless.yml` y el código del handler actualizados, el despliegue se realizó ejecutando una vez más el comando:

```bash
serverless deploy
```

**¿Qué ocurrió esta vez?**

A diferencia del primer intento, el proceso de empaquetado fue diferente:
1.  **Serverless Framework** reconoció la configuración de la Lambda Layer en el archivo `serverless.yml`.
2.  El plugin `serverless-wsgi` se activó, pero gracias a la configuración `packRequirements: false`, no intentó instalar ninguna dependencia de Python.
3.  El framework empaquetó únicamente el código fuente de la aplicación (`app.py` y `wsgi_handler.py`) en un archivo `.zip`. Este archivo era significativamente más pequeño que el del primer despliegue.
4.  Al crear o actualizar la función en AWS Lambda, Serverless le indicó a AWS que adjuntara la Layer especificada por su ARN.

Cuando la función Lambda se ejecuta, AWS combina el contenido del paquete de la función con el contenido de la Layer en el entorno de ejecución, permitiendo que el código importe `flask` y `serverless_wsgi` sin problemas.

## 2. Verificación y Pruebas

Al finalizar el despliegue, la terminal de Serverless mostró la información del stack, incluyendo los endpoints de la API.

```
endpoints:
  ANY / -> https://ab12cde3f4.execute-api.us-east-1.amazonaws.com
```

Para verificar que todo funcionaba correctamente, se accedió a esa URL desde un navegador web o utilizando una herramienta como `curl`:

```bash
curl https://ab12cde3f4.execute-api.us-east-1.amazonaws.com
```

**Resultado Esperado:**

El comando devolvió exitosamente el mensaje definido en la aplicación Flask:

`"Bienvenido al servidor de Flask"`

Este resultado confirmó que todos los componentes estaban funcionando en armonía:
*   **API Gateway** recibió la petición y la reenvió a Lambda.
*   **AWS Lambda** ejecutó el handler.
*   La **Lambda Layer** proveyó las dependencias de `flask` y `serverless-wsgi`.
*   El adaptador **`serverless-wsgi`** tradujo el evento para Flask.
*   La aplicación **Flask** procesó la petición y devolvió la respuesta.
*   El ciclo se completó, devolviendo la respuesta al cliente.

## 3. Resumen del Flujo de Trabajo y Lecciones Clave

Esta asesoría demostró un flujo de trabajo completo y realista para superar limitaciones del entorno de desarrollo y desplegar aplicaciones web en un entorno serverless.

**El Proceso Resumido:**

1.  **Problema Identificado**: La imposibilidad de usar Docker en un entorno de desarrollo Windows impide la creación de paquetes de despliegue de Python compatibles con Lambda.
2.  **Solución Estratégica**: Se utilizó una instancia **EC2 con Amazon Linux** como un entorno de "build" remoto y compatible.
3.  **Gestión de Dependencias**: En lugar de empaquetar las dependencias con cada despliegue, se construyó una **Lambda Layer** reutilizable que contenía las versiones correctas de las librerías.
4.  **Adaptación del Framework**: Se entendió la naturaleza **WSGI** de Flask y se implementó el plugin **`serverless-wsgi`** como el adaptador necesario para la comunicación en el entorno serverless.
5.  **Configuración Final**: El archivo `serverless.yml` se reconfiguró para dejar de gestionar dependencias y, en su lugar, referenciar la Lambda Layer por su ARN.
6.  **Éxito**: El despliegue final fue exitoso, demostrando la viabilidad y robustez de la solución.

**Conclusiones y Buenas Prácticas:**

*   **Los entornos importan**: La paridad entre el entorno de desarrollo/build y el de producción (en este caso, Lambda) es crucial para evitar errores de compatibilidad.
*   **Lambda Layers son tus aliadas**: Para la gestión de dependencias complejas o para optimizar los tiempos de despliegue, las Layers son una herramienta fundamental en el ecosistema serverless.
*   **Comprende los protocolos**: Entender qué es WSGI (o ASGI para frameworks modernos) es clave para saber cómo integrar correctamente una aplicación web en una plataforma como AWS Lambda.
*   **La seguridad es primordial**: Aunque se utilizaron configuraciones permisivas por motivos educativos, siempre se debe priorizar la seguridad, especialmente en el acceso a recursos como instancias EC2, aplicando el principio de menor privilegio y utilizando redes seguras.```