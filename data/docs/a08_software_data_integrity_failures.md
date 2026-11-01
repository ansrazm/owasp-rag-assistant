# A08:2021 - Software and Data Integrity Failures

Risiko ini terjadi ketika aplikasi mempercayai kode atau data tanpa memverifikasi integritasnya. Contohnya pembaruan perangkat lunak tanpa verifikasi tanda tangan, pipeline CI/CD yang mudah disusupi, deserialisasi data yang tidak aman, dan dependensi dari sumber yang tidak tepercaya.

Untuk memastikan webhook tidak dipalsukan, penerima harus memverifikasi signature. Pengirim menghitung HMAC-SHA256 dari isi request dengan secret bersama, lalu penerima menghitung ulang dan membandingkannya dengan header signature. Request dengan signature yang salah ditolak (misalnya dengan status 401).

Pencegahan: gunakan tanda tangan digital atau checksum untuk memverifikasi kode dan data, tinjau perubahan kode, amankan CI/CD dengan kontrol akses yang ketat, dan hindari deserialisasi data yang tidak tepercaya.
