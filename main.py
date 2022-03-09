# -*- coding: utf-8 -*-
# Example main.py
import argparse

import project0


def main(url):
    # Download data
    file_name = project0.fetchincidents(url)

    # Extract data
    incidents = project0.extractincidents(file_name)

    # Create new database
    db = project0.createdb()

    # Insert data
    project0.populatedb(db, incidents)

    # Print incident counts
    project0.status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)