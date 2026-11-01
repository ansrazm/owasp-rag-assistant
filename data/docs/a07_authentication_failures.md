# A07:2021 - Identification and Authentication Failures

Risiko ini terjadi ketika proses identifikasi, autentikasi, atau pengelolaan sesi pengguna lemah sehingga penyerang bisa mengambil alih akun.

Contoh: serangan brute force dan credential stuffing (penyerang mencoba pasangan username dan password yang bocor dari situs lain), mengizinkan password lemah, tidak ada multi-factor authentication (MFA), dan session ID yang tidak dibatalkan setelah logout.

Session harus dibatalkan saat logout agar token yang dicuri tidak bisa dipakai lagi.

Pencegahan: aktifkan MFA, terapkan rate limiting dan penguncian akun sementara, terapkan kebijakan password yang kuat dan cek terhadap daftar password bocor, gunakan session ID acak yang dibatalkan saat logout dan saat timeout.
