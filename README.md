# 📡 Digital Radio Modem — Educational Lab

This project demonstrates how a modem works at the most fundamental level.

Modem = MOdulator + DEModulator.

Computers do not transmit letters.
They transmit 0s and 1s.

We convert:
0 → 1200 Hz tone  
1 → 2200 Hz tone  

A radio transmits sound.
Another computer listens to the sound and detects the frequency.

That is digital communication.

---

## 📂 Project Structure

modem_tx.py — Transmitter  
modem_rx.py — Receiver  
requirements.txt — Dependencies  

---

## 🚀 Setup

### 1. Create virtual environment

python -m venv venv

Activate:

Windows:
venv\Scripts\activate

Linux / macOS:
source venv/bin/activate

---

### 2. Install dependencies

pip install -r requirements.txt

---

## ▶ Running the Demo

### Step 1 — Start receiver

python modem_rx.py

### Step 2 — Start transmitter (on another computer)

python modem_tx.py

---

## 🔎 What You Will See

The receiver shows two lines:

PHY: Physical layer (detected frequencies)
BIT: Logical layer (decoded bits)

Example:

PHY: |++++|----|++++|----
BIT:   1    0    1    0

If synchronization fails:

PHY: |..++|++--|--++|....
BIT:   .    1    0    .

---

## 🧠 Concepts You Learn

- Bits
- Symbols
- Frequency Shift Keying (FSK)
- FFT (Fast Fourier Transform)
- Preamble detection
- Physical vs Logical layers

---

## 🔬 Experiments

Try:

- Lowering volume
- Moving radios apart
- Introducing noise
- Increasing BIT_DURATION

Observe how errors appear.

---

You just built your own digital modem.