
"""
    Senaryo:

    1- Lokasyon Belirleme: 10 noktadan oluşan bir bölgede ihtiyaç malzemelerinin dağıtımı yapılacak. 
    Bu noktalar, harita üzerinde belirli koordinatlara sahip olan ve ihtiyaç malzemelerinin teslim edileceği noktalardır.

    2- Graf Oluşturma: Belirlenen noktalar arasında bir graf oluşturulur ve ihtiyaç malzemelerinin stoklarına göre ağırlıklandırılır.
    Grafın düğümleri, belirlediğimiz 10 nokta olacaktır ve kenarlar, bu noktalar arasındaki rota olacaktır.

    3- En Kısa Yol Belirleme: Graf teorisindeki en kısa yol algoritması kullanılarak, ihtiyaç malzemelerinin dağıtımını yapacağımız 
    rotayı belirleriz. Bu, ihtiyaç malzemelerinin en çok ihtiyaç duyulan noktalara en kısa sürede ulaşmasını sağlayacaktır.

    4- Öncelik Sırasına Göre Dağıtım: Belirlediğimiz rotayı takip ederek, her noktaya ihtiyaç malzemelerini dağıtırız. 
    Dağıtım, belirlenen öncelik sırasına göre yapılmalıdır. Yani öncelik sırasında sağlık malzemeleri, temel gıda, ısınma gereci 
    ve giyecek sırasıyla dağıtılmalıdır.

    5- Araç Kullanımı: Dağıtım sırasında, belirlediğimiz rotayı takip ederek, en kısa sürede ve en az miktarda malzeme kullanarak 
    dağıtım yapmak için drone veya araç gibi araçları kullanabiliriz.

    6- Stok Güncelleme: Dağıtım sonrası, kalan stokları güncellemeli ve ihtiyaç duyulan noktalara yeniden malzeme taşıma planı 
    yapmalıyız. Bu planı yaparken de öncelik sırasına ve stok miktarına göre hareket etmeliyiz.

    7- Acil Müdahale: Dağıtım sırasında ve sonrasında herhangi bir sorun veya aksaklık durumunda acil müdahale ekiplerini çağırmalı 
    ve yardım istemeliyiz.

    8- Veri Analizi: Daha sonraki dağıtımlarda, önceki dağıtımların verilerini kullanarak daha etkili bir dağıtım planı yapabilir
    ve süreci daha verimli hale getirebiliriz.
       
"""

#%%
# import library
import networkx as nx
import matplotlib.pyplot as plt
import heapq

#%%

# Lokasyon Belirleme: 10 noktadan oluşan bir bölgede ihtiyaç malzemelerinin dağıtımı yapılacak. 
# Bu noktalar, harita üzerinde belirli koordinatlara sahip olan ve ihtiyaç malzemelerinin teslim edileceği noktalardır.

# Belirlenen 10 noktanın koordinatları birer dictionary olarak tanımlandı 
noktalar = {
    "Hastane": (41.008236, 28.973454),
    "Okul": (41.006919, 28.968986),
    "Belediye": (41.003942, 28.970025),
    "Spor Salonu": (41.009324, 28.967496),
    "Market": (41.009861, 28.972123),
    "Park": (41.003658, 28.973859),
    "Cami": (41.006293, 28.972932),
    "Kütüphane": (41.007840, 28.971327),
    "Stadyum": (41.007512, 28.966402),
    "İtfaiye": (41.004833, 28.971137)
}

# Stoktaki bilgiler 

stoklar = {
    "sağlık malzemesi": 100,
    "temel gıda": 100,
    "ısınma gereci": 70,
    "giyecek": 70
}


# Öncelik sırası belirleme
oncelik_sirasi = {
    "sağlık malzemesi": 1,
    "temel gıda": 2,
    "ısınma gereci": 3,
    "giyecek": 4
}


