# CMPE 300 Project 2: MPI-Based Parallel NLP System
## Yol Haritası ve Uygulama Planı

**Deadline:** 8 Aralık 2025, 23:59

---

## 📋 PROJE ÖZETİ

MPI tabanlı paralel bir NLP (Natural Language Processing) sistemi geliştirmek. Sistem 4 farklı iletişim pattern'i kullanarak metin dosyalarını işleyecek ve TF (Term-Frequency) ile DF (Document-Frequency) değerlerini hesaplayacak.

---

## 🎯 AŞAMA 1: ORTAM HAZIRLIĞI (1-2 gün)

### 1.1 MPI ve mpi4py Kurulumu
```bash
# macOS için
brew install openmpi
pip install mpi4py

# Linux için
sudo apt-get install openmpi-bin libopenmpi-dev
pip install mpi4py

# Kurulumu test et
mpiexec -n 4 python -c "from mpi4py import MPI; print(MPI.COMM_WORLD.Get_rank())"
```

### 1.2 Proje Klasör Yapısı Oluştur
```
Project2/
├── solution.py              # Ana program
├── test_cases/              # Test dosyaları
│   ├── text_1.txt
│   ├── vocab_1.txt
│   ├── stopwords_1.txt
│   └── ... (5 test case için)
├── sample_data/             # Moodle'dan indirilen örnekler
│   ├── sample_text.txt
│   ├── vocab.txt
│   └── stopwords.txt
└── report.pdf               # Final rapor
```

### 1.3 Örnek Dosyaları İndir ve İncele
- Moodle'dan örnek dosyaları indir
- Dosya formatlarını anla
- Örnek çıktıları incele

---

## 🔧 AŞAMA 2: TEMEL NLP FONKSİYONLARI (2-3 gün)

### 2.1 Yardımcı Fonksiyonlar Geliştir
Bu fonksiyonlar tüm pattern'lerde kullanılacak:

```python
def lowercase_text(sentences):
    """Tüm karakterleri küçük harfe çevir"""
    pass

def remove_punctuation(sentences):
    """Noktalama işaretlerini kaldır"""
    import string
    # string.punctuation kullan
    pass

def remove_stopwords(sentences, stopwords_list):
    """Stopword'leri kaldır"""
    pass

def compute_tf(sentences, vocabulary):
    """Term-Frequency hesapla"""
    # Her kelimenin toplam kaç kez geçtiğini say
    pass

def compute_df(sentences, vocabulary):
    """Document-Frequency hesapla"""
    # Her kelimenin kaç farklı cümlede geçtiğini say
    pass

def split_into_sentences(text):
    """Metni cümlelere böl"""
    pass

def load_vocabulary(vocab_file):
    """Vocabulary dosyasını yükle"""
    pass

def load_stopwords(stopwords_file):
    """Stopwords dosyasını yükle"""
    pass
```

### 2.2 Test Et
- Her fonksiyonu ayrı ayrı test et
- Örnek input/output'ları doğrula
- Edge case'leri kontrol et (boş dosya, tek kelime, vs.)

---

## 📐 AŞAMA 3: PATTERN #1 - End-to-End Processing (3-4 gün)

