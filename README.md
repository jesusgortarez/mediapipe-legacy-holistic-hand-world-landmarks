# MediaPipe (Bifurcación): Holistic Legacy con Hand WORLD_LANDMARKS

Este repositorio es una bifurcación (_fork_) del proyecto original de código abierto MediaPipe de Google, **basado específicamente en la versión 0.10.24**.

### Justificación de la Versión

Se ha seleccionado la versión **0.10.24** como base estable para este parche debido a que es el punto óptimo de compatibilidad entre las APIs de **Solutions** y la infraestructura **Legacy**. Esta versión permite realizar modificaciones profundas en los grafos de cálculo sin perder la integración con los componentes de alto nivel que muchos desarrollos actuales todavía requieren.

### Propósito del Parche

Esta versión contiene modificaciones estructurales en los grafos de cálculo de la arquitectura **MediaPipe Holistic Legacy**. Su propósito es exponer las coordenadas espaciales métricas tridimensionales (`WORLD_LANDMARKS`) de las manos, datos que la arquitectura original calcula internamente pero que omite enrutar hacia la salida final (_output streams_).

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

Una vez instalado el paquete precompilado, el objeto de resultados de la clase `Holistic` expondrá los nuevos atributos espaciales.
Puede validar la extracción de los nuevos datos ejecutando el script de prueba incluido en este repositorio. Este script descarga una imagen de prueba, la procesa utilizando la nueva topología y extrae las coordenadas.

Ejecute el siguiente comando desde su terminal (asegúrese de estar ubicado en la raíz del repositorio):

```python
python scripts/test_holistic_hand_world_landmarks.py
```

o bien aqui esta el script test_holistic_hand_world_landmarks

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

## Cumplimiento de Licencia

El código fuente original de MediaPipe es distribuido bajo la Licencia Apache 2.0. De acuerdo con sus estipulaciones legales, los archivos originales `.pbtxt` y `.py` modificados para este proyecto contienen un aviso explícito documentando la alteración.

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
