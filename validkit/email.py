"""E-mail address validation."""

import re

from validkit._common import require_max_length

# Pragmatic syntactic check for an e-mail address: a local part made of the
# characters commonly allowed before an ``@``, followed by a dot-separated
# domain whose labels each start and end with an alphanumeric character. This
# is pure standard-library validation with no DNS or SMTP lookup; it rejects
# addresses that are obviously malformed and returns False instead of raising.
_EMAIL_RE = re.compile(
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
)


def is_valid_email(text: str) -> bool:
    """Return True when ``text`` is a syntactically valid e-mail address.

    The check is purely syntactic (standard-library ``re`` only, no network): a
    non-empty local part followed by ``@`` and a dot-separated domain. Obviously
    malformed input (missing ``@``, an empty local part or domain, ``not-an-email``)
    returns False rather than raising. Inputs longer than the documented maximum
    raise ``ValueError``.
    """
    require_max_length(text)
    if not text:
        return False
    return _EMAIL_RE.fullmatch(text) is not None
