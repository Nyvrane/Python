# Yazilimlar
Bu kisimda kendimi gelistimek amaciyla yapmis oldugum yazilimlar bulunmaktadir.

BorsaAnalizApp.py ve BorsaAnalizAppGörsel.py
Amaç: Bu program BİST'te bulunan hisseler üzerinde, yatırım tavsiyesi içermeden bir takım temel analizler yapar. 
Hedef: Yazılım alanında eğitim kapsamında oluşturulmuştur ve yatırım tavsiyesi vermeyi hedeflemez.
Yöntem: Python programlama dilinde BeautifulSoup ve request modülleri vasıtasıyla girilen bir hisse adının Fintables.com sitesinden çekilen verileri kullanılarak analizi yapılır.
İçerik: Borsa Analiz App.py dosyası python konsolu üzerinden çalışırken BorsaAnalizAppGörsel.py dosyası PyQt5 modülü ile görselleştirilmiştir. Herhangi bir ücretli API veya üyelik kullanılmadığından ücret ve kullanıcı girişi talep edilmemektedir.
Elde Edilen Veri: Borsada bulunan hisselerin 5 kriter açısından analiz edilmesi ve bulunduğu sektöre ve temel piyasa çarpanlarına göre hedef fiyat bilgilerininin yatırım tavsiyesi içermeksizin analiz sonuçları.
Güncelleme: Borsa Analiz App'in web scraping yöntemiyle veri çektiği sitenin yapısı değişti ve sektör ortalamaları verileri kaldırıldı. Bu nedenle hedef fiyat ve sektör karlılık analiz işlevleri bozuldu ve çalışmamakta.
