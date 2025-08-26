# PDF Generator with PoC OpenAction

This project generates test PDF files with random content, adjusted to a specific size in MB. It also supports including a PoC (Proof of Concept) via an OpenAction that opens an external endpoint when the PDF is opened.  

It is useful for testing **file uploads**, **file scanners**, and controlled simulations of interactions with external services.

---

## Features

- Generates PDFs of an exact (approximate) size in MB.  
- Random lorem ipsum–style content for testing.  
- Support for prefix, suffix, and iterator in file names.  
- Verbose mode to track the generation process.  
- Optional inclusion of a PoC via OpenAction on the last page.  
- Dynamic calculation of the average page size to minimize unnecessary padding.  
- Compatible with Python 3 and `reportlab` + `pikepdf`.

---

## Requirements

- Python 3.10 or higher
- Python libraries:

```bash
pip install -r requirements.txt
````

---

## Usage

```bash
python genpdf.py -s 1,5,10 -px PREFIX_ -sx SUFFIX -i d -v --poc --eu https://<endpoint-url>
```

### Arguments

* `-s, --size`
  PDF sizes in MB to generate, separated by commas (e.g., `1,5,10`).

* `-px, --prefix`
  Prefix for the file name (default: `test`).

* `-sx, --suffix`
  Suffix for the file name (default: empty).

* `-i, --iterator`
  Iterator type for multiple files:

  * `d` → digits (`1, 2, 3...`)
  * `a` → letters (`a, b, c...`)

* `-v, --verbose`
  Displays progress and file size information.

* `--poc`
  Enables PoC inclusion (last page with marker and OpenAction).

* `--eu, --endpoint-url`
  Endpoint URL to be used in the OpenAction (HTTPS).

---

## Notes

* The generated PDF is safe for internal testing; the PoC only triggers an HTTP/HTTPS request when the last page is opened.
* Adjust `draw_page()` if you want to customize the page content.
* Compatible with Burp Collaborator Endpoint

---

### `requirements.txt`

```
reportlab>=3.6.12
pikepdf>=8.5.1
```

> Recent versions are included for compatibility with Python 3.10+.

---

### `LICENSE` (MIT)

This project is licensed under the terms of the [LICENSE](./LICENSE) file.

