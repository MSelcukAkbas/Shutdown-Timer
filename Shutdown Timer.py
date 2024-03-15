"""""
    Bu uygulamanın çalışması için gereksinimler:
    - Python 3.8 veya daha üstü
        -- Tkinter kütüphanesi
        -- threading modülü
        -- shutil modülü
        -- datetime modülü
        -- subprocess modülü
"""""

# tkinter modülünden gerekli bileşenleri al
from tkinter import Label, Button, Tk, Frame, messagebox
# datetime modülünden datetime ve timedelta sınıflarını al
from datetime import datetime, timedelta
# tkinter.ttk modülünden Combobox sınıfını al
from tkinter.ttk import Combobox
# subprocess modülünden run, TimeoutExpired, CalledProcessError sınıflarını al
from subprocess import run, TimeoutExpired, CalledProcessError

class Kapatma_Zamanlayıcı(Tk):
    def __init__(self):
        """
        Sınıfın başlatıcı metodudur.
        """
        # Ana sınıfın başlatıcı metodunu çağır
        super().__init__()
        # Pencere başlığını ve boyutunu ayarla, yeniden boyutlandırılamaz yap
        self.title("Shutdown Timer")
        self.geometry("300x200")
        self.resizable(False, False)
        # Kullanıcı arayüzünü oluştur
        self.arayuz_olustur()
        # Zamanlayıcının başlangıçta çalışmadığını belirt
        self.calisiyor = False
    def arayuz_olustur(self):
        """
        Kullanıcı arayüzünü oluşturan fonksiyon.
        """
        # Bir çerçeve oluştur
        cerceve = Frame(self)
        cerceve.pack(pady=10)
        # Kalan süreyi gösteren etiketi oluştur ve yerleştir
        self.kalan_sure_etiket = Label(cerceve, font="ariel 15", text="Kalan Zaman: --:--:--")
        self.kalan_sure_etiket.grid(row=0, column=0, columnspan=2)
        # Saat seçimini oluştur ve yerleştir
        Label(cerceve, text="Saat:").grid(row=1, column=0, sticky="e")
        self.saat_secim = Combobox(cerceve, values=list(range(0, 25)), state="readonly", width=5)
        self.saat_secim.grid(row=1, column=1)
        self.saat_secim.set(0)
        # Dakika seçimini oluştur ve yerleştir
        Label(cerceve, text="Dakika:").grid(row=2, column=0, sticky="e")
        self.dakika_secim = Combobox(cerceve, values=list(range(0, 61)), state="readonly", width=5)
        self.dakika_secim.grid(row=2, column=1)
        self.dakika_secim.set(1)
        # Saniye seçimini oluştur ve yerleştir
        Label(cerceve, text="Saniye:").grid(row=3, column=0, sticky="e")
        self.saniye_secim = Combobox(cerceve, values=list(range(0, 61)), state="readonly", width=5)
        self.saniye_secim.grid(row=3, column=1)
        self.saniye_secim.set(0)
        # Başlat düğmesini oluştur ve yerleştir
        self.baslat_dugme = Button(cerceve, text="Başlat", command=self.zamanlayiciyi_baslat)
        self.baslat_dugme.grid(row=4, column=0, columnspan=2, pady=10)
        # Durdur düğmesini oluştur ve yerleştir
        self.durdur_dugme = Button(cerceve, text="Durdur", background="red", command=self.zamanlayiciyi_durdur, state="normal")
        self.durdur_dugme.grid(row=5, column=0, columnspan=2)
    def hata_kayit(self , hata_mesaji):
        """     Foknsiyonlarda meydana gelen hataları kullanıcıya gösterir
                Hatalar için dosyaya yazma işlemini gerçekleştirir.  """
        messagebox.showerror("Hata", hata_mesaji)
    def zamanlayiciyi_baslat(self):
        """
        Zamanlayıcıyı başlatmak için kullanılan fonksiyon.
        """
        # Zamanlayıcının çalıştığını işaretlemek için bir bayrak ayarlanır.
        self.calisiyor = True
        # Kullanıcı arayüzünü güncelle.
        self.arayuz_durumunu_guncelle()
        # Kullanıcı saat, dakika veya saniye seçmemişse hata gösterilir.
        if not all(self.saat_secim.get() or self.dakika_secim.get() or self.saniye_secim.get()):
            messagebox.showerror("Hata", "Lütfen saat, dakika veya saniye seçin.")
            # Zamanlayıcıyı durdur ve kullanıcı arayüzünü güncelle.
            self.calisiyor = False
            self.arayuz_durumunu_guncelle()
            return 
        # Kullanıcının seçtiği saat, dakika ve saniyeler alınır.
        self.saat = int(self.saat_secim.get())
        self.dakika = int(self.dakika_secim.get())
        self.saniye = int(self.saniye_secim.get())
        # Toplam saniyeye çevrilir.
        toplam_saniye = self.saat * 3600 + self.dakika * 60 + self.saniye
        # Başlangıç zamanı kaydedilir.
        self.baslangic_zamani = datetime.now()
        # Bitiş zamanı hesaplanır.
        self.bitis_zamani = self.baslangic_zamani + timedelta(seconds=toplam_saniye)
        # Zamanlayıcıyı güncelle.
        self.zamanlayiciyi_guncelle()
        try:
            # Bilgisayarı kapatma işlemi başlatılır.
            run([r"C:\\Windows\\System32\\shutdown.exe", "/s", "/f", "/t", str(toplam_saniye)], shell=True, timeout=10)
        except PermissionError as per:
            # İzin hatası durumunda hata kaydedilir.
            self.hata_kayit(f"Belirtilen komutun çalıştırma izni yok: {per}")
        except CalledProcessError as cal:
            # Çalışma hatası durumunda hata kaydedilir.
            self.hata_kayit(f"Çalıştırılan işlem bir hata ile sonuçlandı: {cal}")
        except TimeoutExpired as tim:
            # Zaman aşımı durumunda hata kaydedilir.
            self.hata_kayit(f"İşlem zaman aşımına uğradı: {tim}")
        except Exception as base:
            # Diğer hata durumlarında hata kaydedilir.
            self.hata_kayit(f"Program çalışırken bir hata ile karşılaştı: {base}")
    def arayuz_durumunu_guncelle(self):
        """
        Kullanıcı arayüzünün durumunu güncelleyen fonksiyon.
        """
        # Başlatma düğmesinin durumu, zamanlayıcı çalışıyorsa devre dışı bırakılır.
        # Aksi takdirde normal durumdadır.
        self.baslat_dugme["state"] = "disabled" if self.calisiyor else "normal"
        # Durdurma düğmesinin durumu, zamanlayıcı çalışıyorsa normal durumdadır.
        # Aksi takdirde devre dışı bırakılır.
        self.durdur_dugme["state"] = "normal" if self.calisiyor else "disabled"
        # Saat seçiminin durumu, zamanlayıcı çalışmıyorsa sadece okunur durumdadır.
        # Aksi takdirde devre dışı bırakılır.
        self.saat_secim["state"] = "readonly" if not self.calisiyor else "disabled"
        # Dakika seçiminin durumu, zamanlayıcı çalışmıyorsa sadece okunur durumdadır.
        # Aksi takdirde devre dışı bırakılır.
        self.dakika_secim["state"] = "readonly" if not self.calisiyor else "disabled"
        # Saniye seçiminin durumu, zamanlayıcı çalışmıyorsa sadece okunur durumdadır.
        # Aksi takdirde devre dışı bırakılır.
        self.saniye_secim["state"] = "readonly" if not self.calisiyor else "disabled"
    def zamanlayiciyi_durdur(self):
        """
        Zamanlayıcıyı durduran fonksiyon.
        """
        # Zamanlayıcı çalışma durumunu değiştir.
        self.calisiyor = False
        # Kullanıcı arayüzünü güncelle.
        self.arayuz_durumunu_guncelle()
        try:
            # Bilgisayarı kapatma işlemini iptal et.
            run([r"C:\\Windows\\System32\\shutdown.exe", "/a"], shell=True, timeout=10)
        except PermissionError as per:
            # İzin hatası durumunda hata kaydedilir.
            self.hata_kayit(f"Belirtilen komutun çalıştırma izni yok: {per}")
        except CalledProcessError as cal:
            # Çalışma hatası durumunda hata kaydedilir.
            self.hata_kayit(f"Çalıştırılan işlem bir hata ile sonuçlandı: {cal}")
        except TimeoutExpired as tim:
            # Zaman aşımı durumunda hata gösterilir.
            messagebox.showerror(f"İşlem zaman aşımına uğradı: {tim}")
        except Exception as base:
            # Diğer hata durumlarında hata kaydedilir.
            self.hata_kayit(f"Program çalışırken bir hata ile karşılaştı: {base}")
        # Kalan süre etiketini güncelle.
        self.kalan_sure_etiket.config(text="Çalışan Görev Yok")
    def zamanlayiciyi_guncelle(self):
        """
        Zamanlayıcıyı güncelleyen ve kalan zamanı gösteren fonksiyon.
        """
        if self.calisiyor:
            # Kalan zamanı hesapla.
            kalan_zaman = self.bitis_zamani - datetime.now()
            
            # Saniyeyi saat, dakika ve saniyeye dönüştür.
            saat, kalan = divmod(kalan_zaman.total_seconds(), 3600)
            dakika, saniye = divmod(kalan, 60)
            # Kalan süreyi ekrana yazdır.
            self.kalan_sure_etiket.config(text=f"Kalan Zaman: {int(saat):02d}:{int(dakika):02d}:{int(saniye):02d}")
            # Her 1 saniyede bir güncelleme yapmak için after fonksiyonunu kullan.
            self.after(1000, self.zamanlayiciyi_guncelle)
if __name__ == "__main__":

    uygulama = Kapatma_Zamanlayıcı()
    uygulama.mainloop()