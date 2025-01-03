# Hand Sign Calculator  
Proyek **Hand Sign Calculator** adalah filter berbasis Python yang memungkinkan pengguna untuk melakukan operasi matematika sederhana dengan menggunakan gestur tangan sebagai input. Aplikasi ini memanfaatkan teknologi Mediapipe untuk mendeteksi simbol tangan dan memilih operasi matematika seperti penjumlahan, pengurangan, perkalian, dan pembagian. Project ini dibuat untuk memenuhi Ujian Akhir Semester mata kuliah **IF4021-Sistem/Teknologi Multimedia** program studi Teknik Informatika yang diampu oleh **Martin Clinton Tosima Manullang, S.T., M.T.** (**[mctosima](https://github.com/mctosima)**)

## Fitur Utama  
- Deteksi gestur angka menggunakan landmark tangan dari Mediapipe.  
- Pemilihan operasi matematika (+, -, *, /) melalui gestur jari.  
- Tampilan hasil secara real-time pada layar webcam.  
- Setiap interaksi memiliki efek suara yang berbeda

---

## Anggota Tim  

<table>
  <tr>
    <td><img src="https://avatars.githubusercontent.com/u/113443626?v=4" alt="Made Redy Wijaya" width="50" height="50" style="border-radius: 50%;"></td>
    <td>Made Redy Wijaya (121140157)</td>
    <td><a href="https://github.com/redywi">@redywi</a></td>
  </tr>
  <tr>
    <td><img src="https://avatars.githubusercontent.com/u/90200753?v=4" alt="Farhan Apri Kesuma" width="50" height="50" style="border-radius: 50%;"></td>
    <td>Farhan Apri Kesuma (121140179)</td>
    <td><a href="https://github.com/parhannn">@parhannn</a></td>
  </tr>
  <tr>
    <td><img src="https://avatars.githubusercontent.com/u/100509735?v=4" alt="Carlos Piero Parhusip" width="50" height="50" style="border-radius: 50%;"></td>
    <td>Carlos Piero Parhusip (121140193)</td>
    <td><a href="https://github.com/gyoro2">@gyoro2</a></td>
  </tr>
</table>


---

## Logbook Progress  
| **Minggu** | **Tanggal**   | **Progress**                                                                                  |  
|------------|---------------|----------------------------------------------------------------------------------------------|  
| 1          | [21/11/2024]     | - Inisialisasi proyek, eksplorasi Mediapipe, studi dokumentasi API Hand Landmarker, implementasi deteksi landmark tangan dan penentuan simbol angka menggunakan Mediapipe, pengintegrasian logika operasi matematika dan debugging hasil kalkulasi.      |  
| 2          | [21/11/2024]     | - Menambahkan UI interaktif pada tampilan webcam untuk memilih, finalisasi program, dokumentasi proyek, dan README.md.                     | 
| 3          | [13/12/2024]     | - Menambahkan efek suara untuk setiap interaksi. Yaitu dalam memilih operasi hitung, hasil operasi hitung dan juga error.                    |
| 3          | [13/12/2024]     | - Memperbaiki UI lama menjadi lebih user-friendly.                    |
| 4          | [16/12/2024]     | - Membuat pelaporan menggunakan LaTex dengan Overleaf sebagai compiler online **[Link Laporan](https://www.overleaf.com/project/67400b14b896283a47afc602)**.                    |
| 5          | [23/12/2024]     | - Mengecek kembali program tidak ada lagi bug atau glitch yang ada dan menyembunyikan landmark pada kamera demi kenyamanan pengguna.                    |


---

## Instruksi Instalasi dan Penggunaan  

### 1. Prasyarat  
Pastikan Anda sudah menginstal **Python 3.8** atau versi lebih baru di sistem Anda.  

### 2. Instalasi  
1. Clone repositori ini ke komputer Anda:  
   ```bash  
   git clone https://github.com/redywi/hand-sign-calculator.git  
   cd hand-sign-calculator
    ```
2. Instal dependensi menggunakan requirements.txt:  
   ```bash  
   pip install -r requirements.txt  
    ```
### 3. Menjalankan Program
1. Jalankan file utama menggunakan Python:  
   ```bash  
    python main.py 
    ```
2. Arahkan tangan Anda ke kamera untuk mendeteksi simbol angka atau memilih operasi.

### 4. Penggunaan Gestur
- Gestur Angka (0-5): Gunakan satu tangan untuk menunjukkan angka yang ingin dimasukkan.
- Memilih Operasi: Arahkan jari telunjuk ke simbol operasi yang ditampilkan di layar (tambah, kurang, kali, bagi).
- Hasil: Hasil perhitungan akan ditampilkan secara real-time di layar.

---

## Contoh Tampilan Program
Tampilan layar program akan menunjukkan:
### 1. Menu Operasi: Daftar operasi matematika di sisi kiri atas layar.

![Snapshots](./snapshots/menu_button.png)

### 2. Deteksi Angka: Angka dari tangan kiri dan kanan yang terdeteksi.

![Snapshots](./snapshots/number_detection.png)

### 3. Hasil Perhitungan: Ditampilkan di bagian tengah layar.

![Snapshots](./snapshots/result_indicator.png)

### 4. Hasil Akhir Program

![Snapshots](./snapshots/result.png)

---

## Kontribusi
Kami terbuka untuk masukan dan kontribusi lebih lanjut. Jika ingin berkontribusi, silakan buat pull request atau ajukan issue pada repositori ini.
