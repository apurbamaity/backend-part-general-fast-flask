from sqlalchemy import text

# Define raw SQL templates using named placeholders
INSERT_INTO_TEMPLATE = """
INSERT INTO {table_name} ({columns})
VALUES ({placeholders})
"""
