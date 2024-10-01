"""""
    Bu uygulamanın çalışması için gereksinimler:
    - Python 3.8 veya daha üstü
        -- Tkinter kütüphanesi
        -- threading modülü
        -- shutil modülü
        -- datetime modülü
        -- subprocess modülü
"""""

from tkinter import Label, Button, Tk, Frame, messagebox
from datetime import datetime, timedelta
from tkinter.ttk import Combobox
from subprocess import run, TimeoutExpired, CalledProcessError

class Kapatma_Zamanlayıcı(Tk):
    def __init__(self):
        """
        Sınıfın başlatıcı metodudur.
        """
        super().__init__()
        self.title("Shutdown Timer")
        self.geometry("300x200")
        self.resizable(False, False)
        self.arayuz_olustur()
        self.calisiyor = False
    def arayuz_olustur(self):
        """
        Kullanıcı arayüzünü oluşturan fonksiyon.
        """
        cerceve = Frame(self)
        cerceve.pack(pady=10)
        self.kalan_sure_etiket = Label(cerceve, font="ariel 15", text="Kalan Zaman: --:--:--")
        self.kalan_sure_etiket.grid(row=0, column=0, columnspan=2)
        Label(cerceve, text="Saat:").grid(row=1, column=0, sticky="e")
        self.saat_secim = Combobox(cerceve, values=list(range(0, 25)), state="readonly", width=5)
        self.saat_secim.grid(row=1, column=1)
        self.saat_secim.set(0)
        Label(cerceve, text="Dakika:").grid(row=2, column=0, sticky="e")
        self.dakika_secim = Combobox(cerceve, values=list(range(0, 61)), state="readonly", width=5)
        self.dakika_secim.grid(row=2, column=1)
        self.dakika_secim.set(1)
        Label(cerceve, text="Saniye:").grid(row=3, column=0, sticky="e")
        self.saniye_secim = Combobox(cerceve, values=list(range(0, 61)), state="readonly", width=5)
        self.saniye_secim.grid(row=3, column=1)
        self.saniye_secim.set(0)
        self.baslat_dugme = Button(cerceve, text="Başlat", command=self.zamanlayiciyi_baslat)
        self.baslat_dugme.grid(row=4, column=0, columnspan=2, pady=10)
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
        self.calisiyor = True
        self.arayuz_durumunu_guncelle()
        if not all(self.saat_secim.get() or self.dakika_secim.get() or self.saniye_secim.get()):
            messagebox.showerror("Hata", "Lütfen saat, dakika veya saniye seçin.")
            self.calisiyor = False
            self.arayuz_durumunu_guncelle()
            return 
        self.saat = int(self.saat_secim.get())
        self.dakika = int(self.dakika_secim.get())
        self.saniye = int(self.saniye_secim.get())
        toplam_saniye = self.saat * 3600 + self.dakika * 60 + self.saniye
        self.baslangic_zamani = datetime.now()
        self.bitis_zamani = self.baslangic_zamani + timedelta(seconds=toplam_saniye)
        self.zamanlayiciyi_guncelle()
        try:
            run([r"C:\\Windows\\System32\\shutdown.exe", "/s", "/f", "/t", str(toplam_saniye)], shell=True, timeout=10)
        except PermissionError as per:
            self.hata_kayit(f"Belirtilen komutun çalıştırma izni yok: {per}")
        except CalledProcessError as cal:
            self.hata_kayit(f"Çalıştırılan işlem bir hata ile sonuçlandı: {cal}")
        except TimeoutExpired as tim:
            self.hata_kayit(f"İşlem zaman aşımına uğradı: {tim}")
        except Exception as base:
            self.hata_kayit(f"Program çalışırken bir hata ile karşılaştı: {base}")
    def arayuz_durumunu_guncelle(self):
        """
        Kullanıcı arayüzünün durumunu güncelleyen fonksiyon.
        """
        # Aksi takdirde normal durumdadır.
        self.baslat_dugme["state"] = "disabled" if self.calisiyor else "normal"
        # Aksi takdirde devre dışı bırakılır.
        self.durdur_dugme["state"] = "normal" if self.calisiyor else "disabled"
        # Aksi takdirde devre dışı bırakılır.
        self.saat_secim["state"] = "readonly" if not self.calisiyor else "disabled"
        # Aksi takdirde devre dışı bırakılır.
        self.dakika_secim["state"] = "readonly" if not self.calisiyor else "disabled"
        # Aksi takdirde devre dışı bırakılır.
        self.saniye_secim["state"] = "readonly" if not self.calisiyor else "disabled"
    def zamanlayiciyi_durdur(self):
        """
        Zamanlayıcıyı durduran fonksiyon.
        """
        self.calisiyor = False
        self.arayuz_durumunu_guncelle()
        try:
            run([r"C:\\Windows\\System32\\shutdown.exe", "/a"], shell=True, timeout=10)
        except PermissionError as per:
            self.hata_kayit(f"Belirtilen komutun çalıştırma izni yok: {per}")
        except CalledProcessError as cal:
            self.hata_kayit(f"Çalıştırılan işlem bir hata ile sonuçlandı: {cal}")
        except TimeoutExpired as tim:
            messagebox.showerror(f"İşlem zaman aşımına uğradı: {tim}")
        except Exception as base:
            self.hata_kayit(f"Program çalışırken bir hata ile karşılaştı: {base}")
        self.kalan_sure_etiket.config(text="Çalışan Görev Yok")
    def zamanlayiciyi_guncelle(self):
        """
        Zamanlayıcıyı güncelleyen ve kalan zamanı gösteren fonksiyon.
        """
        if self.calisiyor:
            kalan_zaman = self.bitis_zamani - datetime.now()
            saat, kalan = divmod(kalan_zaman.total_seconds(), 3600)
            dakika, saniye = divmod(kalan, 60)
            self.kalan_sure_etiket.config(text=f"Kalan Zaman: {int(saat):02d}:{int(dakika):02d}:{int(saniye):02d}")
            self.after(1000, self.zamanlayiciyi_guncelle)
if __name__ == "__main__":

    uygulama = Kapatma_Zamanlayıcı()
    uygulama.mainloop()