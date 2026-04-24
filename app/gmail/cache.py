import threading
import time
import uuid

SCAN_TTL_SECONDS = 15 * 60

_lock = threading.Lock()
_scans = {}
_latest_scan_id = None


def _cleanup_expired(now):
    global _latest_scan_id

    expired_ids = [
        scan_id
        for scan_id, data in _scans.items()
        if data['expires_at'] <= now
    ]

    for scan_id in expired_ids:
        _scans.pop(scan_id, None)
        if _latest_scan_id == scan_id:
            _latest_scan_id = None


def _clone_senders(senders):
    return [
        {
            'sender': sender['sender'],
            'count': sender['count'],
            'ids': list(sender['ids']),
            'example_subject': sender['example_subject'],
        }
        for sender in senders
    ]


def save_scan(senders):
    global _latest_scan_id

    now = time.time()
    expires_at = now + SCAN_TTL_SECONDS
    scan_id = uuid.uuid4().hex

    with _lock:
        _cleanup_expired(now)
        _scans[scan_id] = {
            'senders': _clone_senders(senders),
            'expires_at': expires_at,
        }
        _latest_scan_id = scan_id

    return scan_id, expires_at


def get_scan(scan_id=None):
    now = time.time()

    with _lock:
        _cleanup_expired(now)

        resolved_scan_id = scan_id or _latest_scan_id
        if not resolved_scan_id:
            return None

        scan = _scans.get(resolved_scan_id)
        if not scan:
            return None

        return {
            'scan_id': resolved_scan_id,
            'senders': _clone_senders(scan['senders']),
            'expires_at': scan['expires_at'],
        }
