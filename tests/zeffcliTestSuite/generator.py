#!/usr/bin/env python3
"""Zeff record config generator for HousePrice records."""
import sqlite3


def MockGenerator(url):
    """TBW:
    """
    conn = sqlite3.connect(url)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM properties")
    rows = cursor.fetchmany()
    while rows:
        for row in rows:
            yield row["id"]
        rows = cursor.fetchmany()


if __name__ == "__main__":
    for config in MockGenerator("./db.sqlite3"):
        print(config)
