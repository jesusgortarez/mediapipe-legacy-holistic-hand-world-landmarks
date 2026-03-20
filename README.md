# MediaPipe (Bifurcación): Holistic Legacy con Hand WORLD_LANDMARKS

Este repositorio es una bifurcación (_fork_) del proyecto original de código abierto MediaPipe de Google, **basado específicamente en la versión 0.10.24**.

### Justificación de la Versión

Se ha seleccionado la versión **0.10.24** como base estable para este parche debido a que es el punto óptimo de compatibilidad entre las APIs de **Solutions** y la infraestructura **Legacy**. Esta versión permite realizar modificaciones profundas en los grafos de cálculo sin perder la integración con los componentes de alto nivel que muchos desarrollos actuales todavía requieren.

### Propósito del Parche (Arquitectura Híbrida)

Esta versión contiene modificaciones estructurales profundas en los grafos de cálculo de la arquitectura **MediaPipe Holistic Legacy**. Su propósito fundamental es exponer las coordenadas espaciales métricas tridimensionales (`WORLD_LANDMARKS`) de las manos, datos que la arquitectura original omite enrutar hacia la salida.

Para asegurar la consistencia espacial, **se ha rediseñado el flujo de recorte integrando `PalmDetection` directamente dentro de Holistic**. El sistema toma el recorte corporal de la pose y utiliza la red neuronal de detección de palmas (idéntica a la empleada por MediaPipe Hands) para calcular la caja delimitadora de seguimiento utilizando los mismos parámetros geométricos (`scale: 2.6`, `shift: -0.5`). 

De esta forma, Holistic produce `WORLD_LANDMARKS` con una calibración métrica y proporción tridimensional equivalentes a las del modelo enfocado exclusivamente en manos.

La disponibilidad de estas coordenadas de profundidad con precisión métrica es un requisito crítico en desarrollos de análisis espacial riguroso, permitiendo una interpretación del movimiento en metros reales en lugar de solo coordenadas normalizadas a la imagen.

## Herramientas de Parcheo y Pruebas

Para mantener la transparencia de las modificaciones y aislar los entornos de prueba, el repositorio incluye el directorio `scripts/`. Este directorio contiene los siguientes archivos estructurales:

~~- **`patch_world_landmarks.py`**: Script de automatización que inyecta las configuraciones de salida (`output_stream`) para los `WORLD_LANDMARKS` directamente en los archivos de grafos (`.pbtxt`) y en el envoltorio de Python (`holistic.py`) del código fuente.~~
- **`test_holistic_hand_world_landmarks.py`**: Script de validación diseñado para ejecutarse fuera de la raíz del código fuente (evitando el sombreado de módulos o _shadowing_). Su función es verificar que el paquete compilado e instalado en el sistema operativo expone correctamente los nuevos atributos.

## Instalación de la Versión Modificada

Para preservar la eficiencia del pipeline integrado y evitar los procesos de compilación locales (Bazel, C++), se proporcionan los binarios de instalación de Python precompilados (`.whl`) para arquitecturas de escritorio.

1. Desinstale cualquier versión previa de MediaPipe en su entorno virtual:

   ```bash
   pip uninstall mediapipe
   ```

2. Diríjase a la sección de **Releases** de este repositorio.
3. Copie el enlace directo del archivo `.whl` correspondiente a su sistema operativo (Windows, Linux, macOS Intel o macOS Silicon).
4. Instale el paquete utilizando el enlace directo:
   ```bash
   pip install [URL_DEL_ARCHIVO_WHL]
   ```

### Instalación Windows (Ejemplo python 3.12)

```bash
 pip install https://github.com/jesusgortarez/mediapipe-legacy-holistic-hand-world-landmarks/releases/download/v.0.10.21-patched/mediapipe-0.10.21-cp312-cp312-win_amd64.whl
```

## Verificación de Resultados

Una vez instalado el paquete precompilado, el objeto de resultados de la clase `Holistic` expondrá los nuevos atributos espaciales métricos en 3D.

