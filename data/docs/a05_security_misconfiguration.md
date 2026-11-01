# A05:2021 - Security Misconfiguration

Security Misconfiguration terjadi ketika sistem, framework, server, atau layanan cloud dikonfigurasi dengan tidak aman.

Contoh: kredensial default yang tidak diganti, fitur atau port yang tidak diperlukan masih aktif, pesan error yang menampilkan stack trace atau detail internal kepada pengguna, header keamanan HTTP yang hilang, dan bucket penyimpanan cloud yang bersifat publik.

Kredensial default berbahaya karena nilainya diketahui publik, sehingga penyerang bisa langsung masuk. Stack trace tidak boleh ditampilkan ke pengguna karena membocorkan struktur kode, versi library, dan path server.

Pencegahan: lakukan hardening, buat proses konfigurasi yang berulang dan otomatis, pasang hanya komponen yang diperlukan, tinjau konfigurasi secara berkala, dan aktifkan header keamanan.
