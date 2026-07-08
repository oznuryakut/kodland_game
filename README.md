# Cloud Runner — Kodland Python Eğitmen Test Projesi

Pygame Zero ile yazılmış, gereksinimlere uygun basit bir platformer oyunu.

## Çalıştırma

```bash
pip install pgzero
pgzrun main.py
```

## Kontroller
- Menüde: fare ile butonlara tıkla (Oyuna Başla / Ses Aç-Kapat / Çıkış)
- Oyunda: ←/→ (veya A/D) hareket, SPACE (veya ↑) zıplama

## Gereksinimlerin nasıl karşılandığı
- **Sadece izinli modüller:** `pgzero`, `math`, `random`, ve istisna olarak `pygame.Rect`. Başka hiçbir kütüphane kullanılmadı.
- **Oyun türü:** Platformer (yan görünüm, zıplanabilir platformlar).
- **Ana menü:** Tıklanabilir "Oyuna Başla", "Ses Aç/Kapat", "Çıkış" butonları (`Button` sınıfı).
- **İki tehlikeli düşman:** `enemy1` (yerde devriye gezen slime) ve `enemy2` (havada uçan yarasa), ikisi de kendi bölgelerinde (min_x–max_x arası) gidip geliyor.
- **Kazanma/kaybetme mekaniği:** Bayrağa ulaşmak = kazanma; düşmana çarpmak ya da haritadan düşmek = kaybetme. Hatasız, net kurallarla.
- **Hareket halinde sprite animasyonu:** Kahramanın 4 karelik yürüme animasyonu, düşmanların yürüme/kanat çırpma animasyonları (`AnimatedActor.update_animation`).
- **Sesler:** Zıplama, coin toplama, düşmana çarpma, kazanma ve buton tıklama sesleri + döngülü arka plan müziği. Tüm sesler kod ile (sinüs/kare dalga) sentezlendi, dışarıdan indirilmedi — tamamen özgün.
- **Durgun haldeyken de animasyon:** Kahraman ve düşmanlar için ayrı "idle" kareleri var (nefes alma / hafif kanat kıpırtısı), yürüyüşle karıştırılmadı.
- **Kendi sınıfların (OOP):** `AnimatedActor` (temel animasyon sınıfı), `Hero`, `Enemy`, `Platform`, `Coin`, `Button` — hareket ve animasyon mantığı bu sınıflarda.
- **İsimlendirme / PEP8:** Değişken, fonksiyon ve sınıf isimleri açık İngilizce; `pycodestyle` ile kontrol edildi, hatasız.

## Klasör yapısı
```
main.py              -> oyunun tamamı (~250 anlamlı satır)
images/               -> tüm sprite'lar (generate_assets.py ile üretildi)
sounds/, music/       -> tüm sesler (generate_sounds.py ile üretildi)
generate_assets.py    -> görselleri PIL ile sıfırdan çizen script (opsiyonel, kanıt amaçlı)
generate_sounds.py    -> sesleri sentezleyen script (opsiyonel, kanıt amaçlı)
```

`generate_assets.py` ve `generate_sounds.py` dosyalarını GitHub'a projeyle birlikte
yüklemen, görsellerin/seslerin tamamen orijinal ve senin tarafından üretildiğini
göstermek açısından işine yarar — istersen kaldırıp sadece `images/`, `sounds/`,
`music/`, `main.py` dosyalarını da yükleyebilirsin.
