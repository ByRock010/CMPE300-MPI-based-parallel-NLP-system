#!/usr/bin/env python3
"""
PDF Metin Çıkarma Scripti
Bu script PDF dosyalarından metin çıkarır ve bir text dosyasına kaydeder.
"""

import sys
import os

def extract_with_pypdf2(pdf_path):
    """PyPDF2 kullanarak metin çıkar"""
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"Toplam sayfa sayısı: {len(reader.pages)}")
            for i, page in enumerate(reader.pages, 1):
                print(f"Sayfa {i} işleniyor...", end='\r')
                text += f"\n{'='*80}\n"
                text += f"SAYFA {i}\n"
                text += f"{'='*80}\n\n"
                text += page.extract_text()
                text += "\n\n"
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"\nPyPDF2 ile hata: {e}")
        return None

def extract_with_pdfplumber(pdf_path):
    """pdfplumber kullanarak metin çıkar (daha iyi sonuçlar)"""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Toplam sayfa sayısı: {len(pdf.pages)}")
            for i, page in enumerate(pdf.pages, 1):
                print(f"Sayfa {i} işleniyor...", end='\r')
                text += f"\n{'='*80}\n"
                text += f"SAYFA {i}\n"
                text += f"{'='*80}\n\n"
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                text += "\n\n"
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"\npdfplumber ile hata: {e}")
        return None

def extract_with_pymupdf(pdf_path):
    """PyMuPDF (fitz) kullanarak metin çıkar"""
    try:
        import fitz  # PyMuPDF
        text = ""
        doc = fitz.open(pdf_path)
        print(f"Toplam sayfa sayısı: {len(doc)}")
        for i in range(len(doc)):
            print(f"Sayfa {i+1} işleniyor...", end='\r')
            page = doc[i]
            text += f"\n{'='*80}\n"
            text += f"SAYFA {i+1}\n"
            text += f"{'='*80}\n\n"
            text += page.get_text()
            text += "\n\n"
        doc.close()
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"\nPyMuPDF ile hata: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python3 extract_pdf_text.py <pdf_dosyası> [çıktı_dosyası]")
        print("\nÖrnek:")
        print("  python3 extract_pdf_text.py CMPE_300_P2.pdf")
        print("  python3 extract_pdf_text.py CMPE_300_P2.pdf output.txt")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"Hata: '{pdf_path}' dosyası bulunamadı!")
        sys.exit(1)
    
    # Çıktı dosyası adı
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    else:
        base_name = os.path.splitext(pdf_path)[0]
        output_file = f"{base_name}_extracted.txt"
    
    print(f"PDF dosyası: {pdf_path}")
    print(f"Çıktı dosyası: {output_file}")
    print("\nMetin çıkarılıyor...\n")
    
    # Önce pdfplumber dene (en iyi sonuçlar)
    text = extract_with_pdfplumber(pdf_path)
    
    # pdfplumber yoksa PyMuPDF dene
    if text is None:
        text = extract_with_pymupdf(pdf_path)
    
    # PyMuPDF yoksa PyPDF2 dene
    if text is None:
        text = extract_with_pypdf2(pdf_path)
    
    # Hiçbiri yoksa hata ver
    if text is None:
        print("\nHata: PDF okuma kütüphanesi bulunamadı!")
        print("\nLütfen şu kütüphanelerden birini yükleyin:")
        print("  pip install pdfplumber  (önerilen)")
        print("  pip install PyMuPDF")
        print("  pip install PyPDF2")
        sys.exit(1)
    
    # Metni dosyaya kaydet
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\n\n✓ Başarılı! Metin '{output_file}' dosyasına kaydedildi.")
        print(f"  Toplam karakter sayısı: {len(text)}")
    except Exception as e:
        print(f"\nHata: Dosyaya yazılamadı: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

