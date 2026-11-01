# A10:2021 - Server-Side Request Forgery (SSRF)

SSRF terjadi ketika server mengambil sumber daya dari URL yang diberikan pengguna tanpa validasi yang cukup. Penyerang bisa membuat server mengirim request ke layanan internal yang tidak bisa diakses dari luar.

Contoh dampak: mengakses endpoint metadata cloud untuk mencuri kredensial, memindai port dan layanan di jaringan internal, serta membaca file lokal.

Pencegahan: validasi URL menggunakan allowlist domain, blokir alamat IP internal dan loopback, jangan mengembalikan respons mentah ke klien, nonaktifkan HTTP redirect, dan lakukan segmentasi jaringan agar server aplikasi tidak bisa menjangkau layanan sensitif.
