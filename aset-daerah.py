import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="SIMDA Aset Dummy", layout="wide")


# ------------------------
# INIT SESSION STATE
# ------------------------
def init_state():
    if "aset" not in st.session_state:
        # Dummy data aset (sengaja ada keanehan untuk bahan audit & migration)
        csv_text = """kode_aset,nama_aset,nilai_aset,skpd,status
AST-001,Komputer Ruang Rapat,7500000,Dinas Keuangan,aktif
AST-002,Printer Lantai 2,,Dinas Pendidikan,aktif
AST-003,Kursi Rapat,1500000,,aktif
AST-004,AC Ruang Server,abc,Dinas Kominfo,aktif
AST-005,,2000000,Dinas Kesehatan,aktif
AST-006,Server Aplikasi,25000000,Dinas Kominfo,rusak
AST-007,Meja Pegawai,-500000,Dinas Pendidikan,aktif
"""
        st.session_state.aset = pd.read_csv(StringIO(csv_text))

    if "gl_total_aset" not in st.session_state:
        # Total aset di general ledger (sengaja beda untuk bahan rekonsiliasi)
        st.session_state.gl_total_aset = 70000000  # angka "resmi" GL (dummy)

    if "audit_findings" not in st.session_state:
        st.session_state.audit_findings = []

    if "pir_notes" not in st.session_state:
        st.session_state.pir_notes = []


init_state()


# ------------------------
# HELPERS
# ------------------------
def format_rupiah(x):
    try:
        x = float(x)
        return f"Rp {x:,.0f}".replace(",", ".")
    except Exception:
        return str(x)


def analyze_data_quality(df: pd.DataFrame):
    """Kembalikan list isu kualitas data (untuk migration & auditor)."""
    issues = []

    if df["nama_aset"].isna().any():
        issues.append("Ada aset yang **nama_aset**-nya kosong.")
    if df["nilai_aset"].isna().any():
        issues.append("Ada aset yang **nilai_aset**-nya kosong.")
    # nilai tidak numeric
    non_numeric_mask = pd.to_numeric(df["nilai_aset"], errors="coerce").isna()
    if non_numeric_mask.any():
        issues.append("Ada **nilai_aset** yang bukan angka (contoh: 'abc').")
    # nilai negatif
    numeric_vals = pd.to_numeric(df["nilai_aset"], errors="coerce")
    if (numeric_vals < 0).any():
        issues.append("Ada **nilai_aset** negatif (contoh: -500000).")
    # SKPD kosong
    if df["skpd"].isna().any():
        issues.append("Ada aset tanpa informasi **SKPD**.")

    return issues