# İhtiyaç malzemelerinin stokları 
# İhtiyaç malzemeleri hangi noktalara ne kadar gideceğini belirledik 
ihtiyac_stoklari = {
    "Hastane": {"sağlık malzemesi": 25, "temel gıda": 20, "ısınma gereci": 10, "giyecek": 16},
    "Okul": {"sağlık malzemesi": 10, "temel gıda": 20, "ısınma gereci": 12, "giyecek": 13},
    "Belediye": {"sağlık malzemesi": 13, "temel gıda": 15, "ısınma gereci":8, "giyecek": 11},
    "Spor Salonu": {"sağlık malzemesi": 7, "temel gıda": 5, "ısınma gereci": 6, "giyecek": 2},
    "Market": {"sağlık malzemesi": 11, "temel gıda": 10, "ısınma gereci": 0, "giyecek": 4},
    "Park": {"sağlık malzemesi": 4, "temel gıda": 0, "ısınma gereci": 10, "giyecek": 8},
    "Cami": {"sağlık malzemesi": 10, "temel gıda": 6, "ısınma gereci": 4, "giyecek": 6},
    "Kütüphane": {"sağlık malzemesi": 0, "temel gıda": 10, "ısınma gereci": 10, "giyecek": 1},
    "Stadyum": {"sağlık malzemesi": 8, "temel gıda": 0, "ısınma gereci": 3, "giyecek": 0},
    "İtfaiye": {"sağlık malzemesi": 12, "temel gıda": 14, "ısınma gereci": 7, "giyecek": 9},
}

#%%  

# Graf Oluşturma: Belirlenen noktalar arasında bir graf oluşturulur ve ihtiyaç malzemelerinin stoklarına göre ağırlıklandırılır. 
# Grafın düğümleri, belirlediğimiz 10 nokta olacaktır ve kenarlar, bu noktalar arasındaki rota olacaktır.

# Boş bir graf oluştur
graf = nx.Graph()

# Noktaları düğümler olarak ekle
for nokta, koordinat in noktalar.items():
    graf.add_node(nokta, pos=koordinat)

# Kenarları ekle ve ağırlıklarını belirle
for nokta, ihtiyaclar in ihtiyac_stoklari.items():
    for diger_nokta, diger_ihtiyaclar in ihtiyac_stoklari.items():
        if nokta != diger_nokta:
            agırlık = 0
            for ihtiyac, miktar in ihtiyaclar.items():
                if miktar > 0:
                    oncelik = oncelik_sirasi[ihtiyac.lower()]
                    agırlık += (miktar / stoklar[ihtiyac]) * oncelik
            graf.add_edge(nokta, diger_nokta, weight=agırlık)

# Kenarların ağırlıklarını düzenle
agırlıklar = nx.get_edge_attributes(graf, 'weight')
nx.set_edge_attributes(graf, agırlıklar, 'weight')
            
            
# yukarıda belirlediğimiz nokta, kenarlar ve ağırlıklar ile bir boş sayfa üzerinde noktalar ve aralarındaki ilişkilerini
# Python'ın matplotlib ve networkx kütüphaneleri ile görselleştirme yaptık.
# Grafı çizdirme
pos = nx.spring_layout(graf)
nx.draw_networkx_nodes(graf, pos, node_size=500)
nx.draw_networkx_labels(graf, pos, font_size=10, font_family="sans-serif")
nx.draw_networkx_edges(graf, pos, width=2, edge_color="blue")
nx.draw_networkx_edge_labels(graf, pos, font_size=8)
plt.axis("off")
plt.show()



#%%

# En Kısa Yol Belirleme: Graf teorisindeki en kısa yol algoritması kullanılarak, ihtiyaç malzemelerinin dağıtımını yapacağımız 
# rotayı belirleriz. Bu, ihtiyaç malzemelerinin en çok ihtiyaç duyulan noktalara en kısa sürede ulaşmasını sağlayacaktır.

# Graf modelimizin dijkstra algoritmasını kullanarak en kısa yolu buluyoruz.

# En kısa yol algoritması
def dijkstra(graf, baslangic):
    distances = {node: float('inf') for node in graf}  # Tüm noktalara sonsuz mesafe atanır.
    distances[baslangic] = 0  # Başlangıç noktasının mesafesi 0 olarak atanır.
    heap = [(0, baslangic)]  # Heap sırası, mesafeleri saklamak için kullanılır.
    while heap:
        (current_distance, current_node) = heapq.heappop(heap)  # Heap sırasından en küçük mesafeli düğüm seçilir.
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graf[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))  # Heap sırasına eklenir.
    return distances



#%%

