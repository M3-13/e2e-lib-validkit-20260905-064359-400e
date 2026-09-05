VERDICT: CHANGES_REQUESTED

## Security-Review

### Scanner-Interpretation
- `bandit` wurde nicht ausgeführt (`[skipped]`).
- `semgrep` wurde nicht ausgeführt (`[skipped]`).
- Das Fehlen von Scanner-Ergebnissen ist **kein** Beleg für Abwesenheit von Schwachstellen. Die folgende Bewertung beruht daher auf manueller Analyse des sichtbaren Produktcodes.

### Prüfbereiche

**Secrets**  
Keine hartkodierten Schlüssel, Passwörter, Token oder URLs sichtbar. Fehlermeldungen vermeiden die Rückgabe übergebener Eingabewerte. `mask_secret` entfernt Klartext wie spezifiziert.

**Injection / Eingaben**  
Keine Verwendung von `eval`, `exec`, `compile`, `pickle` oder `subprocess` sichtbar. Regex-Verarbeitung in `validkit/email.py` und `validkit/slug.py` ist bei der dokumentierten Maximallänge linear und bietet keine offensichtliche ReDoS-Fläche.

**AuthN/AuthZ**  
Nicht zutreffend; die Bibliothek ist eigenständig ohne Netzwerk, UI oder Dienste.

**Dependencies**  
Keine Laufzeitabhängigkeiten; nur Standardbibliothek. `pytest` als optionale Dev-Abhängigkeit, Bereich `<9`, kein bekanntes ausnutzbares CVE sichtbar.

**Konfiguration / Transport**  
Keine Netzwerk-, CORS-, Debug- oder Transportkonfiguration vorhanden.

---

## Findings

### 1. Medium — Fehlende Max-Length-Validierung für `country_code` in `normalize_phone`
**Betroffene Stelle:** `validkit/phone.py`, Funktionen `normalize_phone` und `_country_code_digits`

**Beschreibung:**  
`normalize_phone` ruft `require_max_length(text)` nur für den ersten Parameter auf. Der zweite Parameter `country_code` ist laut Signatur `Union[str, int]` und wird in `_country_code_digits` mit `str(country_code).strip()` verarbeitet. Eine überlange Zeichenkette oder sehr große Ganzzahl kann eine sehr große temporäre Zeichenkette erzeugen und anschließend mit `cc + cleaned` konkateniert werden. Das verletzt AC-12 („Alle öffentlichen Funktionen lehnen String-Eingaben oberhalb einer dokumentierten Maximallänge … vor der eigentlichen Prüfung ab“) und öffnet eine lokale Ressourcenerschöpfungsfläche.

**Konkreter Fix:**  
In `_country_code_digits` vor der Weiterverarbeitung prüfen:

```python
def _country_code_digits(country_code: Union[str, int]) -> str:
    if isinstance(country_code, str):
        require_max_length(country_code)
        cc = country_code.strip()
    else:
        cc = str(country_code)
        require_max_length(cc)

    if not cc:
        raise ValueError("country code is empty")
    if not cc.isdigit():
        raise ValueError("country code must contain only digits")
    return cc
```

Hinweis: Für sehr große `int`-Werte entsteht die große Zeichenkette zunächst bei `str(country_code)`. Für eine vollständige Härtung kann zusätzlich vor der Konversion eine Obergrenze für `int`-Werte gesetzt werden, z. B. über die Bit-Länge oder einen festen Maximalwert.

---

### 2. Low — `is_valid_iban` akzeptiert potenziell nicht-ASCII-alphanumerische Zeichen
**Betroffene Stelle:** `validkit/iban.py`, Funktion `is_valid_iban`

**Beschreibung:**  
Nach der Normalisierung wird `normalized.isalnum()` verwendet. `str.isalnum()` liefert auch für viele Unicode-Buchstaben `True`. `_mod_97` behandelt alle Nicht-Ziffern als `ord(char) - 55`. Der IBAN-Standard erlaubt jedoch nur ASCII-Buchstaben (`A–Z`) und Ziffern (`0–9`). Dadurch kann eine strukturell ungültige IBAN mit Unicode-Zeichen unter Umständen als gültig bewertet werden, falls die Prüfsummenrechnung zufällig `1` ergibt. Das ist primär eine Validierungsungenauigkeit, kann aber die Integrität einer IBAN-Prüfung schwächen.

**Konkreter Fix:**  
Nach der Normalisierung auf ASCII-Zeichen beschränken, z. B.:

```python
import re

_IBAN_RE = re.compile(r"[A-Z]{2}[0-9]{2}[A-Z0-9]+")

# in is_valid_iban:
normalized = text.replace(" ", "").upper()
if not _IBAN_RE.fullmatch(normalized):
    return False
```

Auf `_mod_97` kann dann weiterhin ASCII-sicher zugegriffen werden.

---

### 3. Low — `mask_secret` akzeptiert `bool` als `keep`
**Betroffene Stelle:** `validkit/secret.py`, Funktion `mask_secret`

**Beschreibung:**  
`isinstance(True, int)` ist in Python `True`. Dadurch akzeptiert `mask_secret("geheim123", True)` den Wert `keep=1`, obwohl die Dokumentation einen nicht-negativen Ganzzahlwert verlangt. Das ist kein unmittelbarer Angriffsvektor, aber eine Eingabevalidierungslücke, die zu unerwartetem Maskierungsverhalten führen kann.

**Konkreter Fix:**  
`bool` explizit ausschließen:

```python
if isinstance(keep, bool) or not isinstance(keep, int):
    raise ValueError("keep must be a non-negative integer")
if keep < 0:
    raise ValueError("keep must be a non-negative integer")
```

---

## Ergebnis

Es wurden keine kritischen oder hohen Schwachstellen gefunden. Die mittlere Schwachstelle in `normalize_phone` sollte vor Freigabe behoben werden, da sie die dokumentierte Ressourcenschutzgrenze AC-12 nicht vollständig umsetzt. Nach Behebung ist eine erneute Prüfung sinnvoll.