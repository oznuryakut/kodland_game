# Cloud Runner — Kodland Python Eğitmen Test Projesi

Pygame Zero ile yazılmış, gereksinimlere uygun basit bir platformer oyunu.

## Çalıştırma

```bash
pip install pgzero
pgzrun main.py
```

macOS'ta `pgzrun` terminalde bulunmazsa:

```bash
/Users/namelessmuse/Library/Python/3.9/bin/pgzrun main.py
```

## Kontroller
- Menüde: fare ile butonlara tıkla (Oyuna Başla / Ses Aç-Kapat / Çıkış)
- Oyunda: ←/→ (veya A/D) hareket, SPACE (veya ↑) zıplama
- Oyun sırasında: sağ üstteki Durdur/Devam, Ses Aç/Kapat ve Çıkış butonları

## Gereksinimlerin nasıl karşılandığı
- **Sadece izinli modüller:** Oyun kodunda yalnızca Pygame Zero'nun sağladığı nesneler ve izin verilen istisna olarak `pygame.Rect` kullanıldı. Başka kütüphane import edilmedi.
- **Oyun türü:** Platformer (yan görünüm, zıplanabilir platformlar).
- **Ana menü:** Tıklanabilir "Oyuna Başla", "Ses Aç/Kapat", "Çıkış" butonları (`Button` sınıfı).
- **Oyun içi butonlar:** Oyun sırasında sağ üstten oyunu durdurup devam ettirme, sesi açıp kapatma ve ana menüye çıkma.
- **İki tehlikeli düşman:** `enemy1` (yerde devriye gezen slime) ve `enemy2` (havada uçan yarasa), ikisi de kendi bölgelerinde (min_x–max_x arası) gidip geliyor.
- **Kazanma/kaybetme mekaniği:** Bayrağa ulaşmak = kazanma; düşmana çarpmak ya da haritadan düşmek = kaybetme. Hatasız, net kurallarla.
- **Hareket halinde sprite animasyonu:** Kahramanın 4 karelik yürüme animasyonu, düşmanların yürüme/kanat çırpma animasyonları (`AnimatedActor.animate`).
- **Sesler:** Zıplama, coin toplama, düşmana çarpma, kazanma ve buton tıklama sesleri + döngülü arka plan müziği.
- **Durgun haldeyken de animasyon:** Kahraman ve düşmanlar için ayrı "idle" kareleri var (nefes alma / hafif kanat kıpırtısı), yürüyüşle karıştırılmadı.
- **Kendi sınıfların (OOP):** `AnimatedActor` (temel animasyon sınıfı), `Hero`, `Enemy`, `Platform`, `Coin`, `Button` — hareket ve animasyon mantığı bu sınıflarda.
- **İsimlendirme / PEP8:** Değişken, fonksiyon ve sınıf isimleri açık İngilizce seçildi; satır uzunlukları ve temel PEP8 düzeni manuel kontrol edildi.

## Klasör yapısı
```
main.py          -> oyunun tamamı
images/          -> sprite ve arka plan görselleri
sounds/, music/  -> ses efektleri ve arka plan müziği
```
