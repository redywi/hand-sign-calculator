# Library yang digunakan
import cv2
import mediapipe as mp
import numpy as np
import pygame
import time

# Inisialisasi pygame mixer
pygame.mixer.init()

# Load file audio
sound_click = pygame.mixer.Sound("sfx/click.mp3")  # Suara untuk klik operasi
sound_success = pygame.mixer.Sound("sfx/succes.mp3")  # Suara untuk hasil kalkulasi
sound_error = pygame.mixer.Sound("sfx/error.mp3")  # Suara untuk kesalahan (misalnya, pembagian dengan nol)

# Inisialisasi Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Variabel global
left_hand_signs_detected = []
right_hand_signs_detected = []
active_operation = None
operation_processed = False  # Flag untuk memastikan operasi hanya diproses sekali
last_result = None  # Variabel untuk menyimpan hasil terakhir
operations = {"+": "Tambah", "-": "Kurang", "*": "Kali", "/": "Bagi"}

# Variabel untuk mengelola waktu jeda
last_sound_time = 0  # Timestamp terakhir suara dimainkan
click_delay = 1  # Jeda untuk suara klik (detik)

def play_sound_with_delay(sound, delay):
    """
    Mendeteksi simbol tangan berdasarkan posisi landmark.

    Parameters:
        landmarks (list): Daftar landmark dari tangan yang terdeteksi, bisa dilihat melalui tautan [ini](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?hl=id).

    Returns:
        str: Simbol tangan yang terdeteksi ('0'-'5') atau None jika tidak terdeteksi.
    """
    
    global last_sound_time
    current_time = time.time()
    if current_time - last_sound_time >= delay:
        sound.play()
        last_sound_time = current_time

def detect_hand_sign(landmarks, handedness):
    """
    Mendeteksi simbol tangan berdasarkan posisi landmark.
    (Sama seperti sebelumnya.)
    """
    # Untuk tangan kanan (handedness == 'Right')
    if handedness == "Right":
        # Mengecek apakah tangan membentuk simbol 'nol'
        if (landmarks[4].x > landmarks[3].x and landmarks[8].y > landmarks[6].y and landmarks[12].y > landmarks[10].y and landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y):
            return '0'
        # Mengecek apakah tangan membentuk simbol 'satu'
        if (landmarks[4].x > landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y > landmarks[10].y and landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y):
            return '1'
        # Mengecek apakah tangan membentuk simbol 'dua'
        if (landmarks[4].x > landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y):
            return '2'
        # Mengecek apakah tangan membentuk simbol 'tiga'
        if (landmarks[4].x > landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and landmarks[20].y > landmarks[18].y):
            return '3'
        # Mengecek apakah tangan membentuk simbol 'empat'
        if (landmarks[4].x > landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and landmarks[20].y < landmarks[18].y):
            return '4'
        # Mengecek apakah tangan membentuk simbol 'lima'
        if (landmarks[4].x <= landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and landmarks[20].y < landmarks[18].y):
            return '5'
        
    # Untuk tangan kiri (handedness == 'Left')
    if handedness == "Left":
        # Mengecek apakah tangan membentuk simbol 'nol'
        if (landmarks[4].x <= landmarks[3].x and landmarks[8].y > landmarks[6].y and landmarks[12].y > landmarks[10].y and landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y):
            return '0'
        # Mengecek apakah tangan membentuk simbol 'satu'
        if (landmarks[4].x <= landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y > landmarks[10].y and landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y):
            return '1'
        # Mengecek apakah tangan membentuk simbol 'dua'
        if (landmarks[4].x <= landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y):
            return '2'
        # Mengecek apakah tangan membentuk simbol 'tiga'
        if (landmarks[4].x <= landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and landmarks[20].y > landmarks[18].y):
            return '3'
        # Mengecek apakah tangan membentuk simbol 'empat'
        if (landmarks[4].x <= landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and landmarks[20].y < landmarks[18].y):
            return '4'
        # Mengecek apakah tangan membentuk simbol 'lima'
        if (landmarks[4].x > landmarks[3].x and landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and landmarks[16].y < landmarks[14].y and landmarks[20].y < landmarks[18].y):
            return '5'
    
    return None

def detect_operation(x, y):
    """
    Mendeteksi operasi matematika berdasarkan posisi landmark jari telunjuk.
    """
    for i, (symbol, label) in enumerate(operations.items()):
        if 10 <= x <= 60 and 50 + i * 50 <= y <= 90 + i * 50:
            play_sound_with_delay(sound_click, click_delay)  # Suara dengan jeda
            return symbol
    return None

