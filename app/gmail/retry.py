import json
import random
import time

from googleapiclient.errors import HttpError

RETRIABLE_STATUSES = {403, 429, 500, 502, 503, 504}
RETRIABLE_REASONS = {
    'backendError',
    'internalError',
    'rateLimitExceeded',
    'userRateLimitExceeded',
}
MAX_RETRIES = 6


def _extract_error_reasons(exc):
    try:
        payload = json.loads(exc.content.decode('utf-8'))
    except (AttributeError, UnicodeDecodeError, json.JSONDecodeError):
        return set()

    errors = payload.get('error', {}).get('errors', [])
    return {
        error.get('reason')
        for error in errors
        if error.get('reason')
    }


def _retry_after_seconds(exc):
    retry_after = getattr(exc.resp, 'get', lambda *args, **kwargs: None)('retry-after')
    if retry_after is None:
        return None

    try:
        return float(retry_after)
    except ValueError:
        return None


def _should_retry(exc):
    status = getattr(exc.resp, 'status', None)
    reasons = _extract_error_reasons(exc)

    if status == 403 and reasons and not (reasons & RETRIABLE_REASONS):
        return False

    return status in RETRIABLE_STATUSES


def execute_with_retry(action, *, description):
    for attempt in range(MAX_RETRIES + 1):
        try:
            return action()
        except HttpError as exc:
            if not _should_retry(exc) or attempt == MAX_RETRIES:
                raise

            retry_after = _retry_after_seconds(exc)
            if retry_after is None:
                retry_after = min(16, 2 ** attempt) + random.uniform(0, 0.5)

            print(
                f'{description} limitado por Gmail; '
                f'reintentando en {retry_after:.1f}s '
                f'(intento {attempt + 1}/{MAX_RETRIES})'
            )
            time.sleep(retry_after)
