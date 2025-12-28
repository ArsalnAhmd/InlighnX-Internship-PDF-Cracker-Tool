#!/usr/bin/env python3
"""
PDF Password Cracker
Offensive Cybersecurity Internship Project

This tool attempts to decrypt password-protected PDF files using either:
- A wordlist (dictionary attack)
- On-the-fly password generation (brute force)

⚠️ Disclaimer:
This project is for EDUCATIONAL and RESEARCH purposes only.
Do not use against files you do not own or have explicit permission to test.
"""

import pikepdf
from tqdm import tqdm
import itertools
import string
from concurrent.futures import ThreadPoolExecutor
import argparse
import sys


def generate_passwords(chars, min_length, max_length):
    """Generate passwords from given charset and length range."""
    for length in range(min_length, max_length + 1):
        for password in itertools.product(chars, repeat=length):
            yield ''.join(password)


def load_passwords(wordlist_file):
    """Load passwords from a wordlist file."""
    try:
        with open(wordlist_file, 'r', encoding="utf-8") as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print(f"[-] Wordlist file not found: {wordlist_file}")
        sys.exit(1)


def try_password(pdf_file, password):
    """Try a single password on the PDF."""
    try:
        with pikepdf.open(pdf_file, password=password):
            print(f"[+] Password found: {password}")
            return password
    except pikepdf._core.PasswordError:
        return None
    except Exception as e:
        print(f"[-] Error while trying password '{password}': {e}")
        return None


def decrypt_pdf(pdf_file, passwords, total_passwords, max_workers=4):
    """Attempt to decrypt PDF using provided passwords."""
    with tqdm(total=total_passwords, desc="Decrypting PDF", unit="password") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_password = {executor.submit(try_password, pdf_file, pwd): pwd for pwd in passwords}

            for future in tqdm(future_to_password, total=total_passwords):
                if future.result():
                    return future.result()
                pbar.update(1)

    print("[-] Unable to decrypt PDF. Password not found.")
    return None


def main():
    parser = argparse.ArgumentParser(description="Decrypt a password-protected PDF file.")
    parser.add_argument("pdf_file", help="Path to the password-protected PDF file")
    parser.add_argument("--wordlist", help="Path to the password list file", default=None)
    parser.add_argument("--generate", action="store_true", help="Generate passwords on the fly")
    parser.add_argument("--min_length", type=int, help="Minimum length of passwords to generate", default=1)
    parser.add_argument("--max_length", type=int, help="Maximum length of passwords to generate", default=3)
    parser.add_argument("--charset", type=str, help="Characters to use for password generation",
                        default=string.ascii_letters + string.digits)
    parser.add_argument("--max_workers", type=int, help="Maximum number of parallel threads", default=4)

    args = parser.parse_args()

    if args.generate:
        passwords = generate_passwords(args.charset, args.min_length, args.max_length)
        total_passwords = sum(1 for _ in generate_passwords(args.charset, args.min_length, args.max_length))
    elif args.wordlist:
        passwords = load_passwords(args.wordlist)
        total_passwords = sum(1 for _ in load_passwords(args.wordlist))
    else:
        print("[-] Either --wordlist must be provided or --generate must be specified.")
        sys.exit(1)

    decrypted_password = decrypt_pdf(args.pdf_file, passwords, total_passwords, args.max_workers)

    if decrypted_password:
        print(f"[+] PDF decrypted successfully with password: {decrypted_password}")
    else:
        print("[-] Unable to decrypt PDF. Password not found.")


if __name__ == "__main__":
    main()
