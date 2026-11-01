# A02:2021 - Cryptographic Failures

Cryptographic Failures adalah kegagalan melindungi data sensitif, baik saat dikirim (in transit) maupun saat disimpan (at rest). Dampaknya adalah kebocoran data pribadi, kredensial, atau data pembayaran.

Contoh: data dikirim lewat HTTP tanpa enkripsi, memakai algoritma lemah seperti MD5, SHA-1, atau DES, menaruh kunci enkripsi langsung di kode, dan menyimpan password tanpa hashing.

Pencegahan: gunakan TLS untuk semua koneksi, enkripsi data sensitif saat disimpan dengan algoritma modern seperti AES-GCM, simpan password dengan hash khusus seperti bcrypt atau Argon2 yang diberi salt, kelola kunci dengan aman di secret manager, dan jangan menyimpan data sensitif yang tidak diperlukan.