### 3.1 Pattern #1 Mantığı
- **Manager (Rank 0):**
  1. Dosyaları yükle (text, vocab, stopwords)
  2. Metni cümlelere böl
  3. Cümleleri worker sayısına göre dengeli böl (chunk'lara)
  4. Her worker'a bir chunk gönder
  5. Worker'lardan TF sonuçlarını topla
  6. Sonuçları birleştir ve yazdır

- **Worker (Rank 1+):**
  1. Manager'dan chunk al
  2. Lowercasing uygula
  3. Punctuation removal uygula
  4. Stopword removal uygula
  5. TF hesapla
  6. Sonuçları manager'a gönder

### 3.2 İmplementasyon Adımları
1. Manager kodu yaz
2. Worker kodu yaz
3. Chunk bölme algoritmasını test et
4. MPI send/recv iletişimini test et
5. Sonuç birleştirmeyi test et

### 3.3 Test Komutu
```bash
mpiexec -n 5 python solution.py --text sample_text.txt --vocab vocab.txt --stopwords stopwords.txt --pattern 1
```

---

## 🔄 AŞAMA 4: PATTERN #2 - Linear Pipeline (3-4 gün)

### 4.1 Pattern #2 Mantığı
- **Toplam 5 process:** 1 Manager + 4 Worker
- **Worker görevleri:**
  - Worker 1: Lowercasing
  - Worker 2: Punctuation removal
  - Worker 3: Stopword removal
  - Worker 4: TF counting

- **Manager:**
  1. Metni chunk'lara böl (5-20 arası değerle)
  2. Chunk'ları sırayla Worker 1'e gönder
  3. Worker 4'ten final TF sonuçlarını al
  4. Sonuçları yazdır

- **Pipeline Akışı:**
  ```
  Manager → Worker1 → Worker2 → Worker3 → Worker4 → Manager
  ```

### 4.2 Önemli Noktalar
- Manager tüm veriyi bir kerede göndermemeli, chunk chunk göndermeli
- Her worker bir chunk'ı işleyip bir sonrakine gönderirken, yeni chunk'ı alabilmeli
- Worker 4 TF sonuçlarını biriktirmeli (accumulate)

### 4.3 İmplementasyon Adımları
1. Chunk boyutunu belirleme algoritması (5-20 arası)
2. Manager'dan Worker 1'e chunk gönderme döngüsü
3. Pipeline içinde chunk forwarding
4. Worker 4'te TF accumulation
5. Manager'a sonuç gönderme

### 4.4 Test Komutu
```bash
mpiexec -n 5 python solution.py --text sample_text.txt --vocab vocab.txt --stopwords stopwords.txt --pattern 2
```

---

## 🔀 AŞAMA 5: PATTERN #3 - Parallel Pipelines (4-5 gün)

### 5.1 Pattern #3 Mantığı
- **Process sayısı:** 1 + 4i (i ≥ 1)
  - Örnek: 5, 9, 13, 17, ...
- **Pipeline sayısı:** i (her pipeline 4 worker içerir)

- **Manager:**
  1. Metni pipeline sayısına göre büyük chunk'lara böl
  2. Her pipeline'a bir büyük chunk gönder
  3. Her pipeline kendi içinde küçük chunk'lara böler (Pattern #2 gibi)
  4. Her pipeline'ın son worker'ından sonuçları topla
  5. Sonuçları birleştir

- **Pipeline Yapısı:**
  ```
  Manager → Pipeline1 (Worker1→Worker2→Worker3→Worker4)
         → Pipeline2 (Worker5→Worker6→Worker7→Worker8)
         → ...
  ```

### 5.2 İki Aşamalı Chunking
1. **İlk aşama:** Metni pipeline sayısına böl
2. **İkinci aşama:** Her pipeline kendi chunk'ını 5-20 arası değerle böler

### 5.3 İmplementasyon Adımları
1. Process sayısından pipeline sayısını hesapla
2. Manager'da pipeline'lara chunk dağıtımı
3. Her pipeline'da Pattern #2 mantığını uygula
4. Sonuçları toplama ve birleştirme

### 5.4 Test Komutu
```bash
mpiexec -n 9 python solution.py --text sample_text.txt --vocab vocab.txt --stopwords stopwords.txt --pattern 3
```

---

## ⚡ AŞAMA 6: PATTERN #4 - Task Parallelism (4-5 gün)

### 6.1 Pattern #4 Mantığı
- **Process sayısı:** 1 + 2i (i ≥ 1)
  - Örnek: 3, 5, 7, 9, ...
- **Worker sayısı:** 2i (çift sayı)

- **Adımlar:**
  1. Manager metni chunk'lara böler (Pattern #1 gibi)
  2. Her worker kendi chunk'ını alır
  3. Her worker preprocessing yapar (lowercase, punctuation, stopwords)
  4. **Data Exchange:** Worker'lar çiftler halinde veri değişimi yapar
     - Worker 1 ↔ Worker 2
     - Worker 3 ↔ Worker 4
     - ...
  5. **Task Split:**
     - Tek rank'lar (1, 3, 5, ...): TF hesaplar
     - Çift rank'lar (2, 4, 6, ...): DF hesaplar
  6. Manager TF ve DF sonuçlarını toplar

### 6.2 Deadlock Önleme
**KRİTİK:** Deadlock'u önlemek için asimetrik iletişim:
- **Çift rank'lar:** Önce SEND, sonra RECV
- **Tek rank'lar:** Önce RECV, sonra SEND

```python
# Örnek (Worker 2 - çift rank)
if rank % 2 == 0:  # Çift rank
    comm.send(my_data, dest=rank-1, tag=1)
    partner_data = comm.recv(source=rank-1, tag=2)
else:  # Tek rank
    partner_data = comm.recv(source=rank+1, tag=1)
    comm.send(my_data, dest=rank+1, tag=2)
```

### 6.3 İmplementasyon Adımları
1. Preprocessing (Pattern #1 gibi)
2. Pair matching algoritması
3. Asimetrik send/recv implementasyonu
4. TF ve DF hesaplama
5. Manager'a sonuç gönderme

### 6.4 Test Komutu
```bash
mpiexec -n 5 python solution.py --text sample_text.txt --vocab vocab.txt --stopwords stopwords.txt --pattern 4
```

---

## 🧪 AŞAMA 7: TEST CASE'LER HAZIRLAMA (2-3 gün)

### 7.1 Test Case Gereksinimleri
Her test case için:
- **Text file:** 20-100 cümle arası
- **Vocabulary:** 5-15 kelime arası
- **Stopwords:** 3-10 kelime arası

### 7.2 5 Test Case Hazırla
1. **Test Case 1:** Küçük (20-30 cümle, 5-7 kelime vocab)
2. **Test Case 2:** Orta (40-50 cümle, 8-10 kelime vocab)
3. **Test Case 3:** Büyük (70-80 cümle, 12-15 kelime vocab)
4. **Test Case 4:** Edge case (tekrarlayan kelimeler, özel karakterler)
5. **Test Case 5:** Karışık (farklı uzunluklarda cümleler)

### 7.3 Tüm Pattern'lerle Test Et
Her test case için 4 pattern'i çalıştır:
```bash
# Test Case 1 için
mpiexec -n 5 python solution.py --text test_cases/text_1.txt --vocab test_cases/vocab_1.txt --stopwords test_cases/stopwords_1.txt --pattern 1
mpiexec -n 5 python solution.py --text test_cases/text_1.txt --vocab test_cases/vocab_1.txt --stopwords test_cases/stopwords_1.txt --pattern 2
mpiexec -n 9 python solution.py --text test_cases/text_1.txt --vocab test_cases/vocab_1.txt --stopwords test_cases/stopwords_1.txt --pattern 3
mpiexec -n 5 python solution.py --text test_cases/text_1.txt --vocab test_cases/vocab_1.txt --stopwords test_cases/stopwords_1.txt --pattern 4
```

**Toplam:** 5 test case × 4 pattern = 20 çalıştırma

### 7.4 Çıktıları Kaydet
Her çalıştırmanın çıktısını kaydet (rapor için)

---

## 📝 AŞAMA 8: RAPOR YAZMA (3-4 gün)

### 8.1 Rapor İçeriği

#### 8.1.1 Program Description
- Her pattern'in nasıl implement edildiği
- Ana zorluklar ve çözümler
- Her pattern'in gereksinimleri nasıl karşıladığı
- Kod yapısı ve tasarım kararları

#### 8.1.2 Test Cases
- Her test case'in açıklaması
- Her pattern için kullanılan komut
- Her çalıştırmanın çıktısı
- Sonuçların doğruluğu

#### 8.1.3 Work Sharing
- Her grup üyesinin katkıları
- Hangi pattern'leri kim yaptı
- Kod review süreci
- Test case hazırlama

### 8.2 Rapor Formatı
- PDF formatında
- Profesyonel görünüm
- Şemalar/diyagramlar (isteğe bağlı)
- Kod snippet'leri (gerekirse)

---

## 📦 AŞAMA 9: FİNAL KONTROL VE SUBMISSION (1 gün)

### 9.1 Dosya Yapısı Kontrolü
```
StudentNo1_StudentNo2.zip
└── StudentNo1_StudentNo2/
    ├── report.pdf
    ├── solution.py
    └── test_cases/
        ├── text_1.txt
        ├── vocab_1.txt
        ├── stopwords_1.txt
        ├── text_2.txt
        ├── vocab_2.txt
        ├── stopwords_2.txt
        ...
        ├── text_5.txt
        ├── vocab_5.txt
        └── stopwords_5.txt
```

### 9.2 Son Kontroller
- [ ] Tüm pattern'ler çalışıyor mu?
- [ ] Command-line argument'ler doğru mu?
- [ ] Process sayısı gereksinimleri karşılanıyor mu?
- [ ] Kod yorumlu mu?
- [ ] Değişken isimleri açıklayıcı mı?
- [ ] solution.py başında isim/numara var mı?
- [ ] Test case'ler gereksinimleri karşılıyor mu?
- [ ] Rapor tam mı?

### 9.3 Test Senaryoları
- Farklı process sayılarıyla test et
- Farklı dosya boyutlarıyla test et
- Edge case'leri test et
- Hata durumlarını test et (olmayan dosya, vs.)

---

## ⏰ ZAMAN ÇİZELGESİ (Önerilen)

| Aşama | Süre | Toplam |
|-------|------|--------|
| Aşama 1: Ortam Hazırlığı | 1-2 gün | 1-2 gün |
| Aşama 2: Temel NLP Fonksiyonları | 2-3 gün | 3-5 gün |
| Aşama 3: Pattern #1 | 3-4 gün | 6-9 gün |
| Aşama 4: Pattern #2 | 3-4 gün | 9-13 gün |
| Aşama 5: Pattern #3 | 4-5 gün | 13-18 gün |
| Aşama 6: Pattern #4 | 4-5 gün | 17-23 gün |
| Aşama 7: Test Cases | 2-3 gün | 19-26 gün |
| Aşama 8: Rapor | 3-4 gün | 22-30 gün |
| Aşama 9: Final Kontrol | 1 gün | 23-31 gün |

**Toplam:** ~3-4 hafta (deadline'a göre planla)

---

## 💡 İPUÇLARI VE ÖNEMLİ NOTLAR

### Kodlama İpuçları
1. **Modüler kod yaz:** Her pattern için ayrı fonksiyon
2. **Debug için print kullan:** Her process'in ne yaptığını görmek için
3. **Tag kullan:** MPI send/recv'de farklı tag'ler kullan
4. **Hata kontrolü:** Dosya okuma, process sayısı kontrolü
5. **Kod yorumları:** Her önemli adımı açıkla

### MPI İpuçları
1. **Blocking operations:** Sadece send/recv kullan (ISend/IRecv yok)
2. **Tag'ler:** Farklı mesaj tipleri için farklı tag'ler
3. **Deadlock:** Pattern #4'te asimetrik iletişim kritik
4. **Chunking:** Pattern #2 ve #3'te chunk boyutu önemli

### Test İpuçları
1. **Küçükten başla:** Önce küçük dosyalarla test et
2. **Manuel kontrol:** Basit örneklerle manuel hesapla ve karşılaştır
3. **Farklı process sayıları:** Her pattern'i farklı process sayılarıyla test et
4. **Edge cases:** Boş dosya, tek cümle, tek kelime gibi durumları test et

### Rapor İpuçları
1. **Erken başla:** Kod biter bitmez rapor yazmaya başla
2. **Screenshot'lar:** Test çıktılarını kaydet
3. **Açıklayıcı:** Teknik detayları açıkla
4. **Profesyonel:** Düzgün formatla, yazım hatalarına dikkat et

---

## 🚨 YAYGIN HATALAR VE ÇÖZÜMLERİ

### Hata 1: Deadlock (Pattern #4)
**Sorun:** Her iki taraf da send yapıyor
**Çözüm:** Asimetrik iletişim (tek rank recv, çift rank send önce)

### Hata 2: Chunk boyutu (Pattern #2, #3)
**Sorun:** Tüm veriyi bir kerede gönderme
**Çözüm:** 5-20 arası değerle chunk'lara böl

### Hata 3: Process sayısı
**Sorun:** Yanlış process sayısı
**Çözüm:** Her pattern için gereksinimleri kontrol et

### Hata 4: TF/DF birleştirme
**Sorun:** Sonuçlar yanlış birleştiriliyor
**Çözüm:** Dictionary merge işlemini dikkatli yap

---

## 📚 FAYDALI KAYNAKLAR

- mpi4py Documentation: https://mpi4py.readthedocs.io/
- MPI Tutorial: https://mpitutorial.com/
- argparse Documentation: https://docs.python.org/3/library/argparse.html
- Python string.punctuation: https://docs.python.org/3/library/string.html

---

## ✅ CHECKLIST

### Kod Geliştirme
- [ ] Temel NLP fonksiyonları
- [ ] Pattern #1 implementasyonu
- [ ] Pattern #2 implementasyonu
- [ ] Pattern #3 implementasyonu
- [ ] Pattern #4 implementasyonu
- [ ] Command-line argument parsing
- [ ] Hata kontrolü
- [ ] Kod yorumları

### Test
- [ ] 5 test case hazırlama
- [ ] Her test case için 4 pattern test
- [ ] Farklı process sayılarıyla test
- [ ] Edge case testleri
- [ ] Çıktı doğrulama

### Rapor
- [ ] Program description
- [ ] Test case sonuçları
- [ ] Work sharing açıklaması
- [ ] PDF formatında kaydetme

### Submission
- [ ] Dosya yapısı kontrolü
- [ ] İsim/numara ekleme
- [ ] Zip dosyası oluşturma
- [ ] Final kontrol

---

**Başarılar! 🚀**

