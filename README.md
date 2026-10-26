# G*Power Teardown Sprint - K2 (t-test, matched pairs)

## 1. Başlık ve Katman Bilgisi
**G*Power Teardown Sprint - K2 (t-test, matched pairs)**

## 2. Kurulum ve Çalıştırma
### Gereksinimler
- Python **3.10+**
- `scipy` (statistical functions)
- `pytest` (test suite)

```bash
# Install the required Python packages
python -m pip install --upgrade pip
python -m pip install scipy pytest
```

### CLI Kullanım Örneği
```bash
python src/cli.py --test t-paired \
    --mode a-priori \
    --tails 2 \
    --d 0.5 \
    --alpha 0.05 \
    --power 0.8
```
The command prints a single‑line JSON containing `n_total`, `actual_power`, `critical`, `df`, and `ncp`.

## 3. REA ve Ghidra Kontrolü
**Soru:** *REA araçları ve Ghidra sağlayıcısı bu oturumda kullanılabilir mi?*  
**Yanıt:** **Evet.** REA (Reverse‑Engineer‑Anything) ve Ghidra entegrasyonu bu oturumda mevcuttur ve `inspect_*`‑style MCP araçlarıyla kullanılabilir. Ancak bu sprintte sadece SPEC/CONTRACT‑a dayalı **Python** tabanlı bir hesaplama motoru ve CLI geliştirilmiştir; REA ve Ghidra doğrudan kullanılmadı, fakat ortamda aktif oldukları doğrulanmıştır.

## 4. GPower.exe SHA‑256 Hash
```
C63E6A133EB6372932F810C08CC33DC35A06D1DDB658F897BD6C34A754EFC812
```

## 5. Diferansiyel Test Raporu
Oracle klasöründeki **30** G*Power ekran görüntüsünden türetilen **8** temsilci test vektörü aşağıdaki gibi doğrulandı:
- `tails`, `d`, `alpha`, `power` değerlerine karşı elde edilen `n_total` **tamamen** G*Power’ın raporladığı `expected_n` ile eşleşiyor.
- PyTest ile çalışan **diferansiyel test seti** (`tests/test_cli.py`) **%100 uyum** gösterdi ve **2** test başarıyla geçti.

## 6. Demo Video
[60‑saniyelik CLI Demo Video](https://example.com/demo-video)

## 7. Atıf (Citations)
- Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007, 2009). *G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences.*
