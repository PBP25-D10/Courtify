# COURTIFY – PBP D10
---

## 👥 **Anggota Kelompok**

| No | Nama Lengkap        | NIM | Peran / Modul                               |
| -- | ------------------- | --- | ------------------------------------------- |
| 1  | **Rafa Rally Soelistiono**    | 2406344675   | Modul 1 – Autentikasi & Role Management     |
| 2  | **Wildan Al Rizka Yusuf** | 2406407083   | Modul 2 – Booking Lapangan                  |
| 3  | **Justin Timothy Wirawan**   |  2406413981  | Modul 3 – Manajemen Lapangan (Admin Tempat) |
| 4  | **Msy. Aulya Salsabila Putri**  | 2406353364  | Modul 4 – Social Invite & Komunitas         |
| 5  | **Khayra Tazkiya**    | 2406428876   | Modul 5 – Dashboard Admin |

---

## **Deskripsi Aplikasi**

**Courtify** merupakan aplikasi web berbasis **Django** yang dirancang untuk memudahkan user dalam melakukan **pemesanan lapangan olahraga secara online** dan membangun **komunitas bermain bersama**.

Melalui platform ini:

* Pengguna (*User*) dapat **mencari, memesan, dan bergabung bermain** dengan pemain lain secara mudah.
* Pemilik tempat (*Penyedia Lapangan*) dapat **mengatur jadwal dan mengelola lapangan** secara efisien.
* Sistem juga dilengkapi **dashboard** untuk memastikan performa aplikasi dan menentukan arah proses bisnis kedepannya.

### **Tujuan & manfaat**

* Mempercepat proses dalam transaksi dan booking tempat.
* Meningkatkan relasi dan hubungan antara sesama penyuka olahraga.
* Mempermudah penyedia lapangan dalam manajemen wwaktu dan alokasi tempat.
* Menyediakan dashboard bagi super admin untuk memberikan insight dan model bisnis yang tepat.

---

## **Daftar Modul yang Diimplementasikan**

---

### 1. Modul Autentikasi & Role Management

**Penanggung Jawab:** Rafa Rally Soelistiono

**Models:**

* UserProfile

  * user 
  * role (user, penyedia, admin)
  * phone
  * address
  * birth_date
  * profile_picture (ImageField)

**Views:**

* register_view() : form registrasi user & penyedia
* login_view() : proses login & redirect berdasarkan role
* logout_view() : logout pengguna
* profile_view() : menampilkan & mengubah profil pengguna

**Templates:**

* register.html
* login.html
* profile.html
* base.html, header.html, footer.html (basic root templates)

**AJAX:**

* Validasi username & email unik saat registrasi
* Update data profil dan penambahan akun

**Filter Pengguna:**

* Data pribadi (alamat, nomor HP, tanggal lahir) hanya dapat dilihat oleh user yang sudah login

---

### 2. Modul Booking Lapangan

**Penanggung Jawab:** Wildan Al Rizka Yusuf

**Models:**

* Booking

  * user (Fk : UserProfile)
  * lapangan (Fk : Lapangan)
  * tanggal
  * jam_mulai
  * jam_selesai
  * total_harga
  * status (pending, confirmed, cancelled)
  * created_at

**Views:**

* booking_list_view() : menampilkan daftar lapangan dengan filter (harga, lokasi, kategori)
* booking_create_view() : form pemesanan lapangan
* booking_history_view() : menampilkan riwayat booking milik user
* cancel_booking_view() : membatalkan pemesanan

**Templates:**

* booking_list.html
* booking_form.html
* booking_history.html

**AJAX:**

* Mengecek ketersediaan slot waktu lapangan tanpa reload halaman
* Konfirmasi atau pembatalan booking tanpa reload halaman

**Filter Pengguna:**

* Hanya user login yang dapat melakukan booking
---

### 3. Modul Manajemen Lapangan (Admin Tempat)

**Penanggung Jawab:** Justin Timothy Wirawan