# Öncelik Sırasına Göre Dağıtım: Belirlediğimiz rotayı takip ederek, her noktaya ihtiyaç malzemelerini dağıtırız. 
# Dağıtım, belirlenen öncelik sırasına göre yapılmalıdır. Yani öncelik sırasında sağlık malzemeleri, temel gıda, 
# ısınma gereci ve giyecek sırasıyla dağıtılmalıdır.

# Dağıtım planı oluşturma
dagitim_plani = []
# Öncelik sırasına göre dağıtım yap
for oncelik in oncelik_sirasi.values():
    for nokta in noktalar:
        ihtiyaclar = noktalar[nokta]
        if ihtiyaclar[oncelik] > 0:
            en_kisa_yollar = []
            for hedef in stoklar:
                print(type(hedef))
                for ihtiyaclar2 in range(stoklar[hedef]):
                    if ihtiyaclar2[oncelik] > 0:
                        # En kısa yolu bul
                        yol = dijkstra(nokta, hedef)
                        if yol is not None:
                            en_kisa_yollar.append((hedef, yol))
                    """
                        - 'oncelik_sirasi' olarak tanımladığımız dictionary ın değerlerini 'oncelik' adlı değişkenimize atadık.
                        - noktalar adlı dictionary içinde nokta adlı değişkenimizi döngü ile gezdiriyoruz.
                        - ihtiyaçlar değişkenimizi atanan 'oncelik_sirasi' değerlerini sıfırdan büyük olma koşulana bakarak koda devama ediyoruz.
                        - 'en_kisa_yollar' adlı bir boş dizi oluşturuyoruz.
                        - 'hedef' adlı değişkenimizi 'stoklar' adlı dictionary içinde geziniyoruz
                        - 'ihtiyaçlar2' adlı değişkenimizi 'stoklar[hedef]' içinde gezerek 'oncelik_sirasina' göre sıfırdan büyük 
                        olup olmama koşulundan geçiyoruz.
                        - Eğer varsa 'yol' adlı değişkenimize 'dijkstra' algoritmasını çağırarak 'nokta' ve 'hedef' değerlerini 
                        algoritmanın içine gönderiyoruz. 
                        - 'yol' boş olmadığı sürece 'en_kisa_yollar' adlı dizimize 'hedef' ve 'yol' değişkenlerini atıyoruz.
                        
                    """

            # En kısa yolu seç
            en_kisa_yollar = sorted(en_kisa_yollar, key=lambda x: x[1])
            if len(en_kisa_yollar) > 0:
                en_kisa_yol = en_kisa_yollar[0][1]
                hedef = en_kisa_yollar[0][0]
                
                """
                    -'en_kisa_yollar' değişkenini sıralama yapıyoruz.
                    - Daha sonra 'en_kisa_yollar' uzunluğu sıfırdan küçük olmadığı sürece 'en_kisa_yollar' dizimiz parçalıyoruz.
                    - 'en_kisa_yol' ve 'hedef' adli değişkenlere diziyi atıyoruz.
                """

                # İhtiyaçları karşıla
                for ihtiyac in oncelik_sirasi[oncelik]:
                    if ihtiyaclar[ihtiyac] > 0 and stoklar[hedef][ihtiyac] > 0:
                        ihtiyac_miktari = min(ihtiyaclar[ihtiyac], stoklar[hedef][ihtiyac])
                        dagitim_plani[ihtiyac] += ihtiyac_miktari
                        ihtiyaclar[ihtiyac] -= ihtiyac_miktari
                        stoklar[hedef][ihtiyac] -= ihtiyac_miktari

                    """
                        - 'ihtiyac_miktari' adlı değişkene ihtiyaçdaki ve stoklardaki en az değerleri alarak atıyoruz
                        - Daha sonra üstte tanımladığımız 'dagitim_plani' dizimize 'idtiyac_miktarini' ekliyoruz.
                        'ihtiyaclar' ve 'stoklar' dan 'ihtiyac_miktarini' çıkartıyoruz.
                    """
                            
# Dağıtım planı yazdırma
print("Dağıtım Planı:")
for ihtiyac, miktar in dagitim_plani.items():
    print(f"{ihtiyac.capitalize()}: {miktar}")

# Kalan stokları yazdırma
print("\nKalan Stoklar:")
for nokta, stoklar in stoklar.items():
    print(f"{nokta.capitalize()}: {stoklar}")                         
                            
#%%

