# 🛡️ 42 Cybersecurity Piscine

This repository contains my solutions and documentation for the **Cybersecurity Piscine** at 42. This intensive program covers a wide range of security topics, from web vulnerabilities and cryptography to malware analysis and network security.

## 🚀 Projects Overview

| Project | Category | Key Concepts | Link |
| :--- | :--- | :--- | :--- |
| **Arachnida** | Web & Metadata | Web scraping, EXIF data, Python | [View Project](../../tree/arachnida) |
| **ft_otp** | Auth / Crypto | TOTP (RFC 6238), HMAC, Key Security | [View Project](../../tree/ft_otp) |
| **ft_onion** | Networking | Tor Network, Hidden Services, Docker | [View Project](../../tree/ft_onion) |
| **Reverse me** | Reversing | Binary analysis, CTF challenges | [View Project](../../tree/reverse_me) |
| **Stockholm** | Malware | Wannacry mechanics, Encryption | [View Project](../../tree/stockholm) |
| **Inquisitor** | Networking | ARP Spoofing, Packet inspection | [View Project](../../tree/inquisitor) |
| **Vaccine** | Web Security | SQL Injection, XSS, Automation | [View Project](../../tree/vaccine) |

---

## 📂 Project Details

### [🕷️ Arachnida](../../tree/arachnida)
Development of two tools in Python:
* **Spider:** A web crawler to download images recursively from a URL.
* **Scorpion:** A tool to parse images and extract metadata (EXIF, IPTC, etc.).

### [🔐 ft_otp](../../tree/ft_otp)
Implementation of a **One-Time Password** generator.
* Generates 6-digit codes based on a master key.
* Compliant with Google Authenticator standards.
* Focuses on secure key storage and hashing algorithms.

### [🧅 ft_onion](../../tree/ft_onion)
Setting up a secure infrastructure using **Docker**.
* Configures an Nginx server accessible only via the **Tor network** (.onion).
* Implements SSH access and secure routing.

### [🦠 Stockholm](../../tree/stockholm)
A pedagogical project to understand how ransomware works.
* Recursively encrypts files in a specific directory using a secure algorithm.
* Includes a decryption tool (authentication required).
* **Warning:** For educational purposes only.

---

## 🛠️ Tools Used
* **Languages:** Python, C, Shell
* **Infrastructure:** Docker, Nginx, Tor
* **Security Tools:** Wireshark, Burp Suite, GDB/Ghidra

## 📖 How to use
Each folder contains its own `README` with specific instructions on how to run the scripts or compile the programs.

```bash
# Example: Running the OTP generator
cd ft_otp
python3 ft_otp.py -g secret.key
python3 ft_otp.py -k ft_otp.key