Para probar rápidamente que la instalación funciona y que los datos existen, ejecute el script de prueba básico:

```bash
python scripts/test_holistic_hand_world_landmarks.py
```

O bien, aquí está el script `test_holistic_hand_world_landmarks` para probarlo directamente:

```python
import mediapipe as mp
import cv2
import os
import urllib.request


import cv2
# 1. Descargar la imagen directamente al disco
url = "https://cdn.pixabay.com/photo/2019/03/12/20/39/girl-4051811_960_720.jpg"
out_path = "temp_image.jpg"
if not os.path.exists(out_path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(out_path, "wb") as f:
        f.write(resp.read())

# 2. Configurar MediaPipe
mp_holistic = mp.solutions.holistic

with mp_holistic.Holistic(static_image_mode=True, model_complexity=1) as holistic:
    # Leer la imagen descargada
    image = cv2.imread("temp_image.jpg")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesar
    results = holistic.process(image_rgb)

    # 3. Mostrar WORLD_LANDMARKS (Coordenadas métricas)
    if results.left_hand_world_landmarks:
        print("Mano izquierda detectada (World):")
        print(results.left_hand_world_landmarks.landmark[0]) # Solo el primer punto para no llenar la consola

    if results.right_hand_world_landmarks:
        print("Mano derecha detectada (World):")
        print(results.right_hand_world_landmarks.landmark[0])

    # 4. Ver la imagen
    cv2.imshow("Prueba Holistic", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
```

## Comparativa de Precisión con Hands

Además, para verificar el diseño matemático de la caja y comprobar que los datos mantienen un escalado métrico comparable al modelo standalone, puede ejecutar el script comparativo:

```bash
python scripts/test_comparator_holistic_hand_world_landmarks_vs_Hands.py
```

### Salida de Ejemplo (Variación por Cropping)

Al ejecutar la comparativa, se observa que las coordenadas arrojadas por Holistic y Hands mantienen una proporción Z equivalente. 
Existe una variación inherente (en el rango de milímetros o de centímetros) debido a que ambas redes neuronales evalúan recortes (crops) de la imagen con resoluciones y escalas ligeramente distintas:

```text
=== COMPARACIÓN WORLD_LANDMARKS ===

[Mano Izquierda]
  Holistic (landmark 0): x=-0.0049, y=-0.0516, z=0.0766
  Hands    (landmark 0): x=-0.0037, y=-0.0478, z=0.0720

[Mano Derecha]
  Holistic (landmark 0): x=-0.0093, y=-0.0568, z=0.0773
  Hands    (landmark 0): x=-0.0092, y=-0.0534, z=0.0762
```

*(Nota: Esta comparativa ilustra la equivalencia de proporciones lograda al unificar el método de recorte mediante PalmDetection en ambas arquitecturas).*

## Consideraciones y Limitaciones

El rediseño hacia una arquitectura híbrida prioriza la precisión espacial (world landmarks) por encima del rendimiento puro, lo cual conlleva compromisos técnicos:

1. **Sobrecarga Computacional:** La inyección del modelo `PalmDetection` añade una red neuronal adicional al flujo de inferencia de Holistic. Aunque el modelo es eficiente, representa un costo de CPU/GPU superior frente al modelo de recorte original (`hand_recrop.tflite`), el cual estaba diseñado específicamente para ser una operación de bajo costo.
2. **Tolerancia a Oclusiones (Caídas de Inferencia):** El modelo de recorte original de Holistic infería la posición aproximada de la mano basándose en la pose del brazo, incluso si la mano estaba borrosa u oculta. En contraste, `PalmDetection` requiere visibilidad clara de las características de la palma. Si la mano se mueve demasiado rápido (motion blur) o se ocluye, el detector no genera una caja delimitadora, resultando en la ausencia de datos (`drop`) para esa mano en el fotograma.
3. **Resolución de "Hand Swapping":** Al usar `PalmDetection` (un detector general de objetos), si ambas manos se cruzan de cerca, el detector encuentra ambas. Originalmente, el sistema retenía la de mayor *score*, causando que ocasionalmente se invirtiera la mano izquierda con la derecha. Para mitigar esta debilidad del detector SSD, se diseñó e inyectó un nodo C++ personalizado (`ClosestToCenterDetectionCalculator`) en el paquete, el cual filtra matemáticamente la caja delimitadora reteniendo exclusivamente aquella más cercana al centro del recorte de la muñeca.

