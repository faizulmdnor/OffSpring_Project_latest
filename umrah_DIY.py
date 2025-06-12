import pandas as pd

# Sheet 1: Itinerary (Summary version)
itinerary_data = {
    "Hari": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Lokasi": ["Perjalanan ke Madinah", "Madinah", "Madinah", "Madinah", "Madinah ke Mekah & Umrah", "Mekah", "Mekah", "Mekah", "Mekah & Pulang", "Tiba di Malaysia"],
    "Aktiviti Utama": [
        "Flight ke Madinah, check-in hotel, rehat",
        "Solat Subuh di Masjid Nabawi, Ziarah Raudhah & Makam Rasulullah ﷺ, Santai kawasan masjid",
        "Lawatan Jabal Uhud, Masjid Quba, Masjid Qiblatain, Pasar Kurma",
        "Rehat, solat jemaah, beli barang keperluan",
        "Pakaian ihram, niat umrah di Bir Ali, perjalanan ke Mekah, umrah pertama",
        "Solat di Masjidil Haram, lawatan Bukit Safa & Marwah, beli cenderahati",
        "Lawatan Jabal Nur, Jabal Tsur, Padang Arafah, Mina, Muzdalifah",
        "Solat, santai, umrah kedua (jika mampu)",
        "Solat Subuh terakhir, beli oleh-oleh, check-out, ke Jeddah Airport",
        "Tiba di Malaysia, rehat, catat pengalaman"
    ],
    "Nota": [
        "Pastikan anak cukup rehat dan makan",
        "Tempahan Raudhah melalui app Nusuk, lelaki & wanita berasingan",
        "Sewa MPV 4 jam untuk ziarah",
        "Sediakan masa santai untuk anak-anak",
        "Beli tiket keretapi Haramain untuk ke Mekah",
        "Ulang kaji Sa'i & bawa anak ikut keselesaan",
        "Boleh ziarah Masjid Ja'ranah untuk umrah kedua",
        "Jangan paksa anak jika letih",
        "Pastikan semua barang siap, check-out awal",
        "Kongsi pengalaman dan doa bersama keluarga"
    ]
}
df_itinerary = pd.DataFrame(itinerary_data)

# Sheet 2: Budget (with homestay and train)
budget_data = {
    "Komponen": [
        "Tiket Penerbangan (KL - Madinah / Jeddah - KL)",
        "Homestay Madinah (4 malam)",
        "Homestay Mekah (4 malam)",
        "Keretapi Laju Haramain (Madinah → Mekah)",
        "Transport lain (airport + ziarah)",
        "Visa Umrah + Insurans",
        "Makanan & Minuman (boleh masak sendiri)",
        "Umrah kit (ihram, kasut tawaf, dll)",
        "Cenderahati & Oleh-oleh",
        "Simcard Internet Arab Saudi",
        "Caj bagasi tambahan"
    ],
    "Kiraan": [
        "RM2,800 x 2 dewasa; RM2,500 x 4 anak (diskaun minor)",
        "RM400/malam x 4 malam",
        "RM450/malam x 4 malam",
        "2 dewasa + 4 anak, kelas ekonomi",
        "Ringkas (airport + ziarah)",
        "RM700 x 6 orang",
        "RM50/hari x 10 hari x 6 orang",
        "RM150 x 6 orang",
        "Anggaran bebas",
        "RM80 x 2 simcard",
        "Anggaran"
    ],
    "Anggaran (RM)": [
        15800,
        1600,
        1800,
        880,
        1200,
        4200,
        3000,
        900,
        600,
        160,
        300
    ]
}
df_budget = pd.DataFrame(budget_data)

# Sheet 3: Checklist Document (Umrah DIY)
checklist_document_data = {
    "Dokumen": [
        "Pasport dengan visa Umrah",
        "Tiket penerbangan pergi balik",
        "Tempahan hotel/homestay Madinah & Mekah",
        "Tiket keretapi Haramain (jika guna)",
        "Insurans perjalanan",
        "Surat kebenaran sekolah anak (jika perlu)",
        "Rekod kesihatan / vaksinasi COVID-19",
        "Salinan kad pengenalan / passport setiap ahli keluarga",
        "Resit pembayaran dan dokumen penting lain"
    ],
    "Catatan": [
        "Pastikan pasport masih sah sekurang-kurangnya 6 bulan",
        "Simpan dalam telefon & cetak salinan",
        "Pastikan tempahan boleh dibatalkan jika perlu",
        "Tempah awal untuk dapat harga lebih baik",
        "Untuk keselamatan dan keperluan perubatan",
        "Jika anak masih sekolah",
        "Pastikan lengkap mengikut syarat Saudi",
        "Untuk urusan imigresen dan kecemasan",
        "Simpan dalam fail khas perjalanan"
    ]
}
df_checklist_doc = pd.DataFrame(checklist_document_data)

# Sheet 4: Checklist Barang (Packing List Umrah DIY)
checklist_barang_data = {
    "Barang": [
        "Pakaian ihram (2 dewasa + 4 anak lelaki jika perlu)",
        "Pakaian biasa untuk anak-anak dan isteri",
        "Kasut selesa untuk tawaf",
        "Telekung untuk wanita",
        "Sejadah kecil",
        "Masker muka & sanitizer",
        "Beg sandang kecil (untuk barang penting)",
        "Alat solat (tasbih, buku doa, Al-Quran kecil)",
        "Ubat-ubatan peribadi & kit kecemasan",
        "Bekalan makanan ringan / kurma",
        "Botol air kosong untuk refill",
        "Powerbank & charger telefon",
        "Dokumen perjalanan & salinan pasport",
        "Camera / telefon untuk dokumentasi",
        "Kain pelikat / sarung bantal kecil (anak-anak tidur)"
    ],
    "Nota": [
        "Pastikan cukup untuk setiap ahli keluarga",
        "Bawa pakaian mengikut cuaca dan jumlah hari",
        "Elakkan kasut baru untuk elak sakit kaki",
        "Bawa telekung ringan mudah dibawa",
        "Untuk solat di luar masjid",
        "Untuk lindungi diri dan elak jangkitan",
        "Mudah akses barang penting semasa berjalan",
        "Baca doa dan zikir dengan anak-anak",
        "Bawa ubat demam, sakit kepala, plester, balm",
        "Senang beri tenaga dan elak lapar",
        "Boleh isi air zam-zam di masjid",
        "Pastikan bateri penuh untuk komunikasi",
        "Sentiasa bawa untuk rujukan dan urusan",
        "Untuk rakam kenangan dan aktiviti keluarga",
        "Untuk tidur lebih selesa di homestay"
    ]
}
df_checklist_barang = pd.DataFrame(checklist_barang_data)

# Save to Excel with multiple sheets
file_path = 'E:/data/Umrah_DIY_Keluarga_Faizul.xlsx'
with pd.ExcelWriter(file_path) as writer:
    df_itinerary.to_excel(writer, sheet_name='Itinerary', index=False)
    df_budget.to_excel(writer, sheet_name='Budget', index=False)
    df_checklist_doc.to_excel(writer, sheet_name='Checklist_Document', index=False)
    df_checklist_barang.to_excel(writer, sheet_name='Checklist_Barang', index=False)

file_path
