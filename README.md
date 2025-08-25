# PDF Generator with PoC OpenAction

Este proyecto permite generar archivos PDF de prueba con contenido aleatorio, ajustados a un tamaño específico en MB. Además, soporta la inclusión de un PoC (Proof of Concept) mediante un OpenAction que abre un endpoint externo al abrir el PDF.  

Es útil para pruebas de **file upload**, **file scanners** y simulaciones controladas de interacción con servicios externos.

---

## Características

- Genera PDFs de tamaño exacto (aproximado) en MB.  
- Contenido aleatorio tipo lorem ipsum para pruebas.  
- Soporte de prefijo, sufijo e iterador en nombres de archivo.  
- Modo verbose para seguimiento del proceso.  
- Inclusión opcional de PoC mediante OpenAction en la última página.  
- Cálculo dinámico del tamaño promedio por página para minimizar padding innecesario.  
- Compatible con Python 3 y `reportlab` + `pikepdf`.

---

## Requisitos

- Python 3.10 o superior
- Librerías Python:

```bash
pip install -r requirements.txt
````

---

## Uso

```bash
python genpdf.py -s 1,5,10 -px PREFIX_ -sx SUFFIX -i d -v --poc --eu https://<endpoint-url>
```

### Argumentos

* `-s, --size`
  Tamaños en MB de los PDFs a generar, separados por coma (ej: `1,5,10`).

* `-px, --prefix`
  Prefijo para el nombre del archivo (por defecto `test`).

* `-sx, --suffix`
  Sufijo para el nombre del archivo (por defecto vacío).

* `-i, --iterator`
  Tipo de iterador para múltiples archivos:

  * `d` → dígitos (`1, 2, 3...`)
  * `a` → letras (`a, b, c...`)

* `-v, --verbose`
  Muestra información del progreso y tamaño de cada PDF.

* `--poc`
  Habilita la inclusión del PoC (última página con huella y OpenAction).

* `--eu, --endpoint-url`
  Endpoint URL a usar en el OpenAction (HTTPS).

---

## Consideraciones

* El PDF generado es seguro para pruebas internas; el PoC solo abre un enlace HTTP/HTTPS cuando se abre la última página.
* Ajusta `draw_page()` si deseas personalizar el contenido de las páginas.

---

## Licencia

Este proyecto está bajo la **Licencia MIT**, lo que garantiza que seguirá siendo open source y libre para su uso, modificación y distribución.

---

### `requirements.txt`

```

reportlab>=3.6.12
pikepdf>=8.5.1

````

> Se incluyen versiones recientes para compatibilidad con Python 3.10+.

---

### `LICENSE` (MIT)

```text
MIT License

Copyright (c) 2025 Tracel3ss

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````
