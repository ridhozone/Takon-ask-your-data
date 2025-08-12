import os
import io
import fitz
import docx


def extract_pdf(_filename: str, content: bytes):
    try:
        doc = fitz.open(stream=content, filetype="pdf")
        text = "".join(page.get_text() for page in doc)
        return text.strip()

    except Exception as e:
        raise ValueError(f"PDF extraction error: {str(e)}")


def extract_docx(_filename: str, content: bytes):
    try:
        doc = docx.Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs).strip()

    except Exception as e:
        raise ValueError(f"DOCX extraction error: {str(e)}")


def extract_txt(_filename: str, content: bytes):
    try:
        return content.decode("utf-8").strip()

    except Exception as e:
        raise ValueError(f"TXT extraction error: {str(e)}")


def extract_mp3(filename: str, content: bytes):
    try:
        from groq import Groq
        from utils_rag.secret import groq_key

        client = Groq(api_key=groq_key)
        transcription = client.audio.transcriptions.create(
            file=(filename, content),
            model="whisper-large-v3-turbo",
        )
        return transcription.text.strip()

    except Exception as e:
        raise ValueError(f"MP3 transcription error: {str(e)}")


handlers = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".txt": extract_txt,
    ".mp3": extract_mp3,
}


def extractor(filename: str, content: bytes):
    ext = os.path.splitext(filename)[1].lower()

    if ext not in handlers:
        raise ValueError(f"Unsupported file type: {ext}")

    return handlers[ext](filename, content)
