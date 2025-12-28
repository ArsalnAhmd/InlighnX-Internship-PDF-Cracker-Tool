# PDF Password Cracker 🔐
**Offensive Cybersecurity Internship Project**

This project demonstrates a brute-force and wordlist-based approach to decrypting password-protected PDF files using Python.  
It was developed as part of an **offensive security internship project** to showcase skills in:
- Cryptography & password auditing
- Multithreading with `ThreadPoolExecutor`
- Progress tracking with `tqdm`
- Secure coding practices in Python

⚠️ **Disclaimer**: This tool is for **educational and research purposes only**.  
Do not use it against files you do not own or have explicit permission to test.

---

## 🚀 Features
- Wordlist-based PDF password cracking
- On-the-fly password generation (charset + length range)
- Multithreaded execution for faster cracking
- Progress bar visualization with `tqdm`
- Jupyter Notebook demo for interactive exploration

---

## 📂 Project Structure
- `cracker.py` → CLI tool
- `notebook_demo.ipynb` → Jupyter demo
- `examples/` → Sample PDF + wordlist
- `docs/` → Architecture & ethical notes

---

## ⚙️ Installation
```bash
git clone https://github.com/ArsalnAhmd/pdf-cracker.git
cd pdf-cracker
pip install -r requirements.txt
