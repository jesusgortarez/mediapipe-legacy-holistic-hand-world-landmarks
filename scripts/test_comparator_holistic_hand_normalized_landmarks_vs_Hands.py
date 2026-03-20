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
mp_hands = mp.solutions.hands

with mp_holistic.Holistic(static_image_mode=True, model_complexity=1) as holistic, \
     mp_hands.Hands(static_image_mode=True, max_num_hands=2, model_complexity=1) as hands:
    
    # Leer la imagen descargada
    image = cv2.imread("temp_image.jpg")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesar
    results_holistic = holistic.process(image_rgb)
    results_hands = hands.process(image_rgb)

    # --- Resultados Holistic ---
    holistic_left = results_holistic.left_hand_landmarks
    holistic_right = results_holistic.right_hand_landmarks

    # --- Resultados Hands ---
    hands_left = None
    hands_right = None
    if results_hands.multi_hand_landmarks:
        for handedness, hand_landmarks in zip(results_hands.multi_handedness, results_hands.multi_hand_landmarks):
            label = handedness.classification[0].label
            # MediaPipe Hands asume por defecto un modo 'selfie' (espejo) para la clasificación de manos.
            # Por lo tanto, invertimos la etiqueta para que coincida con la perspectiva de Holistic.
            if label == 'Left':
                hands_right = hand_landmarks
            elif label == 'Right':
                hands_left = hand_landmarks

    # Mostrar landmarks (Coordenadas métricas) comparadas
    print("=== COMPARACIÓN Normalized landmarks ===")
    
    # if holistic_left and hands_left:
    #     print("\n[Mano Izquierda]")
    #     print("  Holistic (landmark 5): x={:.4f}, y={:.4f}, z={:.4f}".format(
    #         holistic_left.landmark[5].x, holistic_left.landmark[5].y, holistic_left.landmark[5].z))
    #     print("  Hands    (landmark 5): x={:.4f}, y={:.4f}, z={:.4f}".format(
    #         hands_left.landmark[5].x, hands_left.landmark[5].y, hands_left.landmark[5].z))
        
    # if holistic_right and hands_right:
    #     print("\n[Mano Derecha]")
    #     print("  Holistic (landmark 5): x={:.4f}, y={:.4f}, z={:.4f}".format(
    #         holistic_right.landmark[5].x, holistic_right.landmark[5].y, holistic_right.landmark[5].z))
    #     print("  Hands    (landmark 5): x={:.4f}, y={:.4f}, z={:.4f}".format(
    #         hands_right.landmark[5].x, hands_right.landmark[5].y, hands_right.landmark[5].z))

    # if holistic_left and hands_left:
    #     print("\n[Mano Izquierda 0]")
    #     print("  Holistic (landmark 0): x={:.4f}, y={:.4f}, z={:.4f}".format(
    #         holistic_left.landmark[0].x, holistic_left.landmark[0].y, holistic_left.landmark[0].z))
    #     print("  Hands    (landmark 0): x={:.4f}, y={:.4f}, z={:.4f}".format(
    #         hands_left.landmark[0].x, hands_left.landmark[0].y, hands_left.landmark[0].z))
        
    # if holistic_right and hands_right:
    #     print("\n[Mano Derecha 0]")
    #     print("  Holistic (landmark 0): x={:.4f}, y={:.4f}, z={:.4f}".format(
    #         holistic_right.landmark[0].x, holistic_right.landmark[0].y, holistic_right.landmark[0].z))
    #     print("  Hands    (landmark 0): x={:.4f}, y={:.4f}, z={:.4f}".format(
    #         hands_right.landmark[0].x, hands_right.landmark[0].y, hands_right.landmark[0].z))


    if holistic_left and hands_left:
        print("\n[Mano Izquierda - Todos los puntos]")
        for idx, (hl, hd) in enumerate(zip(holistic_left.landmark, hands_left.landmark)):
            print("  Landmark {:2d} | Holistic: x={:.4f}, y={:.4f}, z={:.4f} | Hands: x={:.4f}, y={:.4f}, z={:.4f}".format(
                idx, hl.x, hl.y, hl.z, hd.x, hd.y, hd.z))

    if holistic_right and hands_right:
        print("\n[Mano Derecha - Todos los puntos]")
        for idx, (hl, hd) in enumerate(zip(holistic_right.landmark, hands_right.landmark)):
            print("  Landmark {:2d} | Holistic: x={:.4f}, y={:.4f}, z={:.4f} | Hands: x={:.4f}, y={:.4f}, z={:.4f}".format(
                idx, hl.x, hl.y, hl.z, hd.x, hd.y, hd.z))

    # Ver la imagen
    cv2.imshow("Prueba Comparativa", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()