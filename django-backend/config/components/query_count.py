QUERYCOUNT = {
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 0,
    },
    'IGNORE_REQUEST_PATTERNS': [r'^/admin/'],
    'IGNORE_SQL_PATTERNS': [r'NO SCROLL CURSOR WITH'],
    'DISPLAY_DUPLICATES': 10,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count',
}
