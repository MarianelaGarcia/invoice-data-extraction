# Invoice Data Extraction Tool

## Overview

This project is a Python-based tool that extracts structured data from PDF invoices.

It supports both digital and scanned documents using OCR and is designed to work with multiple invoice formats.

---

## Features

* Extracts invoice number, total amount, and currency
* Supports scanned PDFs using OCR
* Handles multiple invoice formats
* Processes multiple files in batch
* Exports data to Excel, CSV, and JSON

---

## How it works

1. Reads all PDF files from the `Invoices` folder
2. Extracts text from each file (uses OCR when needed)
3. Parses relevant data using pattern matching
4. Saves structured results in the `Output` folder

---

## Project Structure

```
invoice-data-extraction/
│
├── main.py
├── requirements.txt
├── README.md
├── Invoices/
├── Output/
├── Image/
```

---

## How to run

```
pip install -r requirements.txt
python main.py
```

---

## Example Output

| file         | invoice | total | currency |
| ------------ | ------- | ----- | -------- |
| Invoice1.pdf | 01234   | 440   | $        |

---

## Demo

![Demo](Image/demo.png)

---

## Notes

* Works best with standard invoice layouts
* OCR accuracy depends on image quality
* The parser can be adapted to different invoice formats

---

## Use Cases

* Invoice processing automation
* Accounting workflows
* Data extraction pipelines
* Freelance automation projects

---

## Future Improvements

* API version (FastAPI)
* AI-based invoice parsing
* Web interface

---

## Author

Developed as a freelance-ready automation project.
