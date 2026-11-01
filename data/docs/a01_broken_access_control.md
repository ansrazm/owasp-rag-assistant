# A01:2021 - Broken Access Control

Broken Access Control terjadi ketika pengguna bisa mengakses data atau melakukan tindakan di luar hak aksesnya. Ini adalah risiko paling umum pada aplikasi web.

Contoh: mengubah ID di URL untuk melihat data pengguna lain (IDOR, Insecure Direct Object Reference), membuka halaman admin tanpa peran admin, memanipulasi token atau cookie, dan konfigurasi CORS yang terlalu longgar.

Pencegahan: terapkan prinsip deny by default (semua akses ditolak kecuali diizinkan secara eksplisit), lakukan pemeriksaan otorisasi di sisi server pada setiap request, pastikan setiap record hanya bisa diakses oleh pemiliknya, matikan directory listing, catat kegagalan akses, dan terapkan rate limiting pada API.
