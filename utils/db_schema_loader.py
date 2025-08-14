def load_schema(file_path):
    """Load database schema from a SQL file"""
    with open(file_path, 'r') as file:
        return file.read()