## Arquitecturas Alternativas y Trabajo Futuro

Durante la investigación de las divergencias en la escala espacial 3D, se plantearon múltiples rutas técnicas. A continuación se documenta el estado de estas aproximaciones, abarcando las vías descartadas y las líneas de desarrollo a futuro:

### Aproximaciones Descartadas
- **Doble Inferencia (2-Pass):** Se diseñó e implementó una arquitectura de doble inferencia que resultó en un error de propagación (*distribution shift*). La primera pasada heredaba la distorsión del recorte inicial, deformando las coordenadas base y corrompiendo irrevocablemente la segunda iteración.

### Líneas de Trabajo Futuro
- **Calibración Empírica del Recorte Original:** Modificación manual de los parámetros geométricos de la caja base (ej. `scale: 0.8`, `shift: 0.0`). Esta aproximación plantea ajustar la holgura del recorte de forma directa, ofreciendo una implementación de nulo costo computacional. Sin embargo, su dependencia de constantes rígidas compromete la generalización geométrica ante variaciones extremas de distancia focal.
- **Iteración de Convergencia (3-Pass):** Para mitigar el error de propagación del 2-Pass, se plantea la adición de una tercera iteración que podría forzar teóricamente la convergencia progresiva de la caja de recorte. Aunque esta metodología prescinde de constantes empíricas y redes externas, triplicaría la latencia de la inferencia al exigir múltiples ciclos de procesamiento por fotograma.
- **Calibración Analítica:** Ejecutar Holistic y Hands en paralelo para extraer las métricas de sus cajas delimitadoras, buscando aislar un factor de corrección analítico mediante análisis relacional. Este enfoque restituiría la eficiencia nativa del modelo sin requerir redes adicionales (`PalmDetection`), pero exige diseñar herramientas de sincronización complejas para alinear tensores entre arquitecturas asíncronas.
- **Lógica de Respaldo Dinámico (Fallback):** Extender la actual Arquitectura Híbrida mediante un enrutamiento condicional. Si el detector omite fotogramas por movimiento extremo, el sistema activaría un respaldo utilizando el modelo original `hand_recrop.tflite` o una triangulación desde la pose. Esto garantizaría un flujo ininterrumpido de datos bajo oclusión severa, a expensas de introducir bifurcaciones estructurales que incrementan sustancialmente la complejidad del grafo.

## Cumplimiento de Licencia

El código fuente original de MediaPipe es distribuido bajo la Licencia Apache 2.0. De acuerdo con sus estipulaciones legales, los archivos originales `.pbtxt` y `.py` modificados para este proyecto contienen un aviso explícito documentando la alteración.

Adicionalmente, se han conservado las versiones originales inalteradas (provenientes del tag oficial `v0.10.21`) de todos los archivos modificados, utilizando la extensión `.bak`. Esto facilita la inspección directa de los cambios (*diffs*) y garantiza una total transparencia arquitectónica frente al código base de Google. Los archivos respaldados incluyen los grafos de *recrop* y *landmarks from pose*, así como los archivos estructurales `setup.py`, `WORKSPACE` y `BUILD`.

---

# Documentación Oficial de MediaPipe

---
layout: forward
target: https://developers.google.com/mediapipe
title: Home
nav_order: 1
---

----

