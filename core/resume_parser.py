import io
import zipfile
import olefile
from typing import Union
from pdfminer.high_level import extract_text
from docx import Document

def parse_pdf(file) -> str:
    """Парсинг PDF с обработкой ошибок"""
    try:
        if hasattr(file, 'read'):
            file_bytes = file.read()
        else:
            file_bytes = file
            
        with io.BytesIO(file_bytes) as f:
            return extract_text(f)
    except Exception as e:
        raise ValueError(f"Ошибка чтения PDF: {str(e)}")

def parse_docx(file) -> str:
    """Парсинг DOCX"""
    try:
        if hasattr(file, 'read'):
            file_bytes = file.read()
        else:
            file_bytes = file
            
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        raise ValueError(f"Ошибка чтения DOCX: {str(e)}")

def parse_doc(file) -> str:
    """Парсинг старых DOC"""
    try:
        if hasattr(file, 'read'):
            file_bytes = file.read()
        else:
            file_bytes = file
            
        with io.BytesIO(file_bytes) as f:
            if not olefile.isOleFile(f):
                raise ValueError("Неверный формат DOC")
                
            ole = olefile.OleFileIO(f)
            if ole.exists('WordDocument'):
                stream = ole.openstream('WordDocument')
                text = stream.read().decode('latin-1', errors='ignore')
                return ' '.join(text.split()).strip()
                
        raise ValueError("Не удалось извлечь текст из DOC")
    except Exception as e:
        raise ValueError(f"Ошибка чтения DOC: {str(e)}")

def parse_txt(file) -> str:
    """Парсинг TXT"""
    try:
        if hasattr(file, 'read'):
            file_bytes = file.read()
        else:
            file_bytes = file
            
        for encoding in ['utf-8', 'cp1251', 'windows-1251']:
            try:
                return file_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError("Не удалось определить кодировку")
    except Exception as e:
        raise ValueError(f"Ошибка чтения TXT: {str(e)}")

def parse_resume(file) -> str:
    """Основной парсер"""
    if not file:
        raise ValueError("Файл не загружен")
        
    filename = file.name.lower() if hasattr(file, 'name') else "file"
    
    try:
        if filename.endswith('.pdf'):
            return parse_pdf(file)
        elif filename.endswith('.docx'):
            return parse_docx(file)
        elif filename.endswith('.doc'):
            return parse_doc(file)
        elif filename.endswith('.txt'):
            return parse_txt(file)
        else:
            raise ValueError("Неподдерживаемый формат файла")
    except Exception as e:
        raise ValueError(f"Ошибка обработки файла: {str(e)}")