# Araç Kullanımı: Dağıtım sırasında, belirlediğimiz rotayı takip ederek, en kısa sürede ve en az miktarda malzeme kullanarak 
# dağıtım yapmak için drone veya araç gibi araçları kullanabiliriz.
  
def arac_kullan(en_kisa_yol, hedef, arac_tipi, dagitim_plani):
    
    if arac_tipi == 'drone':
        print('\nDrone kullanılarak dağıtım yapılıyor.\n')
        for i in range(len(en_kisa_yol)):
            for j in range(len(dagitim_plani)):     
                print(f'{en_kisa_yol[i]} noktasından {hedef[i]} noktasına {dagitim_plani[j]} malzemesi götürüldü.')
    elif arac_tipi == 'araç':
        print('*\nAraç kullanılarak dağıtım yapılıyor.\n')
        for i in range(len(en_kisa_yol)):
            for j in range(len(dagitim_plani)):     
                print(f'{en_kisa_yol[i]} noktasından {hedef[i]} noktasına {dagitim_plani[j]} malzemesi götürüldü.')
    else:
        print('Geçersiz araç tipi.')
       
        
        
arac_tipi = input("Dağıtım yapmak istediğiniz araç tipini seçiniz(drone/araç): ")

en_kisa_yol = ["Market", "Kütüphane","Cami", "İtfaiye", "Hastane", "Belediye", "Belediye", "Okul", "Spor Salonu", "Spor Salonu"]
hedef = ["Hastane","Okul","Belediye", "Spor Salonu", "Market", "Park", "Cami","Kütüphane", "Stadyum", "İtfaiye"]

dagitim_plani = ["Sağlık Malzemesi", "Temel Gıda", "Isınma Gereci", "Giyecek"]



"""
    - Araç tipi kullanıcıdan alınarak nasıl dağıtım yapılmasını tercih ediyor.
    
    - Yukarıda ufak sıkıntıdan kodun çalışamadığından dolayı kodun devamında başka sıkıntılar olmaması için;
'en_kisa_yol' ve 'hedef' diye iki dizi içerisine yukarıda içine atama yapamadığımdan dolayı burada kendim değerler verdim.
Hangi noktanın diğer noktalara göre en kısa mesafede olduğunu bulup tanımladığım diziye elle yazdım.

    - Yukarıda çalışmayan kodun alt tarafında dagitim_plani olarak tanımlanan dizi içerisine hangi noktaya hangi öncelik sırasına göre
kaç tane malzeme gideceği ayarlanmıştı. Bu dediklerim olmadığından dolayı ben burada sadece öncelik sırasını elle yazabildim. 
En azından ekranda görüntü olabilmesi için

    - Daha sonrasında yazdığımız fonksiyonu çağırıyoruz.

"""

arac_kullan(en_kisa_yol, hedef, arac_tipi, dagitim_plani)




#%%

# Stok Güncelleme: Dağıtım sonrası, kalan stokları güncellemeli ve ihtiyaç duyulan noktalara yeniden malzeme taşıma planı yapmalıyız.
# Bu planı yaparken de öncelik sırasına ve stok miktarına göre hareket etmeliyiz.

def stok_güncelleme(stoklar, ihtiyaclar):
    for i in range(len(stoklar)):
        stoklar[i] -= ihtiyaclar[i]
        if stoklar[i] < 0:
            stoklar[i] = 0
    return stoklar
 
stok_güncelleme(stoklar, ihtiyaclar)

"""
    - Stok güncellemesinde for döngümüz stokların uzunluğu kadar döner. 
    - Daha sonra hangi stoklardan ne kadar ihtiyaç edilerek gönderilmiş olanı çıkartıyoruz ve güncel stoklarımızı dönderiyoruz. 
    - Burada kod çalıştığı zaman hata veriyor çünkü yukarıdaki hatadan dolayı 'ihtiyaclar' değişkenimizin içerisinde 
    tam veri bulunmamaktadır.
"""

#%%  
# Acil Müdahale: Dağıtım sırasında ve sonrasında herhangi bir sorun veya aksaklık durumunda 
# acil müdahale ekiplerini çağırmalı ve yardım istemeliyiz.


def acil_mudahale():
    # Acil bir durum olduğunda, müdahale ekibini çağırmak için bu fonksiyon kullanılır.
    # Fonksiyon, acil müdahale ekibini çağırır ve yardım talebinde bulunur.
    print("Acil durum! Yardım isteniyor!")
    # Acil müdahale ekibi çağırılır ve yardım talebinde bulunulur
    acil_durum_ekibini_ara("Hatay")