**Models:**

* Lapangan

  * penyedia (Fk : UserProfile)
  * nama
  * kategori
  * lokasi
  * harga_per_jam
  * fasilitas
  * foto
  * jam_buka
  * jam_tutup
  * rating

* JadwalLapangan

  * lapangan (Fk : Lapangan)
  * hari
  * jam
  * status (tersedia / tidak)

**Views:**

* lapangan_create_view() : form tambah lapangan
* lapangan_edit_view() : ubah/update data lapangan
* lapangan_delete_view() : hapus lapangan
* lapangan_list_owner_view() : menampilkan daftar lapangan milik penyedia

**Templates:**

* lapangan_form.html
* lapangan_list_owner.html
* lapangan_detail.html

**AJAX:**

* Update status ketersediaan lapangan tanpa reload halaman

**Filter Pengguna:**

* Hanya penyedia lapangan yang dapat mengakses modul ini
---

### 4. Modul Social Invite & Komunitas

**Penanggung Jawab:** *Msy. Aulya Salsabila Putri

**Models:**

* Join Permainan

  * pengirim (Fk : UserProfile)
  * penerima (Fk : UserProfile)
  * booking (Fk : Booking, nullable)
  * status (pending, accepted, declined)

* Message

  * pengirim (Fk : UserProfile)
  * isi_pesan
  * timestamp

**Views:**

* online_users_view() : menampilkan daftar user yang sedang online
* send_invite_view() : mengirim undangan bermain
* private_chat_view() → menampilkan ruang obrolan dan daftar pesan

**Templates:**

* online_users.html
* chat_room.html
  Desain interaktif dengan layout grid dan include untuk komponen seperti sidebar dan daftar user

**AJAX:**

* Mengirim dan menerima pesan tanpa reload
* Update status online user

**Filter Pengguna:**

* Hanya user login yang dapat melihat dan mengirim undangan

---

### 5. Modul Dashboard & Deployment Monitoring

**Penanggung Jawab:** Khayra Tazkiya

**Models:**

* SystemLog

  * user
  * action
  * detail
  * created_at
  * level (INFO, WARNING, ERROR)

**Views:**

* admin_dashboard_view() : menampilkan total user, booking, lapangan, dan log sistem
* owner_dashboard_view() : menampilkan statistik booking dan pendapatan penyedia
* user_dashboard_view() : menampilkan ringkasan aktivitas user

**Templates:**

* dashboard_admin.html
* dashboard_owner.html
* dashboard_user.html

**AJAX:**

* Refresh data log dan grafik tanpa reload halaman

**Filter Pengguna:**

* Admin: melihat log sistem & status server
* Penyedia: melihat performa lapangan & statistik pendapatan
* User: melihat aktivitas pribadi & histori booking

---

## **Sumber Initial Dataset**

Dataset awal diambil dari beberapa sumber publik untuk kategori **lapangan olahraga**:

* **Kategori utama produk:** lapangan olahraga : futsal, basket, tenis, padel, badminton
* **Sumber dataset awal:**

  * Data hasil scrapping website oleh internal kelompok untuk nama lapangan, jam booking, harga, jadwal, dan fasilitas lapangan.


---

## 👤 **Role dan Deskripsi Pengguna**

| Role                          | Deskripsi                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **User (Pemain)**             | Dapat mencari lapangan, melakukan booking, mengundang pengguna lain, serta melihat riwayat pemesanan.        |
| **Penyedia Lapangan (Owner)** | Dapat menambahkan dan mengelola lapangan, mengatur jadwal, serta melihat laporan pemesanan.                  |
| **Admin**                     | Mengelola seluruh data aplikasi (user, penyedia, sistem log). |

---

## 🌐 **Tautan Deployment & Desain**

* **Tautan Deployment (PWS):** [link pws](https://courtify.cs.ui.ac.id)
* **Link Desain (Figma):** [link figma](https://www.figma.com/design)

---

