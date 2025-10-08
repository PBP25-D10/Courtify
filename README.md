# COURTIFY – PBP D10
---

## 👥 **Anggota Kelompok**

| No | Nama Lengkap        | NIM | Peran / Modul                               |
| -- | ------------------- | --- | ------------------------------------------- |
| 1  | **Rafa Rally Soelistiono**    | 2406344675   | Modul 1,6 – Autentikasi & Role Management & Wishlist    |
| 2  | **Wildan Al Rizka Yusuf** | 2406407083   | Modul 2 – Booking Lapangan                  |
| 3  | **Justin Timothy Wirawan**   |  2406413981  | Modul 3 – Manajemen Lapangan (Admin Tempat) |
| 4  | **Msy. Aulya Salsabila Putri**  | 2406353364  | Modul 5 – Iklan         |
| 5  | **Khayra Tazkiya**    | 2406428876   | Modul 4 – Artikel Berita |

---

## **Deskripsi Aplikasi**

**Courtify** merupakan aplikasi web berbasis **Django** yang dirancang untuk memudahkan user dalam melakukan **pemesanan lapangan olahraga secara online** dan membangun **komunitas bermain bersama**.

Melalui platform ini:

* Pengguna (*User*) dapat **mencari, memesan, dan bergabung bermain** dengan pemain lain secara mudah.
* Pemilik tempat (*Penyedia Lapangan*) dapat **mengatur jadwal dan mengelola lapangan** secara efisien.

### **Tujuan & manfaat**

* Mempercepat proses dalam transaksi dan booking tempat.
* Meningkatkan relasi dan hubungan antara sesama penyuka olahraga.
* Mempermudah penyedia lapangan dalam manajemen wwaktu dan alokasi tempat.

---

## **Daftar Modul yang Diimplementasikan**

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

* Update data profil dan penambahan akun tanpa perlu reload halaman

**Filter Pengguna:**


* hanya dapat dilihat oleh user yang sudah login

---

### 2. Modul Booking Lapangan

**Penanggung Jawab:** Wildan Al Rizka Yusuf

**Models:**

* Booking

  * tanggal
  * id booking
  * jam_mulai
  * jam_selesai
  * total_harga
  * status (pending, confirmed, cancelled)
  * created_at

**Views:**

* booking_list_view() : menampilkan daftar lapangan
* booking_create_view() : form pemesanan lapangan
* cancel_booking_view() : membatalkan pemesanan
* update_booking_view() : update tanggal pemesanan


**Templates:**

* booking_list.html
* booking_form.html
* booking_history.html

**AJAX:**

* CRUD booking tanpa reload halaman

**Filter Pengguna:**

* Hanya user login yang dapat melakukan booking
---

### 3. Modul Manajemen Lapangan (Admin Tempat)

**Penanggung Jawab:** Msy. Aulya Salsabila Putri

**Models:**

* Lapangan

  * id lapangan
  * nama
  * deskripsi
  * kategori
  * lokasi
  * harga_per_jam
  * foto
  * jam_buka
  * jam_tutup

**Views:**

* lapangan_create_view() : form tambah lapangan
* lapangan_edit_view() : ubah/update data lapangan
* lapangan_delete_view() : hapus lapangan
* lapangan_list_view() : menampilkan daftar lapangan milik penyedia

**Templates:**

* lapangan_form.html
* lapangan_list_owner.html
* lapangan_detail.html

**AJAX:**

* CRUD lapangan tanpa reload halaman

**Filter Pengguna:**

* Hanya penyedia lapangan yang dapat mengakses modul ini

---

### 4. Modul Artikel Olahraga

**Penanggung Jawab:** Khayra Tazkiya

**Models:**

* News

  * id berita
  * title
  * content
  * kategori
  * thumbnail
  * created_at

**Views:**

* news_create_view() : form tambah berita
* news_edit_view() : ubah/update data berita
* news_delete_view() : hapus berita
* news_list_view() : menampilkan daftar berita

**Templates:**

* berita_form.html
* berita_list_owner.html
* berita_detail.html

**AJAX:**

* CRUD news olahraga tanpa reload halaman

**Filter Pengguna:**

* Hanya penyedia lapangan yang dapat mengakses modul ini dan buat form dalam modal.
* Bisa dilihat oleh user

---

### 5. Modul Iklan

**Penanggung Jawab:** Msy. Aulya Salsabila Putri

**Models:**

* Iklan

  * host
  * lapangan
  * date
  * banner

**Views:**

* iklan_create_view() : form tambah iklan
* iklan_edit_view() : ubah/update data iklan
* iklan_delete_view() : hapus iklan
* iklan_list_view() : menampilkan daftar iklan

**Templates:**

* iklan_form.html
* iklan_list_owner.html

**AJAX:**

* CRUD iklan tanpa reload halaman dan modal

**Filter Pengguna:**

* Hanya penyedia lapangan yang dapat mengakses modul ini

---

### 6. Modul Wishlist

**Penanggung Jawab:** Rafa Rally Soelistiono

**Models:**

* Wishlist

  * user
  * lapangan
  * added_on

**Views:**

* wishlist_create_view() : tambah wishlist
* wishlist_delete_view() : hapus wishlist
* wishlist_list_view() : menampilkan daftar wishlist user

**Templates:**

* wishlist.html

**AJAX:**

* CRUD wishlist tanpa reload halaman

**Filter Pengguna:**

* Hanya user yang dapat mengakses modul ini

---

## **Sumber Initial Dataset**

Dataset awal diambil dari beberapa sumber publik untuk kategori **lapangan olahraga**:

* **Kategori utama produk:** lapangan olahraga : futsal, basket, tenis, padel, badminton
* **Sumber dataset awal:**

  * **tautan dataset :** [link dataset](https://opendata.jabarprov.go.id/id/dataset/jumlah-fasilitaslapangan-olahraga-berdasarkan-kategori-dan-desakelurahan-di-jawa-barat)


---

## 👤 **Role dan Deskripsi Pengguna**

| Role                          | Deskripsi                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **User (Pemain)**             | Dapat mencari lapangan, melakukan booking, mengundang pengguna lain, serta melihat riwayat pemesanan.        |
| **Penyedia Lapangan (Owner)** | Dapat menambahkan dan mengelola lapangan, mengatur jadwal, serta melihat laporan pemesanan.                  |


---

## 🌐 **Tautan Deployment & Desain**

* **Tautan Deployment (PWS):** [link pws](https://justin-timothy-courtify.pbp.cs.ui.ac.id/)
* **Link Desain (Figma):** [link figma](https://www.figma.com/design/WFXPpXYAMJKiQBmJfbklMn/PBP-COURTIFY?node-id=0-1&t=oJticVyhsjIw0hyG-1)

---

