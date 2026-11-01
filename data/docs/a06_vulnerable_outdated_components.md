# A06:2021 - Vulnerable and Outdated Components

Risiko ini muncul ketika aplikasi memakai library, framework, atau komponen yang sudah usang atau memiliki kerentanan publik (CVE) yang belum ditambal.

Contoh: memakai versi library lama yang celahnya sudah diketahui, tidak mengetahui versi komponen yang dipakai, dan tidak pernah memperbarui dependensi.

Cara mendeteksi dependensi yang punya celah keamanan: lakukan Software Composition Analysis (SCA) menggunakan alat seperti Dependabot, OWASP Dependency-Check, atau npm audit, dan simpan inventaris dependensi (SBOM).

Pencegahan: perbarui dependensi secara berkala, hapus dependensi yang tidak dipakai, ambil komponen hanya dari sumber resmi, dan pantau pengumuman kerentanan.
