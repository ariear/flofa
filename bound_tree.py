import cairo

WIDTH = 600
HEIGHT = 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)

context = cairo.Context(surface)

# --- Gambar Batang Pohon ---

# Definisikan 3 warna coklat buat batang pohon
# Angka dibagi 255 karena Cairo pakai skala 0-1, bukan 0-255
dark_brown = (88/255, 60/255, 34/255)      # Coklat gelap buat bayangan
medium_brown = (120/255, 80/255, 45/255)   # Coklat sedang buat warna utama
light_brown = (150/255, 100/255, 60/255)   # Coklat terang buat highlight

# Simpan status konteks sekarang (biar bisa di-restore nanti)
# Kayak save game sebelum kita mulai gambar
context.save()

# BAGIAN 1: Gambar batang utama dengan warna coklat sedang
context.set_source_rgb(*medium_brown)  # Set warna kuas ke coklat sedang
context.move_to(WIDTH * 0.45, HEIGHT * 0.9)  # Mulai dari kiri bawah batang
# Buat kurva pertama: dari bawah ke tengah atas batang
context.curve_to(WIDTH * 0.4, HEIGHT * 0.7, WIDTH * 0.48, HEIGHT * 0.5, WIDTH * 0.5, HEIGHT * 0.45)
# Buat kurva kedua: dari tengah atas ke kanan bawah batang
context.curve_to(WIDTH * 0.52, HEIGHT * 0.5, WIDTH * 0.6, HEIGHT * 0.7, WIDTH * 0.55, HEIGHT * 0.9)
context.close_path()  # Tutup bentuk (kembali ke titik awal)
context.fill()  # Isi bentuk dengan warna

# BAGIAN 2: Gambar bayangan gelap di sisi kanan batang
context.set_source_rgb(*dark_brown)  # Set warna kuas ke coklat gelap
context.move_to(WIDTH * 0.5, HEIGHT * 0.45)  # Mulai dari tengah atas
# Buat garis kurva mengikuti sisi kanan batang
context.curve_to(WIDTH * 0.52, HEIGHT * 0.5, WIDTH * 0.6, HEIGHT * 0.7, WIDTH * 0.55, HEIGHT * 0.9)
context.line_to(WIDTH * 0.49, HEIGHT * 0.9)  # Tarik garis lurus ke kiri
# Buat kurva balik ke atas untuk menutup bentuk bayangan
context.curve_to(WIDTH * 0.58, HEIGHT * 0.7, WIDTH * 0.5, HEIGHT * 0.5, WIDTH * 0.49, HEIGHT * 0.46)
context.close_path()  # Tutup bentuk bayangan
context.fill()  # Isi dengan warna coklat gelap

# BAGIAN 3: Gambar highlight terang di sisi kiri batang
context.set_source_rgb(*light_brown)  # Set warna kuas ke coklat terang
context.move_to(WIDTH * 0.45, HEIGHT * 0.9)  # Mulai dari kiri bawah
# Buat kurva mengikuti sisi kiri batang (bagian yang kena cahaya)
context.curve_to(WIDTH * 0.42, HEIGHT * 0.8, WIDTH * 0.45, HEIGHT * 0.6, WIDTH * 0.48, HEIGHT * 0.48)
context.line_to(WIDTH * 0.49, HEIGHT * 0.5)  # Tarik garis ke tengah
# Buat kurva balik ke bawah untuk menutup bentuk highlight
context.curve_to(WIDTH * 0.47, HEIGHT * 0.6, WIDTH * 0.44, HEIGHT * 0.8, WIDTH * 0.47, HEIGHT * 0.9)
context.close_path()  # Tutup bentuk highlight
context.fill()  # Isi dengan warna coklat terang

# Kembalikan status konteks ke kondisi awal (sebelum save)
context.restore()

# --- Detail-detail Batang Pohon ---

# Warna coklat khusus buat detail tekstur kayu
dark_brown_detail = (70/255, 48/255, 20/255)    # Coklat gelap buat retakan kayu
light_brown_detail = (170/255, 115/255, 75/255)  # Coklat terang buat serat kayu

# Simpan status konteks lagi sebelum gambar detail
context.save()

# --- Gambar Detail Gelap (Retakan Kayu) ---
context.set_source_rgb(*dark_brown_detail)  # Set warna ke coklat gelap detail
context.set_line_width(2)  # Set ketebalan garis = 2 pixel

# Retakan kayu pertama: garis zig-zag di kanan batang
context.move_to(WIDTH * 0.51, HEIGHT * 0.55)  # Titik awal retakan
context.line_to(WIDTH * 0.53, HEIGHT * 0.65)  # Garis ke bawah-kanan
context.line_to(WIDTH * 0.52, HEIGHT * 0.75)  # Garis lanjut ke bawah
context.stroke()  # Gambar garisnya

