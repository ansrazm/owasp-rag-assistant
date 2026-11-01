# A09:2021 - Security Logging and Monitoring Failures

Tanpa pencatatan dan pemantauan yang memadai, serangan tidak terdeteksi atau baru ketahuan setelah lama berlalu.

Event yang perlu dicatat di log keamanan: login berhasil dan gagal, kegagalan kontrol akses, kegagalan validasi input, perubahan hak akses, dan transaksi bernilai tinggi. Log harus berisi cukup konteks (waktu, pengguna, alamat IP, aksi) untuk investigasi.

Pencegahan: gunakan format log yang konsisten dan terpusat, jangan mencatat data sensitif seperti password atau nomor kartu, pasang alert untuk aktivitas mencurigakan, lindungi log dari perubahan, dan siapkan rencana incident response.
