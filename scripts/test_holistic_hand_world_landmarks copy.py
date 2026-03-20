import mediapipe as mp
import cv2
import os


# 1. Descargar la imagen directamente al disco solo si no existe
url = "https://cdn.pixabay.com/photo/2019/03/12/20/39/girl-4051811_960_720.jpg"
out_path = "temp_image.jpg"
if not os.path.exists(out_path):
    
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
else:
    print(f"La imagen '{out_path}' ya existe. No se descarga de nuevo.")

# 2. Configurar MediaPipe
mp_holistic = mp.solutions.holistic

with mp_holistic.Holistic(static_image_mode=True, model_complexity=1) as holistic:
    # Leer la imagen descargada
    image = cv2.imread("temp_image.jpg")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesar
    results = holistic.process(image_rgb)

    # Mostrar Normalizer_LANDMARKS (Coordenadas normalizadas)
    if results.left_hand_landmarks:
        print("Mano izquierda detectada (Normalizer):")
        print(results.left_hand_landmarks.landmark[0]) 

    if results.right_hand_landmarks:
        print("Mano derecha detectada (Normalizer):")
        print(results.right_hand_landmarks.landmark[0])

    # Mostrar WORLD_LANDMARKS (Coordenadas métricas)
    if results.left_hand_world_landmarks:
        print("Mano izquierda detectada (World):")
        print(results.left_hand_world_landmarks.landmark[0]) 

    if results.right_hand_world_landmarks:
        print("Mano derecha detectada (World):")
        print(results.right_hand_world_landmarks.landmark[0])

    # Ver la imagen
    cv2.imshow("Prueba Holistic", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()