def acil_durum_ekibini_ara(konum):
    """
    Verilen konuma acil müdahale ekibi çağırır.
    """
    print(f"Acil müdahale ekibi, {konum} konumuna yönlendiriliyor...")
    # burada gerçek hayatta yapılacak işlemler yer alır
    # örneğin, konuma en yakın ambulans, polis veya itfaiye ekibi yönlendirilir

acil_mudahale()


#%% 

# Veri Analizi: Daha sonraki dağıtımlarda, önceki dağıtımların verilerini kullanarak daha etkili bir dağıtım planı yapabilir 
# ve süreci daha verimli hale getirebiliriz.


def analiz_et(onceden_yapilan_teslimatlar):
    # onceden_yapilan_teslimatlar, her bir önceki teslimat için teslimat verilerini içeren bir demet listesidir
    # her bir demet (lokasyon, teslim_edilen_ürünler, teslimat_süresi) içerir

    # Ortalama teslimat süresini hesaplar
    toplam_sure = 0
    for teslimat in onceden_yapilan_teslimatlar:
        toplam_sure += teslimat[2]
    ortalama_sure = toplam_sure / len(onceden_yapilan_teslimatlar)

    # Sık talep edilen ürünleri belirler
    urun_sayisi = {}
    for teslimat in onceden_yapilan_teslimatlar:
        for urun in teslimat[1]:
            if urun in urun_sayisi:
                urun_sayisi[urun] += 1
            else:
                urun_sayisi[urun] = 1
    sık_urunler = sorted(urun_sayisi.items(), key=lambda x: x[1], reverse=True)

    # Sık talep edilen lokasyonları belirler
    lokasyon_sayisi = {}
    for teslimat in onceden_yapilan_teslimatlar:
        lokasyon = tuple(teslimat[0])
        if lokasyon in lokasyon_sayisi:
            lokasyon_sayisi[lokasyon] += 1
        else:
            lokasyon_sayisi[lokasyon] = 1
    sık_lokasyonlar = sorted(lokasyon_sayisi.items(), key=lambda x: x[1], reverse=True)

    # Analiz sonuçlarını bir sözlük olarak döndürür
    analiz_sonuclari = {
        "ortalama_teslimat_suresi": ortalama_sure,
        "sik_talep_edilen_urunler": sık_urunler,
        "sik_talep_edilen_lokasyonlar": sık_lokasyonlar
    }
    

    return analiz_sonuclari


onceden_yapilan_teslimatlar = [
    (["Hastane","Okul","Belediye","Spor Salonu","Market","Park","Cami","Kütüphane","Stadyum","İtfaiye"],
     ["Sağlık malzemesi", "Temel Gıda", "Isınma gereci", "Giyecek"],
     2),
    (["Hastane","Okul","Belediye","Spor Salonu","Kütüphane","Stadyum","İtfaiye"],
     ["Sağlık malzemesi", "Temel Gıda", "Isınma gereci"],
     1),
    (["Belediye","Spor Salonu","Kütüphane","Stadyum","İtfaiye"],
     ["Sağlık malzemesi","Isınma gereci"],
     13),
]


"""
    - Buradaki kodda önceden yapılan teslimatların ortalama sürelerini, sık talep edilen ürünlerini ve sık talep edilen lokasyonlarını 
analiz sonucu yazdırıyoruz.
    - Tabi buradaki koda önceden yapılan teslimatlar diye elle ekleme yaptım. Yukarıdaki kodun çalışmayarak devam edemediği için
    - Aşağıda fonksiyonu çalıştırıyoruz. 
"""        

analiz_et(onceden_yapilan_teslimatlar)      
         
#%%


"""
    ------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------
    Hocam elimizden geldiği kadar kodu yazmaya ve çalıştırmaya çalıştık.
    Bazı yerlerde durumlar istediğimiz gibi gitmedi.
    Bu durumları kendimizce açıklmaya çalıştık.
    Kodun gerisinde kalan kısımları da elle değerler verek en azından kodu çalıştırmaya çalıştık.
    ------------------------------------------------------------------------------------------------------------------------
    ------------------------------------------------------------------------------------------------------------------------
"""


                       