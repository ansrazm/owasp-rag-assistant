# A03:2021 - Injection

Injection terjadi ketika data dari pengguna dikirim ke interpreter (database, shell, browser) sebagai bagian dari perintah, sehingga penyerang bisa mengeksekusi perintah yang tidak diinginkan. Jenisnya antara lain SQL injection, NoSQL injection, OS command injection, dan Cross-Site Scripting (XSS).

Contoh: query SQL yang disusun dengan menggabungkan string dari input pengguna, sehingga input seperti ' OR '1'='1 mengubah arti query.

Pencegahan: gunakan parameterized query atau prepared statement, gunakan ORM dengan benar, validasi input dengan allowlist, lakukan escape pada output (terutama HTML), dan berikan hak akses database seminimal mungkin (least privilege).