**Attention:** *We have moved to
[https://developers.google.com/mediapipe](https://developers.google.com/mediapipe)
as the primary developer documentation site for MediaPipe as of April 3, 2023.*

![MediaPipe](https://developers.google.com/static/mediapipe/images/home/hero_01_1920.png)

**Attention**: MediaPipe Solutions Preview is an early release. [Learn
more](https://developers.google.com/mediapipe/solutions/about#notice).

**On-device machine learning for everyone**

Delight your customers with innovative machine learning features. MediaPipe
contains everything that you need to customize and deploy to mobile (Android,
iOS), web, desktop, edge devices, and IoT, effortlessly.

*   [See demos](https://goo.gle/mediapipe-studio)
*   [Learn more](https://developers.google.com/mediapipe/solutions)

## Get started

You can get started with MediaPipe Solutions by by checking out any of the
developer guides for
[vision](https://developers.google.com/mediapipe/solutions/vision/object_detector),
[text](https://developers.google.com/mediapipe/solutions/text/text_classifier),
and
[audio](https://developers.google.com/mediapipe/solutions/audio/audio_classifier)
tasks. If you need help setting up a development environment for use with
MediaPipe Tasks, check out the setup guides for
[Android](https://developers.google.com/mediapipe/solutions/setup_android), [web
apps](https://developers.google.com/mediapipe/solutions/setup_web), and
[Python](https://developers.google.com/mediapipe/solutions/setup_python).

## Solutions

MediaPipe Solutions provides a suite of libraries and tools for you to quickly
apply artificial intelligence (AI) and machine learning (ML) techniques in your
applications. You can plug these solutions into your applications immediately,
customize them to your needs, and use them across multiple development
platforms. MediaPipe Solutions is part of the MediaPipe [open source
project](https://github.com/google/mediapipe), so you can further customize the
solutions code to meet your application needs.

These libraries and resources provide the core functionality for each MediaPipe
Solution:

*   **MediaPipe Tasks**: Cross-platform APIs and libraries for deploying
    solutions. [Learn
    more](https://developers.google.com/mediapipe/solutions/tasks).
*   **MediaPipe models**: Pre-trained, ready-to-run models for use with each
    solution.

These tools let you customize and evaluate solutions:

*   **MediaPipe Model Maker**: Customize models for solutions with your data.
    [Learn more](https://developers.google.com/mediapipe/solutions/model_maker).
*   **MediaPipe Studio**: Visualize, evaluate, and benchmark solutions in your
    browser. [Learn
    more](https://developers.google.com/mediapipe/solutions/studio).

### Legacy solutions

We have ended support for [these MediaPipe Legacy Solutions](https://developers.google.com/mediapipe/solutions/guide#legacy)
as of March 1, 2023. All other MediaPipe Legacy Solutions will be upgraded to
a new MediaPipe Solution. See the [Solutions guide](https://developers.google.com/mediapipe/solutions/guide#legacy)
for details. The [code repository](https://github.com/google/mediapipe/tree/master/mediapipe)
and prebuilt binaries for all MediaPipe Legacy Solutions will continue to be
provided on an as-is basis.

For more on the legacy solutions, see the [documentation](https://github.com/google/mediapipe/tree/master/docs/solutions).

## Framework

To start using MediaPipe Framework, [install MediaPipe
Framework](https://developers.google.com/mediapipe/framework/getting_started/install)
and start building example applications in C++, Android, and iOS.

[MediaPipe Framework](https://developers.google.com/mediapipe/framework) is the
low-level component used to build efficient on-device machine learning
pipelines, similar to the premade MediaPipe Solutions.

Before using MediaPipe Framework, familiarize yourself with the following key
[Framework
concepts](https://developers.google.com/mediapipe/framework/framework_concepts/overview.md):

*   [Packets](https://developers.google.com/mediapipe/framework/framework_concepts/packets.md)
*   [Graphs](https://developers.google.com/mediapipe/framework/framework_concepts/graphs.md)
*   [Calculators](https://developers.google.com/mediapipe/framework/framework_concepts/calculators.md)

## Community

*   [Slack community](https://mediapipe.page.link/joinslack) for MediaPipe
    users.
*   [Discuss](https://groups.google.com/forum/#!forum/mediapipe) - General
    community discussion around MediaPipe.
*   [Awesome MediaPipe](https://mediapipe.page.link/awesome-mediapipe) - A
    curated list of awesome MediaPipe related frameworks, libraries and
    software.

## Contributing

We welcome contributions. Please follow these
[guidelines](https://github.com/google/mediapipe/blob/master/CONTRIBUTING.md).

We use GitHub issues for tracking requests and bugs. Please post questions to
the MediaPipe Stack Overflow with a `mediapipe` tag.

## Resources

### Publications

*   [Bringing artworks to life with AR](https://developers.googleblog.com/2021/07/bringing-artworks-to-life-with-ar.html)
    in Google Developers Blog
*   [Prosthesis control via Mirru App using MediaPipe hand tracking](https://developers.googleblog.com/2021/05/control-your-mirru-prosthesis-with-mediapipe-hand-tracking.html)
    in Google Developers Blog
*   [SignAll SDK: Sign language interface using MediaPipe is now available for
    developers](https://developers.googleblog.com/2021/04/signall-sdk-sign-language-interface-using-mediapipe-now-available.html)
    in Google Developers Blog
*   [MediaPipe Holistic - Simultaneous Face, Hand and Pose Prediction, on
    Device](https://ai.googleblog.com/2020/12/mediapipe-holistic-simultaneous-face.html)
    in Google AI Blog
*   [Background Features in Google Meet, Powered by Web ML](https://ai.googleblog.com/2020/10/background-features-in-google-meet.html)
    in Google AI Blog
*   [MediaPipe 3D Face Transform](https://developers.googleblog.com/2020/09/mediapipe-3d-face-transform.html)
    in Google Developers Blog
*   [Instant Motion Tracking With MediaPipe](https://developers.googleblog.com/2020/08/instant-motion-tracking-with-mediapipe.html)
    in Google Developers Blog
*   [BlazePose - On-device Real-time Body Pose Tracking](https://ai.googleblog.com/2020/08/on-device-real-time-body-pose-tracking.html)
    in Google AI Blog
*   [MediaPipe Iris: Real-time Eye Tracking and Depth Estimation](https://ai.googleblog.com/2020/08/mediapipe-iris-real-time-iris-tracking.html)
    in Google AI Blog
*   [MediaPipe KNIFT: Template-based feature matching](https://developers.googleblog.com/2020/04/mediapipe-knift-template-based-feature-matching.html)
    in Google Developers Blog
*   [Alfred Camera: Smart camera features using MediaPipe](https://developers.googleblog.com/2020/03/alfred-camera-smart-camera-features-using-mediapipe.html)
    in Google Developers Blog
*   [Real-Time 3D Object Detection on Mobile Devices with MediaPipe](https://ai.googleblog.com/2020/03/real-time-3d-object-detection-on-mobile.html)
    in Google AI Blog
*   [AutoFlip: An Open Source Framework for Intelligent Video Reframing](https://ai.googleblog.com/2020/02/autoflip-open-source-framework-for.html)
    in Google AI Blog
*   [MediaPipe on the Web](https://developers.googleblog.com/2020/01/mediapipe-on-web.html)
    in Google Developers Blog
*   [Object Detection and Tracking using MediaPipe](https://developers.googleblog.com/2019/12/object-detection-and-tracking-using-mediapipe.html)
    in Google Developers Blog
*   [On-Device, Real-Time Hand Tracking with MediaPipe](https://ai.googleblog.com/2019/08/on-device-real-time-hand-tracking-with.html)
    in Google AI Blog
*   [MediaPipe: A Framework for Building Perception Pipelines](https://arxiv.org/abs/1906.08172)

### Videos

*   [YouTube Channel](https://www.youtube.com/c/MediaPipe)
