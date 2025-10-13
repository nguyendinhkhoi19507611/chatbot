"""
Utilities for converting numpy and other non-JSON-serializable types
to native Python types so they can be safely stored in MongoDB or
returned as JSON responses.
"""

from datetime import datetime, date

try:
    import numpy as _np  # optional; used for type checks
except Exception:  # pragma: no cover
    _np = None


def to_native_types(value):
    """Recursively convert values to native Python types.

    - numpy.integer -> int
    - numpy.floating -> float
    - numpy.ndarray -> list
    - datetime/date left as-is
    - dict/list/tuple/set are processed recursively
    """
    # Basic primitives
    if value is None or isinstance(value, (str, bool, int, float, datetime, date)):
        return value

    # numpy scalars and arrays
    if _np is not None:
        if isinstance(value, _np.integer):
            return int(value)
        if isinstance(value, _np.floating):
            return float(value)
        if isinstance(value, _np.ndarray):
            return [to_native_types(v) for v in value.tolist()]

    # Mappings
    if isinstance(value, dict):
        return {str(k): to_native_types(v) for k, v in value.items()}

    # Iterables
    if isinstance(value, (list, tuple, set)):
        return [to_native_types(v) for v in value]

    # Fallback to string representation
    try:
        return str(value)
    except Exception:
        return value