# Retakan kayu kedua: garis lurus di kiri batang
context.move_to(WIDTH * 0.47, HEIGHT * 0.6)  # Titik awal
context.line_to(WIDTH * 0.46, HEIGHT * 0.7)  # Garis ke bawah
context.stroke()  # Gambar garisnya

# --- Gambar Detail Terang (Serat Kayu) ---
context.set_source_rgb(*light_brown_detail)  # Set warna ke coklat terang detail
context.set_line_width(1.5)  # Set ketebalan garis = 1.5 pixel (lebih tipis)

# Serat kayu pertama: diagonal di bagian atas kiri
context.move_to(WIDTH * 0.48, HEIGHT * 0.5)  # Titik awal
context.line_to(WIDTH * 0.46, HEIGHT * 0.6)  # Garis miring ke bawah-kiri
context.stroke()  # Gambar garisnya

# Serat kayu kedua: vertikal di bagian tengah
context.move_to(WIDTH * 0.50, HEIGHT * 0.68)  # Titik awal
context.line_to(WIDTH * 0.49, HEIGHT * 0.78)  # Garis ke bawah
context.stroke()  # Gambar garisnya

# --- Gambar Garis Lengkung Halus di Ujung Atas Batang ---
context.set_source_rgb(*light_brown)  # Set warna ke coklat terang
context.move_to(WIDTH * 0.49, HEIGHT * 0.45)  # Mulai dari kiri atas batang
# Buat kurva halus kecil yang melengkung ke kanan
context.curve_to(WIDTH * 0.495, HEIGHT * 0.448, WIDTH * 0.505, HEIGHT * 0.448, WIDTH * 0.51, HEIGHT * 0.45)
context.set_line_width(1)  # Set ketebalan garis = 1 pixel (tipis)
context.stroke()  # Gambar garis kurva (bukan isi)

# Kembalikan status konteks ke kondisi sebelum gambar detail
context.restore()

# --- Gambar Daun-daun Pohon ---

# Definisikan 3 warna hijau buat daun pohon
# Bikin variasi warna hijau biar daun keliatan lebih natural
dark_green = (30/255, 70/255, 20/255)      # Hijau gelap buat bayangan daun
medium_green = (70/255, 120/255, 40/255)   # Hijau sedang buat daun utama
light_green = (120/255, 180/255, 70/255)   # Hijau terang buat highlight daun

# Simpan status konteks sebelum mulai gambar daun
context.save()

# --- DAUN #1: Daun besar di kiri atas ---
context.set_source_rgb(*medium_green)  # Set warna ke hijau sedang
context.move_to(WIDTH * 0.3, HEIGHT * 0.35)  # Mulai dari kiri tengah daun
# Kurva pertama: naik ke atas membentuk setengah lingkaran kiri-atas
context.curve_to(WIDTH * 0.2, HEIGHT * 0.2, WIDTH * 0.4, HEIGHT * 0.15, WIDTH * 0.5, HEIGHT * 0.2)
# Kurva kedua: turun ke bawah membentuk setengah lingkaran kanan-bawah
context.curve_to(WIDTH * 0.6, HEIGHT * 0.25, WIDTH * 0.45, HEIGHT * 0.4, WIDTH * 0.3, HEIGHT * 0.35)
context.fill()  # Isi bentuk daun dengan warna hijau

# --- DAUN #2: Daun besar di kanan atas ---
context.set_source_rgb(*medium_green)  # Set warna ke hijau sedang
context.move_to(WIDTH * 0.5, HEIGHT * 0.2)  # Mulai dari tengah atas
# Kurva pertama: melengkung ke kanan atas lalu turun ke kanan
context.curve_to(WIDTH * 0.6, HEIGHT * 0.15, WIDTH * 0.8, HEIGHT * 0.25, WIDTH * 0.7, HEIGHT * 0.4)
# Kurva kedua: balik ke kiri membentuk bagian bawah daun
context.curve_to(WIDTH * 0.6, HEIGHT * 0.45, WIDTH * 0.55, HEIGHT * 0.3, WIDTH * 0.5, HEIGHT * 0.2)
context.fill()  # Isi bentuk daun dengan warna hijau

# --- DAUN #3: Daun sedang di kiri tengah ---
context.set_source_rgb(*medium_green)  # Set warna ke hijau sedang
context.move_to(WIDTH * 0.25, HEIGHT * 0.45)  # Mulai dari kiri bawah daun
# Kurva pertama: naik membentuk bagian atas daun
context.curve_to(WIDTH * 0.15, HEIGHT * 0.35, WIDTH * 0.35, HEIGHT * 0.3, WIDTH * 0.45, HEIGHT * 0.4)
# Kurva kedua: turun membentuk bagian bawah daun
context.curve_to(WIDTH * 0.4, HEIGHT * 0.5, WIDTH * 0.3, HEIGHT * 0.5, WIDTH * 0.25, HEIGHT *