def calculate_result(left, right, operation):
    """
    Menghitung hasil operasi matematika berdasarkan input tangan kiri, kanan, dan operasi.
    """
    global operation_processed, last_result

    if operation_processed:
        return last_result  # Jangan lakukan perhitungan ulang jika sudah diproses

    left = int(left)
    right = int(right)
    result = None

    if operation == "+":
        result = left + right
    elif operation == "-":
        result = left - right
    elif operation == "*":
        result = left * right
    elif operation == "/" and right != 0:
        result = left / right
    else:
        result = "Error"
        sound_error.play()  # Suara error jika pembagian dengan nol

    # Mainkan suara sukses hanya jika operasi valid
    if result != "Error":
        sound_success.play()

    operation_processed = True  # Tandai bahwa operasi sudah diproses
    last_result = result  # Simpan hasil terakhir
    return result

def draw_text_with_stroke(frame, text, position, font, scale, color, thickness, stroke_color, stroke_thickness):
    # Gambar stroke hitam
    x, y = position
    cv2.putText(frame, text, (x, y), font, scale, stroke_color, stroke_thickness, lineType=cv2.LINE_AA)
    # Gambar teks utama
    cv2.putText(frame, text, (x, y), font, scale, color, thickness, lineType=cv2.LINE_AA)

def main():
    global active_operation, left_hand_signs_detected, right_hand_signs_detected, operation_processed, last_result

    # Buka webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Gambar tombol operasi dengan ukuran yang sesuai teks
        margin = 10  # Margin di sekitar teks
        y_offset = 50  # Offset vertikal untuk tombol

        for i, (symbol, label) in enumerate(operations.items()):
            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
            text_width, text_height = text_size[0]
            text_baseline = text_size[1]

            # Tentukan koordinat kotak berdasarkan ukuran teks
            x1, y1 = 10, y_offset + i * (text_height + 2 * margin + 10)
            x2, y2 = x1 + text_width + 2 * margin, y1 + text_height + 2 * margin

            # Warna kotak berdasarkan status aktif
            color_fill = (50, 205, 50) if active_operation == symbol else (255, 255, 255)
            color_outline = (0, 128, 0) if active_operation == symbol else (0, 0, 0)

            # Gambar kotak tombol
            cv2.rectangle(frame, (x1, y1), (x2, y2), color_outline, 2)
            cv2.rectangle(frame, (x1 + 2, y1 + 2), (x2 - 2, y2 - 2), color_fill, -1)

            # Tambahkan label pada tombol (teks di tengah kotak)
            text_x = x1 + margin
            text_y = y1 + text_height + margin
            cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Deteksi tangan
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[idx].classification[0].label
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                hand_sign = detect_hand_sign(hand_landmarks.landmark, handedness)
                if hand_sign:
                    if handedness == "Left" and hand_sign not in left_hand_signs_detected:
                        left_hand_signs_detected = [hand_sign]
                        operation_processed = False  # Reset saat input berubah
                    elif handedness == "Right" and hand_sign not in right_hand_signs_detected:
                        right_hand_signs_detected = [hand_sign]
                        operation_processed = False  # Reset saat input berubah

                # Deteksi operasi berdasarkan posisi jari
                x = int(hand_landmarks.landmark[8].x * w)
                y = int(hand_landmarks.landmark[8].y * h)
                selected_operation = detect_operation(x, y)
                if selected_operation:
                    if selected_operation != active_operation:
                        left_hand_signs_detected = []
                        right_hand_signs_detected = []
                        active_operation = selected_operation
                        operation_processed = False  # Reset saat operasi berubah
                
                x = int(hand_landmarks.landmark[8].x * w)
                y = int(hand_landmarks.landmark[8].y * h)
                selected_operation = detect_operation(x, y)
                if selected_operation:
                    if selected_operation != active_operation:
                        left_hand_signs_detected = []
                        right_hand_signs_detected = []
                        active_operation = selected_operation
                        operation_processed = False

        if left_hand_signs_detected:
            draw_text_with_stroke(frame, f"Kiri: {left_hand_signs_detected[0]}", (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, (0, 0, 0), 3)
        if right_hand_signs_detected:
            draw_text_with_stroke(frame, f"Kanan: {right_hand_signs_detected[0]}", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, (0, 0, 0), 3)

        # Tampilkan hasil
        if active_operation and left_hand_signs_detected and right_hand_signs_detected:
            result = calculate_result(left_hand_signs_detected[0], right_hand_signs_detected[0], active_operation)
            if result is not None:
                draw_text_with_stroke(frame, f"Hasil: {result}", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, (0, 0, 0), 3)
        
        if active_operation:
            operation_label = operations.get(active_operation, "")
            draw_text_with_stroke(frame, f"Operasi: {operation_label}", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, (0, 0, 0), 3)

        cv2.imshow("Hand Sign Calculator", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
