# A04:2021 - Insecure Design

Insecure Design adalah kelemahan pada rancangan atau arsitektur aplikasi, bukan sekadar bug pada kode. Aplikasi yang diimplementasikan dengan sempurna tetap tidak aman jika desainnya salah.

Contoh: alur pemulihan password yang memakai pertanyaan rahasia yang mudah ditebak, fitur pembelian tanpa batas jumlah sehingga bisa disalahgunakan (abuse of business logic), dan tidak adanya pemisahan antara data publik dan privat.

Pencegahan: lakukan threat modeling sejak tahap desain untuk mengidentifikasi ancaman dan cara penyerang menyalahgunakan fitur, gunakan pola desain aman (secure design pattern), tulis unit test dan integration test untuk skenario penyalahgunaan, pisahkan lapisan sistem, dan batasi penggunaan resource per pengguna.
