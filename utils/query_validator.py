import sqlparse

def validate_query(sql):
    """Basic SQL query validation"""
    try:
        parsed = sqlparse.parse(sql)
        if not parsed:
            return False
        return True
    except Exception:
        return False