# Library yang digunakan
import cv2
import mediapipe as mp
import numpy as np

# Inisialisasi Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Variabel global untuk menyimpan simbol tangan yang terdeteksi dan operasi aktif
left_hand_signs_detected = []
right_hand_signs_detected = []
active_operation = None
operations = {"+": "Tambah", "-": "Kurang", "*": "Kali", "/": "Bagi"}

def detect_hand_sign(landmarks, handedness):
    """
    Mendeteksi simbol tangan berdasarkan posisi landmark.

    Parameters:
        landmarks (list): Daftar landmark dari tangan yang terdeteksi, bisa dilihat melalui tautan [ini](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?hl=id).

    Returns:
        str: Simbol tangan yang terdeteksi ('0'-'5') atau None jika tidak terdeteksi.
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

    Parameters:
        x (int): Koordinat x jari telunjuk.
        y (int): Koordinat y jari telunjuk.

    Returns:
        str: Simbol operasi matematika ('+', '-', '*', '/') atau None jika tidak terdeteksi.
    """
    for i, (symbol, label) in enumerate(operations.items()):
        if 10 <= x <= 60 and 50 + i * 50 <= y <= 90 + i * 50:
            return symbol
    return None

def calculate_result(left, right, operation):
    """
    Menghitung hasil operasi matematika berdasarkan input tangan kiri, kanan, dan operasi.

    Parameters:
        left (str): Simbol angka yang terdeteksi pada tangan kiri.
        right (str): Simbol angka yang terdeteksi pada tangan kanan.
        operation (str): Simbol operasi matematika yang terdeteksi.

    Returns:
        float/int/str: Hasil perhitungan atau pesan error jika operasi tidak valid.
    """
    left = int(left)
    right = int(right)
    if operation == "+":
        return left + right
    if operation == "-":
        return left - right
    if operation == "*":
        return left * right
    if operation == "/" and right != 0:
        return left / right
    return "Error"

def main():
    """
    Fungsi utama untuk menjalankan kalkulator berbasis simbol tangan.
    """
    # Inisialisasi variabel global dalam fungsi main karena nilai variabel bisa berubah
    global active_operation, left_hand_signs_detected, right_hand_signs_detected

    # Buka webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip frame untuk tampilan lebih alami
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Proses deteksi tangan
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Tampilkan menu operasi di kiri atas
        for i, (symbol, label) in enumerate(operations.items()):
            color = (0, 255, 0) if active_operation == symbol else (255, 255, 255)
            cv2.rectangle(frame, (10, 50 + i * 50), (60, 90 + i * 50), color, -1)
            cv2.putText(frame, symbol, (15, 85 + i * 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        # Deteksi tangan dan operasi
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[idx].classification[0].label
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Deteksi simbol tangan
                hand_sign = detect_hand_sign(hand_landmarks.landmark, handedness)
                if hand_sign:
                    if handedness == "Left" and hand_sign not in left_hand_signs_detected:
                        left_hand_signs_detected = [hand_sign]
                    elif handedness == "Right" and hand_sign not in right_hand_signs_detected:
                        right_hand_signs_detected = [hand_sign]

                # Deteksi pilihan operasi
                x = int(hand_landmarks.landmark[8].x * w)
                y = int(hand_landmarks.landmark[8].y * h)
                selected_operation = detect_operation(x, y)
                if selected_operation:
                    if selected_operation != active_operation:
                        # Reset perhitungan jika operasi berubah
                        left_hand_signs_detected = []
                        right_hand_signs_detected = []
                    active_operation = selected_operation

        # Hitung hasil jika kedua tangan terdeteksi
        if active_operation and left_hand_signs_detected and right_hand_signs_detected:
            result = calculate_result(left_hand_signs_detected[0], right_hand_signs_detected[0], active_operation)
            cv2.putText(frame, f"Result: {result}", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # Tampilkan nilai masing-masing tangan
        if left_hand_signs_detected:
            cv2.putText(frame, f"Left: {left_hand_signs_detected[0]}", (200, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if right_hand_signs_detected:
            cv2.putText(frame, f"Right: {right_hand_signs_detected[0]}", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


        # Tampilkan simbol operasi yang aktif
        if active_operation:
            cv2.putText(frame, f"Operation: {active_operation}", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Tampilkan frame
        cv2.imshow("Hand Sign Calculator", frame)

        # Keluar dari loop jika 'q' ditekan
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()