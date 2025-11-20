<p align="center">
  <h1 align="center">🌿 FLOFA 🌿</h1>
  <p align="center"><i>Flora & Fauna Exploration Game</i></p>
</p>

<p align="center">
<a href="https://www.pygame.org"><img src="https://img.shields.io/badge/Pygame-2.0+-green.svg" alt="Pygame Version"></a>
<a href="https://www.python.org"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
</p>

## Tentang Flofa

Flofa adalah game eksplorasi alam 2D yang dibangun dengan **Pygame** dan **PyCairo**. Game ini menerapkan arsitektur **Model-View-Controller (MVC)** untuk pemisahan kode yang bersih dan mudah dipelihara.

Dalam game ini, pemain dapat:

- 🎮 **Jelajahi** dunia yang luas dengan sistem kamera yang mengikuti pemain
- 🌳 **Berinteraksi** dengan berbagai pohon dan tanaman eksotis
- 🐾 **Temui** hewan-hewan lucu dengan AI yang realistis
- 🐱 **Amati** kucing dengan state machine (idle, jalan, lari, tidur)
- 🌾 **Nikmati** rumput yang bergoyang dengan animasi procedural
- 🗺️ **Navigasi** dengan bantuan minimap real-time

Flofa dirancang untuk pembelajaran dan eksplorasi, menggabungkan visual yang menarik dengan code architecture yang solid.

## Prasyarat

Sebelum menjalankan game, pastikan Anda telah menginstal:

- **Python 3.8+**
- **Pygame 2.0+**
- **PyCairo** (untuk rendering rumput procedural)

## Instalasi

Clone repository ini:

```bash
git clone https://github.com/ariear/flofa.git
cd flofa
```

Install dependencies:

```bash
pip install pygame pycairo
```

## Menjalankan Game

Jalankan game dengan perintah:

```bash
python main.py
```

## Kontrol

- **WASD** atau **Arrow Keys**: Gerakkan pemain
- **SPASI**: Berinteraksi dengan objek terdekat
- **ESC**: Tutup popup informasi

## Arsitektur MVC

Flofa menggunakan pola **Model-View-Controller** untuk organisasi kode yang optimal:

```
flofa/
├── main.py                      # Entry point aplikasi
├── assets/                      # Asset game (sprites, images)
│   ├── player.png              # Spritesheet player 8x4
│   ├── animals/                # Sprite hewan
│   ├── animals_move/           # Spritesheet animasi hewan
│   └── Plants/                 # Sprite pohon & tanaman
└── src/
    ├── config.py               # Konfigurasi & konstanta
    ├── models/                 # Model Layer
    │   ├── player.py           # Player dengan animasi 4 arah
    │   ├── animal.py           # Entity hewan
    │   ├── cat.py              # Kucing dengan AI state machine
    │   ├── tree.py             # Entity pohon
    │   └── grass.py            # Generasi rumput procedural
    ├── views/                  # View Layer
    │   ├── game_view.py        # Rendering utama game
    │   └── info_popup.py       # UI popup informasi
    ├── controllers/            # Controller Layer
    │   └── game_controller.py  # Orchestrator game logic
    └── utils/                  # Utilities
        ├── asset_loader.py     # Loader asset dengan error handling
        └── helpers.py          # Fungsi helper
```

### Model Layer
Berisi entitas game dan logika bisnis:
- **Player**: Animasi 32 frame (8 frame × 4 arah)
- **Animal**: Static entities dengan highlight
- **Cat**: AI dengan 4 state (idle, walking, running, sleeping)
- **Tree**: Entity statis dengan info deskriptif
- **Grass**: Procedural generation dengan PyCairo

### View Layer
Menangani semua rendering:
- **GameView**: Depth sorting, minimap, instructions overlay
- **InfoPopup**: Modal popup dengan image preview

### Controller Layer
Mengatur alur game:
- **GameController**: Input handling, camera control, interaction detection, cat AI updates

## Fitur Unggulan

### 🎨 Procedural Grass Generation
Menggunakan **PyCairo** untuk menggambar rumput secara procedural dengan variasi warna dan animasi goyang berbasis sine wave.

### 🤖 Cat AI State Machine
Kucing memiliki perilaku realistis:
- **Idle**: Berdiri diam
- **Walking**: Berjalan santai ke target random
- **Running**: Berlari cepat
- **Sleeping**: Tidur dengan animasi lambat

### 📍 Smart Interaction System
Deteksi proximity otomatis dengan highlight visual pada objek terdekat yang dapat diinteraksi.

### 🗺️ Minimap Real-time
Peta mini dengan skala 0.08 menampilkan posisi pemain, pohon, dan hewan dalam satu pandangan.

## Dependencies

```json
{
  "pygame": "^2.0.0",
  "pycairo": "^1.20.0"
}
```

## Asset Credits

- **Player Sprite**: Spritesheet 512×256 (8 kolom × 4 baris)
- **Cat Animation**: Spritesheet 512×256 (idle, walk, run, sleep)
- **Animals**: Individual PNG sprites
- **Plants**: Tree sprites dengan berbagai jenis

## Kontribusi

Kontribusi sangat diterima! Silakan fork repository ini dan submit pull request.

1. Fork project
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

## License

Project ini dilisensikan di bawah [MIT License](LICENSE).

## Kontak

**Developer**: Arie Andrian Rahman  
**Email**: your.email@example.com  
**GitHub**: [@ariear](https://github.com/ariear)

---

<p align="center">Dibuat dengan ❤️ menggunakan Python & Pygame</p>
