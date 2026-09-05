# validkit

Eine kleine, eigenständige Python-Bibliothek mit neun reinen Prüf- und
Normalisierungsfunktionen für alltägliche Eingabedaten: E-Mail-Adressen,
Kreditkarten-Prüfziffern (Luhn), IBANs, ISBN-13, Telefonnummern, Diakritika,
Secrets, Slugs und numerische Werte. Jede Funktion ist sauber typannotiert,
einzeln nutzbar, meldet ungültige Eingaben mit aussagekräftigen Fehlern und
lehnt überlange Eingaben frühzeitig mit einem `ValueError` ab, um
Ressourcenerschöpfung und ReDoS zu verhindern.

## Tech-Stack

- **Sprache**: Python (nur Standardbibliothek)
- **Python-Version**: `>= 3.9`
- **Tests**: pytest
- **Abhängigkeiten**: keine (nur Standardbibliothek)

## Installation

```bash
pip install -e .
```

Für Entwicklung und Tests zusätzlich die optionale Dev-Abhängigkeit:

```bash
pip install -e ".[dev]"
```

## Nutzung

Alle neun Funktionen sind über `from validkit import <name>` erreichbar:

```python
from validkit import is_valid_email, clamp, slugify
```

Jede String-Eingabe wird vor der eigentlichen Prüfung auf eine dokumentierte
Maximallänge (10 000 Zeichen) begrenzt; darüber hinaus wird ein `ValueError`
geworfen, der den übergebenen Wert selbst nicht preisgibt.

## Beispiele

Jede der neun öffentlichen Funktionen mit einem kurzen Beispiel:

| Funktion | Aufruf | Erwartetes Ergebnis |
| --- | --- | --- |
| `is_valid_email` | `is_valid_email("test@example.com")` | `True` |
| `luhn_check` | `luhn_check("4111111111111111")` | `True` |
| `is_valid_iban` | `is_valid_iban("DE89 3704 0044 0532 0130 00")` | `True` |
| `is_valid_isbn13` | `is_valid_isbn13("978-3-16-148410-0")` | `True` |
| `normalize_phone` | `normalize_phone("+49 170 1234567", "49")` | `"+491701234567"` |
| `strip_accents` | `strip_accents("Crème brûlée")` | `"Creme brulee"` |
| `mask_secret` | `mask_secret("geheim123", keep=3)` | `"******123"` |
| `slugify` | `slugify("Héllo Wörld!")` | `"hello-world"` |
| `clamp` | `clamp(5, 1, 10)` | `5` |

## Funktionen

- **`is_valid_email(text: str) -> bool`** – prüft, ob `text` eine gültige
  E-Mail-Adresse ist.
- **`luhn_check(digits: str) -> bool`** – prüft die Luhn-Prüfziffer einer
  Ziffernfolge; Nicht-Ziffern lösen einen `ValueError` aus.
- **`is_valid_iban(text: str) -> bool`** – prüft eine IBAN per Modulo-97
  (toleriert Leerzeichen und Kleinschreibung).
- **`is_valid_isbn13(text: str) -> bool`** – prüft eine ISBN-13 inklusive
  Prüfziffer.
- **`normalize_phone(text: str, country_code: Union[str, int]) -> str`** –
  normalisiert eine Telefonnummer nach E.164 (`+CC<Teilnehmerziffern>`).
- **`strip_accents(text: str) -> str`** – entfernt Diakritika (Akzente).
- **`mask_secret(text: str, keep: int = 4) -> str`** – maskiert alle Zeichen
  außer den letzten `keep`.
- **`slugify(text: str) -> str`** – erzeugt einen URL-freundlichen Slug.
- **`clamp(value, low, high) -> Union[int, float]`** – begrenzt `value` auf das
  Intervall `[low, high]`; `low > high` löst einen Fehler aus.