# ------------------------
# SIDEBAR: PILIH ROLE
# ------------------------
st.sidebar.title("SIMDA Aset – Roleplay Pertemuan 4")
role = st.sidebar.radio(
    "Pilih Peran Kelompok",
    [
        "1. Vendor Pemenang",
        "2. User – Petugas Entri Aset",
        "3. User – Pengelola Aset SKPD",
        "4. User – Keuangan / Akuntansi",
        "5. Auditor",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Aplikasi dummy untuk kuliah Audit Sistem Informasi.\n"
    "Data & fitur sengaja dibuat tidak sempurna untuk bahan diskusi readiness, migration, dan PIR."
    "PS: Tidak ada aplikasi sesederhana ini di dunia nyata ya 😄."
    "\n\n- Reza"
)


# ------------------------
# ROLE 1 – VENDOR PEMENANG
# ------------------------
if role == "1. Vendor Pemenang":
    st.title("Kelompok 1 – Vendor Pemenang")

    st.markdown(
        """
### 🎤 Tugas Vendor Pemenang
Kelompok ini harus **mem-presentasikan solusi SIMDA Aset** kepada user & auditor, dengan fokus:

1. **Modul & Status Pengembangan**  
2. **Readiness Strategy (kesiapan implementasi)**  
3. **Migration Strategy (strategi migrasi data)**  
4. **Menjelaskan error / kelemahan aplikasi kepada user** dan rencana perbaikan.
"""
    )

    col1, col2 = st.columns(2)

    # Modul & status
    with col1:
        st.subheader("📦 Modul SIMDA Aset (Versi Vendor)")
        st.markdown(
            """
- Modul Input & Inventaris Aset  
- Modul Mutasi & Penghapusan Aset  
- Modul Laporan Aset per SKPD  
- Modul Rekonsiliasi dengan GL  
- Modul Dashboard Manajemen  
- Integrasi dengan SIMDA Keuangan (direncanakan)  
"""
        )

        st.subheader("📊 Status Pengembangan (Self-Reported)")
        dev_status = pd.DataFrame(
            [
                {"Modul": "Input & Inventaris", "Status": "Selesai 100%"},
                {"Modul": "Mutasi & Penghapusan", "Status": "80%"},
                {"Modul": "Laporan Aset per SKPD", "Status": "70%"},
                {"Modul": "Rekonsiliasi GL", "Status": "50%"},
                {"Modul": "Integrasi SIMDA Keu", "Status": "Dalam Perencanaan"},
            ]
        )
        st.table(dev_status)

    # Readiness & migration story
    with col2:
        st.subheader("✅ Readiness Strategy (contoh poin yang bisa dijelaskan)")
        st.markdown(
            """
- Environment **testing** sudah tersedia  
- dst
"""
        )
        st.subheader("🚚 Migration Strategy (contoh narasi)")
        st.markdown(
            """
- Data lama diambil dari file Excel / sistem lama  
- dst
"""
        )

    st.markdown("---")
    st.subheader("🧩 Contoh Error / Kelemahan yang Harus Dijelaskan Vendor")

    df = st.session_state.aset.copy()
    issues = analyze_data_quality(df)
    # if issues:
    #     st.write("Kualitas data awal (sebelum migrasi) mengandung masalah, misalnya:")
    #     for i in issues:
    #         st.write("•", i)
    # else:
    #     st.write("Saat ini tidak terdeteksi masalah data (untuk dummy ini).")

    st.info(
        "Vendor diminta menjelaskan kepada user & auditor: "
        "mengapa hal-hal ini bisa terjadi, risiko bisnisnya, dan rencana perbaikannya."
    )


# ------------------------
# ROLE 2 – USER: PETUGAS ENTRI ASET
# ------------------------
elif role == "2. User – Petugas Entri Aset":
    st.title("Kelompok 2 – User: Petugas Entri Aset")

    st.markdown(
        """
### 🎯 Tugas Kelompok 2
- Mencoba fitur **input aset baru**  
- Mengamati form input  
- Menilai apakah sistem sudah mendukung pekerjaan entri aset dengan aman & akurat  
- Menyusun 2–3 rekomendasi perbaikan untuk Vendor
"""
    )

    st.subheader("Form Input Aset (Dummy)")

    col1, col2 = st.columns(2)
    with col1:
        kode = st.text_input("Kode Aset (contoh: AST-008)")
        nama = st.text_input("Nama Aset")
        nilai = st.text_input("Nilai Aset (angka)")
    with col2:
        skpd = st.text_input("SKPD (contoh: Dinas Kesehatan)")
        status = st.selectbox("Status Aset", ["aktif", "rusak", "dihapus"])

    if st.button("Simpan Aset"):
        # SENGAJA: tidak ada validasi nilai numeric, boleh kosong, dll.
        new_row = {
            "kode_aset": kode,
            "nama_aset": nama,
            "nilai_aset": nilai,
            "skpd": skpd,
            "status": status,
        }
        st.session_state.aset = pd.concat(
            [st.session_state.aset, pd.DataFrame([new_row])],
            ignore_index=True,
        )
        st.success(
            "Aset *seolah-olah* tersimpan. Perhatikan: tidak ada validasi apakah data benar atau tidak."
        )

    st.markdown("---")
    st.subheader("Daftar Aset (Termasuk yang Baru Diinput)")

    df = st.session_state.aset.copy()
    df["nilai_aset_format"] = df["nilai_aset"].apply(format_rupiah)
    st.dataframe(df, use_container_width=True)

    st.markdown(
        """
**Pertanyaan bantuan diskusi untuk Kelompok 2 untuk menjawab tugas:**
- Apa risiko jika validasi lemah seperti ini?  
- Kontrol aplikasi apa yang seharusnya ada di form input aset?
"""
    )


# ------------------------
# ROLE 3 – USER: PENGELOLA ASET SKPD
# ------------------------
elif role == "3. User – Pengelola Aset SKPD":
    st.title("Kelompok 3 – User: Pengelola Aset SKPD")

    st.markdown(
        """
### 🎯 Tugas Kelompok 3
- Menggunakan laporan aset per SKPD di aplikasi dummy  
- Mencari kejanggalan  
- Menilai apakah laporan bisa dijadikan dasar keputusan manajemen  
- Memberikan rekomendasi kontrol agar laporan SKPD dapat dipercaya
"""
    )

    df = st.session_state.aset.copy()

    skpd_list = ["(Semua SKPD)"] + sorted([s for s in df["skpd"].dropna().unique().tolist()])
    skpd_filter = st.selectbox("Filter SKPD", skpd_list)

    if skpd_filter != "(Semua SKPD)":
        df = df[df["skpd"] == skpd_filter]

    df["nilai_aset_format"] = df["nilai_aset"].apply(format_rupiah)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Daftar Aset")
        st.dataframe(df, use_container_width=True)
    with col2:
        st.subheader("Ringkasan Singkat")
        st.write("Jumlah baris data:", len(df))
        try:
            total = pd.to_numeric(df["nilai_aset"]).sum()
            st.write("Total nilai (hitung kasar):")
            st.write(format_rupiah(total))
        except Exception:
            st.error(
                "Tidak bisa menghitung total nilai aset karena ada data yang bukan angka."
            )

    st.markdown(
        """
**Pertanyaan diskusi untuk Kelompok 3:**

- Apa dampaknya?  
- Apakah laporan seperti ini bisa dipakai untuk audit atau laporan keuangan?  
- Kontrol apa yang perlu ada (baik di proses, maupun di aplikasi) agar laporan SKPD akurat?
"""
    )


# ------------------------
# ROLE 4 – USER: KEUANGAN / AKUNTANSI
# ------------------------
elif role == "4. User – Keuangan / Akuntansi":
    st.title("Kelompok 4 – User: Keuangan / Akuntansi")

    st.markdown(
        """
### 🎯 Tugas Kelompok 4
- Melihat **ringkasan nilai aset menurut aplikasi**  
- Membandingkan dengan **saldo aset di General Ledger (GL)**  
- Mengidentifikasi penyebab selisih  
- Menyusun rekomendasi prosedur rekonsiliasi & kontrol yang diperlukan
"""
    )

    df = st.session_state.aset.copy()

    st.subheader("Ringkasan Nilai Aset Menurut Aplikasi (SIMDA Dummy)")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Tampilan data mentah:")
        st.dataframe(df, use_container_width=True)
    with col2:
        st.write("Percobaan menghitung total aset:")

        try:
            df_num = pd.to_numeric(df["nilai_aset"])
            total_simda = df_num.sum()
            st.success(f"Total menurut SIMDA Aset (hanya baris valid): {format_rupiah(total_simda)}")
        except Exception:
            # Jika ada error, coba drop yang tidak numeric
            df_num = pd.to_numeric(df["nilai_aset"], errors="coerce")
            total_simda = df_num.sum()
            st.warning(
                "Terdapat nilai aset yang bukan angka. Baris tersebut diabaikan "
                "saat menghitung total."
            )
            st.write(f"Total setelah abaikan nilai tidak valid: {format_rupiah(total_simda)}")

    st.markdown("---")
    st.subheader("Saldo Aset Menurut GL (Dummy)")
    gl_total = st.session_state.gl_total_aset
    st.write("Saldo Aset (GL):", format_rupiah(gl_total))

    selisih = gl_total - total_simda
    st.write("Selisih GL - SIMDA Aset:", format_rupiah(selisih))

    if selisih != 0:
        st.error("⚠ Ada selisih antara GL dan SIMDA Aset (ini bahan rekonsiliasi).")
    else:
        st.success("Tidak ada selisih antara GL dan SIMDA Aset (jarang terjadi di dunia nyata 😄).")

    st.markdown(
        """
**Pertanyaan diskusi untuk Kelompok 4:**

- Apa kemungkinan penyebab selisih antara GL dan aplikasi?  
- Bagaimana prosedur rekonsiliasi aset seharusnya dilakukan?  
- Kontrol apa yang perlu diterapkan agar nilai aset di GL & SIMDA konsisten dan dapat diaudit?
"""
    )


# ------------------------
# ROLE 5 – AUDITOR
# ------------------------
elif role == "5. Auditor":
    st.title("Kelompok 5 – Auditor")

    st.markdown(
        """
### 🎯 Tugas Kelompok 5
Sebagai auditor sistem informasi, Anda diminta melakukan audit readiness, migration, dan post-implementation review (PIR) terhadap implementasi SIMDA Aset ini.
Hasil audit anda akan digunakan untuk memberikan rekomendasi apakah sistem ini siap digunakan, bagaimana proses migrasi data, serta evaluasi awal setelah implementasi.

### 📋 Langkah Audit, pastikan:
1. **Readiness** – apakah sistem dan data siap go-live?  
2. **Migration Controls** – apakah kualitas data & proses migrasi memadai?  
3. **Post-Implementation Review (PIR)** – masalah yang muncul & rekomendasi perbaikan.  
4. **Procurement Findings** – catatan terkait proses pengadaan sistem.
5. **Menyusun temuan audit** berdasarkan analisis di atas.
"""
    )

    df = st.session_state.aset.copy()

    # 1. Readiness overview
    st.subheader("1) Readiness Overview")
    st.markdown(
        """
        Pertanyaan panduan audit:
- Apakah data aset sudah lengkap & akurat untuk go-live?  
- Apakah ada kontrol validasi data di aplikasi?
- Apakah user sudah siap menggunakan sistem ini?
- Apakah vendor sudah menyelesaikan pengembangan sesuai kontrak?
"""
    )

    # 2. Migration / data quality
    st.markdown("---")
    st.subheader("2) Migration & Data Quality Issues")
    st.markdown(
        """
**Pertanyaan panduan audit:**

- Jika data seperti ini langsung dimigrasikan, apa risikonya?  
- Kontrol apa yang seharusnya ada dalam proses migrasi (cleansing, validation, reconciliation, sign-off)?  
"""
    )

    # 3. PIR – catatan setelah sistem digunakan
    st.markdown("---")
    st.subheader("3) Post-Implementation Review (PIR)")

    st.markdown(
        """
 **Temuan PIR**, misalnya:

- Keluhan user (input susah, laporan tidak akurat)  
- Error di aplikasi (nilai tidak bisa dihitung, data hilang)  
- Manfaat yang belum tercapai  

Anda bisa menganggap temuan PIR ini berbasis cerita dari User & Vendor saat roleplay.
"""
    )

    # 4. Procurement findings
    st.markdown("---")
    st.subheader("4) Procurement Findings")
    st.markdown(
        """
**Catatan audit terkait proses pengadaan sistem**, misalnya: apakah sudah sesuai prosedur, apakah ada potensi konflik kepentingan, dsb.
"""
    )