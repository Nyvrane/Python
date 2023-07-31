# Kütüphaneleri alalım.
import requests
from bs4 import BeautifulSoup
import time
"""
pyinstaller --onefile --noconsole --icon=BorsaAnalizApp/logo.ico BorsaAnalizApp/BorsaAnalizAppGörsel.py
"""
# Ana fonksiyonumuzda kullanacağımız hissenin puanını temsil eden global bir puan değişkeni oluşturalım.
puan = 0
bedelsizpotansiyeli = 1

# Ana foksiyonumuzu oluşturalım
def anafonksiyon():
    # yukarıda belirttiğimiz puan değişkenini içeriye aktaralım. Hesaplamalar bitince puanı bir sonraki hissede yeniden
    # hesaplamak için sıfırlayacağız.
    global puan
    # Başlık yazımızı oluşturalım
    print("*" * 40, "fromNyvrane", "*" * 40,
          "\nBu program eğitim amacıyla yapılmış olup hiçbir şekilde yatırım tavsiyesi içermemektedir.\n")

    # Kullanıcıdan hesaplanacak hissenin sembolünü isteyelim
    hisse = input("Bir hisse sembolü girin: ")
    # Sitenin hisse linklerinde semboller büyük harfle ve ingilizce olduğundan upper fonksiyonu uygulayalım.
    hisse = hisse.upper()

    # Hesaplamalarda veri çekeceğimiz adresleri oluşturalım.
    bilancoadres = "https://fintables.com/sirketler/" + hisse + "/finansal-tablolar/bilanco"
    gelirtablosuadres = "https://fintables.com/sirketler/" + hisse + "/finansal-tablolar/gelir-tablosu"
    sektoradres = "https://fintables.com/sektorler"
    yenisektoradres = "https://fintables.com/"
    anaadres = "https://fintables.com/sirketler/" + hisse

    # Yukarıdaki adreslerden request ile içeriği indirelim.
    bilancocevap = requests.get(bilancoadres)
    gelirtablosucevap = requests.get(gelirtablosuadres).content
    sektorcevap = requests.get(sektoradres).content
    anaadrescevap = requests.get(anaadres).content

    # İndirilen içerikleri Beautifulsoup ile html dilinde parse edelim.
    bilancosoup = BeautifulSoup(bilancocevap.content, "html.parser")
    gelirtablosusoup = BeautifulSoup(gelirtablosucevap, "html.parser")
    sektorsoup = BeautifulSoup(sektorcevap, "html.parser")
    bilancotext = bilancocevap.text
    anaadressoup = BeautifulSoup(anaadrescevap, "html.parser")

    # Aldığımız içerikteki ana etiketleri bulup liste içerisine atalım.
    bilancotaglar = bilancosoup.find_all("tr",
                                         {"class": "group hover:bg-black/80 border-b border-neutral-white-10"})
    bilancotaglar2 = bilancosoup.find_all("tr",
                                         {"class": "group hover:bg-black/80 text-gray-100 font-bold"})
    bilancotaglar3 = bilancosoup.find_all("tr",
                                         {"class": "group hover:bg-black/80 text-gray-100 font-bold border-b border-neutral-white-10"})
    gelirtablosutaglar = gelirtablosusoup.find_all("tr", {
        "class": "group hover:bg-black/80 border-b border-neutral-white-10"})
    gelirtablosutaglar2 = gelirtablosusoup.find_all("tr", {
        "class": "group hover:bg-black/80 text-gray-100 font-bold"})
    gelirtablosutaglar3 = gelirtablosusoup.find_all("tr", {
        "class": "group hover:bg-black/80 text-gray-100 font-bold border-b border-neutral-white-10"})
    sektortaglar = sektorsoup.find_all("a", {
        "class": "cursor-pointer"})
    anaadrestaglar = anaadressoup.find_all("tr", {
        "class": "group hover:bg-neutral-black-30 border-b border-neutral-white-10"})

    # Birazdan alacağımız verileri kullanım kolaylığı için bilanço verilerinde sözlük yapısında kullanacağız.
    bilancoveriler = {}

    # Hisse bilanço değerlerinin ve onların isimlerinin yukarıdaki sözlüğe eklenmesini sağlayalım.
    for i in bilancotaglar:
        kalem = i.find("div", {"class": "flex-grow"}).text
        miktar_elements = i.find("td", {"class": "text-right pr-3 bg-black/40"}).find_all("span", {
            "class": "inline-flex items-center tabular-nums"})
        miktar = miktar_elements[1].text if len(miktar_elements) >= 2 else ""
        bilancoveriler[kalem] = miktar

    for i in bilancotaglar2:
        kalem = i.find("div", {"class": "flex-grow"}).text
        miktar_elements = i.find("td", {"class": "text-right pr-3 bg-black/40"}).find_all("span", {
            "class": "inline-flex items-center tabular-nums"})
        miktar = miktar_elements[1].text if len(miktar_elements) >= 2 else ""
        bilancoveriler[kalem] = miktar

    for i in bilancotaglar3:
        kalem = i.find("div", {"class": "flex-grow"}).text
        miktar_elements = i.find("td", {"class": "text-right pr-3 bg-black/40"}).find_all("span", {
            "class": "inline-flex items-center tabular-nums"})
        miktar = miktar_elements[1].text if len(miktar_elements) >= 2 else ""
        bilancoveriler[kalem] = miktar

    # Birazdan alacağımız verileri kullanım kolaylığı için gelir tablosu verilerinde sözlük yapısında kullanacağız.
    gelirtablosuveriler = {}

    # Hisse gelir tablosu değerlerinin ve onların isimlerinin yukarıdaki sözlüğe eklenmesini sağlayalım.
    for i in gelirtablosutaglar:
        kalem = i.find("div", {"class": "flex-grow"}).text
        miktar_elements = i.find("td", {"class": "text-right pr-3 bg-black/40"}).find_all("span", {
            "class": "inline-flex items-center tabular-nums"})
        miktar = miktar_elements[1].text if len(miktar_elements) >= 2 else ""
        gelirtablosuveriler.update({kalem: miktar})

    for i in gelirtablosutaglar2:
        kalem = i.find("div", {"class": "flex-grow"}).text
        miktar_elements = i.find("td", {"class": "text-right pr-3 bg-black/40"}).find_all("span", {
            "class": "inline-flex items-center tabular-nums"})
        miktar = miktar_elements[1].text if len(miktar_elements) >= 2 else ""
        gelirtablosuveriler.update({kalem: miktar})

    for i in gelirtablosutaglar3:
        kalem = i.find("div", {"class": "flex-grow"}).text
        miktar_elements = i.find("td", {"class": "text-right pr-3 bg-black/40"}).find_all("span", {
            "class": "inline-flex items-center tabular-nums"})
        miktar = miktar_elements[1].text if len(miktar_elements) >= 2 else ""
        gelirtablosuveriler.update({kalem: miktar})

    # Birazdan alacağımız verileri kullanım kolaylığı için ana adres verilerinde sözlük yapısında kullanacağız.
    anaadresveriler = {}

    # Hisse adresindeki değerlerin ve onların isimlerinin yukarıdaki sözlüğe eklenmesini sağlayalım.
    for i in anaadrestaglar:
        kalem = i.find("td", {"class": "pl-4 text-neutral-white-70 font-semibold"}).text
        miktar = i.find("td", {"class": "text-right py-3.5 pr-3"}).text
        anaadresveriler.update({kalem: miktar})

    # Dönen verileri görüp ona göre etiketler kullanmak için gerektiğinde içeriği burada yazdırabiliriz.
    # print(bilancoveriler)
    # print(gelirtablosuveriler)

    # Hissenin fiyatını içerikten alalım. Yanlış girilmesi durumunda kullanıcıdan yeni işlem isteyelim.
    try:
        ilkindex = bilancotext.index('price') + 8
        sonindex = bilancotext.index(',', ilkindex)
        hissefiyati = float(bilancotext[ilkindex:sonindex])
        # print(hissefiyati)
    except ValueError:
        print("Geçersiz hisse adı.")
        hisseyanlis = input("Aşağıdaki işlemler için belirtilen sayıya basınız"
                            "\n1-Yeni hisse girişi\n2-Çıkış\nİşlem: ")
        if hisseyanlis == "1":
            anafonksiyon()
        elif hisseyanlis == "2":
            quit()

    # Bu aşamadan sonra kriterlerimizi tanımlayalım.
    # Buradaki kriterler belirli matematiksel işlemler gerçekleştiriyor ve belirli değerleri hesaplıyor.
    # Ayrıca karşıladığı kriterlere göre puanda artış veya azalışlar yapabiliyor.

    # birincikriter şirketin borçlarını ödeyebilme durumunu kontrol ediyor.
    def birincikriter(donenvarliklar, kisavadeyukum, finansalgelir, finansalgider, brutkar):
        global puan
        print("\nBu işlem yaklaşık 5 dakikaya kadar sürebilmektedir. Lütfen işlem sonlanana kadar bekleyin.\n")
        donenvarliklar = donenvarliklar.replace(".", "")
        kisavadeyukum = kisavadeyukum.replace(".", "")
        if int(donenvarliklar) - int(kisavadeyukum) >= 0:
            print("1.Kriter - İYİ: Şirket borçlarını ödeyebilecek durumda")
            puan += 20
            pass
        else:
            finansalgelir = finansalgelir.replace(".", "")
            finansalgider = finansalgider.replace(".", "")
            brutkar = brutkar.replace(".", "")
            if int(finansalgelir) >= int(finansalgider) and int(brutkar) >= 0:
                print("1.Kriter - ORTA: Şirket borçlarını ödeyebilecek durumda değil fakat kar ediyor")
                puan += 10
            else:
                print("1.Kriter - KÖTÜ: Şirket borçlarını ödeyecek durumda değil ve karsız. Dikkat!")
        time.sleep(1)

    # ikinci kriter şirketin dönen varlıklarının kalitesini kontrol ediyor.
    def ikincikriter(nakit, kisavadefinansalborc, kisavadeyatirim):
        global puan
        nakit = nakit.replace(".", "") or 0
        kisavadefinansalborc = kisavadefinansalborc.replace(".", "") or 0
        kisavadeyatirim = kisavadeyatirim.replace(".", "") or 0
        if int(nakit) >= int(kisavadefinansalborc):
            print("2.Kriter - İYİ: Dönen varlıkların kalitesi iyi.")
            puan += 20
        elif int(nakit) + int(kisavadeyatirim) >= int(kisavadefinansalborc):
            print("2.Kriter - ORTA: Şirketin borçlarını ödemek için",
                  "nakiti yetmiyor fakat yatırımları eklenince kısa vade borçlarını karşılıyor")
            puan += 10
        else:
            print("2.Kriter - KÖTÜ: Şirket kısa vade borçlarını karşılayacak durumda değil. Alacakların şüpheli",
                  "alacak olup olmadığını kontrol etmek gerekebilir. Dikkat!")
        time.sleep(1)

    # ucuncukriter şirketin mali yapısını kontrol ediyor.
    def ucuncukriter(toplamvarliklar, ozkaynaklar):
        global puan
        toplamvarliklar = toplamvarliklar.replace(".", "")
        ozkaynaklar = ozkaynaklar.replace(".", "")
        if 1 >= int(ozkaynaklar) / (int(toplamvarliklar)) >= 0.7:
            print("3.Kriter - İYİ: Mali Yapısı Güçlü")
            puan += 20
        elif 0.7 > int(ozkaynaklar) / (int(toplamvarliklar)) >= 0.4:
            print("3.Kriter - ORTA: Mali Yapısı Dengeli")
            puan += 10
        elif 0.4 > int(ozkaynaklar) / (int(toplamvarliklar)) >= 0:
            print("3.Kriter - KÖTÜ: Mali Yapısı Güçsüz")
        elif int(ozkaynaklar) < 0:
            print("3.Kriter - ÇOK KÖTÜ: Şirket Özkaynakları ekside, iflas aşamasında olabilir.")
            puan -= 5
        time.sleep(1)

    # dorduncu kriter şirketin favök marjını sektör marjı ile kıyaslayıp karlılık hesaplıyor.
    def dorduncukriter(favok, satisgelirleri, hisse):
        global puan
        sektortaglar = sektorsoup.find_all("div", {
            "class": "divide-y divide-neutral-white-10 sm:divide-y-0 sm:grid sm:grid-cols-2"})
        sektoradlari = []
        for sektortag in sektortaglar:
            a_etiketleri = sektortag.find_all("a")
            for a_etiketi in a_etiketleri:
                favoksektorlink = "https://fintables.com/" + a_etiketi.get("href")
                favoksektorcevap = requests.get(favoksektorlink).content
                favoksektorsoup = BeautifulSoup(favoksektorcevap, "html.parser")
                aetiketleri = favoksektorsoup.find_all("a")
                for aetiketi in aetiketleri:
                    if hisse in aetiketi.get_text().lower():
                        sektoradlari.append(f"{favoksektorlink.replace('https://fintables.com//sektorler/', '')}")


        favok = favok.replace(".", "")
        favokmarj = int(favok) / int(satisgelirleri.replace(".", "")) * 100
        if favokmarj == 100000.0:
            favokmarj = 10

        sektorfavokmarj = {"ambalaj": 17.46, "ana-metal": 14.58, "araci-kurum": 10.0, "bankacilik": 10.0,
                           "bilisim-ve-yazilim": 10.0, "cam-seramik-porselen": 10.0,
                           "dayanikli-tuketim-urunleri": 10.0,
                           "destek-ve-hizmet": 10.0, "emeklilik": 10.0, "enerji-teknolojileri": 10.0,
                           "enerji-uretim-ve-dagitim": 10.0, "faktoring": 10.0, "finansal-kiralama": 10.0,
                           "gayrimenkul": 10.0, "gida-perakendeciligi": 10.0, "gida-ve-icecek": 10.0,
                           "girisim-sermayesi-yatirim-ortakligi": 10.0,
                           "giyim-tekstil-ve-deri-urunleri-perakendeciligi": 10.0, "haberlesme": 10.0,
                           "holding": 10.0, "ilac-ve-saglik": 10.0, "imalat": 10.0, "insaat": 10.0,
                           "kagit-ve-kagit-urunleri": 10.0, "kimya-ve-plastik": 10.0,
                           "madencilik-ve-tas-ocakciligi": 10.0, "menkul-kiymet-yatirim-ortakligi": 10.0,
                           "metal-esya-ve-makine": 10.0, "mobilya-ve-dekorasyon": 10.0, "otomotiv": 10.0,
                           "otomotiv-yan-sanayi": 10.0, "savunma": 10.0, "servis-tasimaciligi-ve-arac-kiralama": 10.0,
                           "sigorta": 10.0, "spor": 10.0, "tarim-hayvancilik-balikcilik": 10.0,
                           "tasarruf-finansman": 10.0, "tas-toprak-cimento": 10.0, "teknolojik-urun-ticareti": 10.0,
                           "tekstil-giyim-ve-deri": 10.0, "toptan-ve-perakende-ticaret": 10.0, "turizm": 10.0,
                           "ulastirma": 10.0, "varlik-yonetimi": 10.0}


        for sektoradi in sektoradlari:
            if favokmarj / sektorfavokmarj.get(sektoradi, 1) >= 1:
                print("4.Kriter - İYİ: Favök Marjı: {:.2f}, {} sektörü ortalamasının üzerinde"
                      .format(favokmarj, (sektoradi.replace('-', ' ').upper())))
                if len(sektoradlari) > 1:
                    puan += 10
                else:
                    puan += 20
            elif 1 > favokmarj / sektorfavokmarj.get(sektoradi, 1) >= 0.9:
                print("4.Kriter - ORTA: Favök Marjı: {:.2f}, {} sektörü ortalamasına yakın"
                      .format(favokmarj, sektoradi.replace('-', ' ').upper()))
                if len(sektoradlari) > 1:
                    puan += 5
                else:
                    puan += 10
            else:
                print("4.Kriter - KÖTÜ: Favök Marjı: {:.2f}, {} sektörü ortalamasının altında"
                      .format(favokmarj, sektoradi.replace('-', ' ').upper()))

    # besincikriter ise hissenin bedelsiz potansiyelini hesaplıyor.
    def besincikriter(ozkaynaklar, odenmissermaye):
        global puan, bedelsizpotansiyeli
        ozkaynaklar = ozkaynaklar.replace(".", "")
        odenmissermaye = odenmissermaye.replace(".", "")
        bedelsizpotansiyeli = int(ozkaynaklar) / int(odenmissermaye)
        bedelsizpotyuzde = int(bedelsizpotansiyeli) * 100
        if bedelsizpotyuzde >= 1000:
            print(f"5.Kriter - İYİ: Hissenin bedelsiz potansiyeli: % {bedelsizpotyuzde}")
            puan += 20
        elif bedelsizpotyuzde >= 600:
            print(f"5.Kriter - ORTA: Hissenin bedelsiz potansiyeli: % {bedelsizpotyuzde}")
            puan += 10
        else:
            print(f"5.Kriter - KÖTÜ: Hissenin bedelsiz potansiyeli: % {bedelsizpotyuzde}")

    # hedefhesapla hissenin PDDD ve FK'ya göre sektörlere kıyasla gidebileceği hedef fiyatları belirliyor.
    def hedefhesapla(hisse):
        print("Hissenin hedefi hesaplanıyor...")
        for i in sektortaglar:
            sektorlink = yenisektoradres + i.get("href")
            sektorcevap = requests.get(sektorlink).content
            sektorsoup = BeautifulSoup(sektorcevap, "html.parser")
            aetiketleri = sektorsoup.find_all("a")
            for aetiketi in aetiketleri:
                if hisse in aetiketi.get_text().lower():
                    # print("'{0}' kelimesi {1} adresinde bulundu.".format(hisse, sektorlink))
                    print(
                        f'{sektorlink.replace("https://fintables.com//sektorler/", "").replace("-", " ").upper()} '
                        f'sektörüne göre hedef: ')
                    dongusektorcevap = requests.get(sektorlink).content
                    dongusektorsoup = BeautifulSoup(dongusektorcevap, "html.parser")
                    sektoragirlikli = dongusektorsoup.find_all("tr", {"class": "group hover:bg-neutral-black-30"})
                    agirlikliortalamaliste = []
                    for agirlikli in sektoragirlikli:
                        if "ağırlıklı ortalama" in agirlikli.text.lower():
                            agirlikli_span = agirlikli.find_all("span")
                            for span in agirlikli_span:
                                agirlikliortalamaliste.append(span.text)
                    # print(agirlikliortalamaliste)
                    tretiketleri = dongusektorsoup.find_all("tr")
                    tdliste = []
                    for tretiketi in tretiketleri:
                        tdetiketleri = tretiketi.find_all('td')
                        for tdetiketi in tdetiketleri:
                            if hisse in tdetiketi.get_text().lower():
                                for digertd in tdetiketleri:
                                    tdliste.append(digertd.get_text().replace(",", "."))
                    # print(tdliste)
                    hissefdfavok = tdliste[4]
                    hissefk = tdliste[2]
                    hissepddd = tdliste[3]
                    sektorfdfavok = agirlikliortalamaliste[2].replace(",", ".")
                    sektorfk = agirlikliortalamaliste[0].replace(",", ".")
                    sektorpddd = agirlikliortalamaliste[1].replace(",", ".")

                    pdddhedef = float(sektorpddd) / float(hissepddd) * float(hissefiyati)
                    try:
                        fkhedef = float(sektorfk) / float(hissefk) * float(hissefiyati)
                    except:
                        try:
                            fkhedef = float(sektorfdfavok) / float(hissefdfavok) * float(hissefiyati)
                        except:
                            fkhedef = float(sektorfk) / float(hissepddd) * float(hissefiyati)
                    anahedef = (pdddhedef + fkhedef) / 2
                    bedelsizhedef = bedelsizpotansiyeli * anahedef / 10

                    print(
                        '*' * 30 + "\nHisse Fiyatı: {:.2f} TL\nPDDD'ye Göre Hedef: {:.2f} TL\nFK'ya Göre "
                                   "Hedef: {:.2f} TL\nBedelsiz Potansiyeli ile Ortalama Hedef: {:.2f} TL"
                                   "\nTemel Analiz Sonucu Ana Hedef: {:.2f} TL\n".format(hissefiyati, pdddhedef,
                                                                                         fkhedef, bedelsizhedef,
                                                                                         anahedef) + '*' * 30 + "\n")
                    # print(hissefk, hissepddd, hissefdfavok, sektorfk, sektorpddd, sektorfdfavok)

    # Burada yukarıda sözlük yapısı içerisine aldığımız verileri key değeri vererek çağırıyoruz.
    # Bazı bilançolarda bu veriler bulunmuyor, hata almamak için get fonksiyonu ile 1 değerini veriyoruz.
    # Bilançolar milyon/milyar değerler içerdiğinden buradaki 1 değerinin sonuca etkisi yok denecek kadar az.
    birincikriter(bilancoveriler.get("Toplam Dönen Varlıklar", "1"), bilancoveriler.get("Toplam Kısa Vadeli Yükümlülükler", "1"),
                  gelirtablosuveriler.get("(Esas Faaliyet Dışı) Finansal Gelirler", "1"),
                  gelirtablosuveriler.get("(Esas Faaliyet Dışı) Finansal Giderler (-)", "-1"),
                  gelirtablosuveriler.get("Brüt Kar (Zarar)", "1"))

    ikincikriter(bilancoveriler.get("Nakit ve Nakit Benzerleri", "1"), bilancoveriler.get("Finansal Borçlar", "1"),
                 bilancoveriler.get("Finansal Yatırımlar", "1"))

    ucuncukriter(bilancoveriler.get("Toplam Varlıklar", bilancoveriler.get("VARLIKLAR TOPLAMI",
                bilancoveriler.get("TOPLAM VARLIKLAR" , "1"))), bilancoveriler.get("Toplam Özkaynaklar",
                bilancoveriler.get("ÖZKAYNAKLAR", "1")))

    dorduncukriter(anaadresveriler.get("FAVÖK", "1"), gelirtablosuveriler.get("Satış Gelirleri", "1"), hisse.lower())

    besincikriter(bilancoveriler.get("Toplam Özkaynaklar", bilancoveriler.get("ÖZKAYNAKLAR", "1")),
                  bilancoveriler.get("Ödenmiş Sermaye", "1"))

    # Hissenin kriterlere göre puanını hesaplıyoruz.
    print(f"\nPUAN: {hisse} hissesi inceleme sonucunda 100 üzerinden {puan} puan almıştır.\n")
    # Yukarıda yazdırdığımız için artık puanla işimiz yok bu yüzden 0 yapıp puanı bir sonraki fonksiyona hazır ediyoruz.
    puan = 0

    # Son fonksiyon olan hedef hesaplama fonksiyonunu çağırıyoruz.
    hedefhesapla(hisse.lower())

    # try except bloğu içine alacağımız bir karar değişkeni atıyoruz. Uyarı almamak için önceden string tanımladık.
    karar = ""

    # Tüm işlemler bittikten sonra kullanıcıdan yeni hisse girip girmeyeceğini öğrenip buna göre devam ediyoruz.
    try:
        karar = input("Hesaplama Sonlandı. İlgili verilere yukarıdan ulaşabilirsiniz.\n"
                      "\nAşağıdaki işlemler için belirtilen sayıya basınız"
                      "\n1-Yeni hisse girişi\n2-Çıkış\nİşlem: ")
    except ValueError:
        print("Geçersiz değer girildi")

    if karar == "1":
        anafonksiyon()
    elif karar == "2":
        quit()


# Bütün bu işlemleri bir anafonksiyon altında yaptığımız için fonsiyonu başlatmamız gerekiyor.
anafonksiyon()
