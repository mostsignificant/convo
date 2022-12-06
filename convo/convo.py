"""
Converts JSON files to other formats via templates.
"""

import argparse
import csv
import json
import os

from jinja2 import Environment, FileSystemLoader


def read_json_file(input_file: str):
    file = open(input_file)
    return json.load(file)


def read_csv(input_file: str):
    reader = csv.reader(open(input_file, 'r'), delimiter=';')
    header = True

    data = {'items': []}
    keys = []

    for row in reader:
        if len(row) == 0:
            continue  # skip empty rows

        if header:
            for key in row:
                key = key.replace(' ', '')
                keys.append(key)
            header = False
            continue

        item = {}
        for i, value in enumerate(row):
            item[keys[i]] = value

        data['items'].append(item)

    return data


def main():
    """
    Parse command line arguments, read JSON from input file, transform via template and write to output file.
    """
    parser = argparse.ArgumentParser(
        description='Converts JSON files to other formats via templates')
    parser.add_argument('input', type=str)
    parser.add_argument('template', type=str)
    parser.add_argument('output', type=str)

    args = parser.parse_args()

    input_file = args.input
    _, input_fileext = os.path.splitext(input_file)

    data = {}

    if input_fileext == '.json':
        data = read_json(input_file)
    elif input_fileext == '.csv':
        data = read_csv(input_file)

    template_dir = os.path.dirname(os.path.abspath(args.template))
    environment = Environment(loader=FileSystemLoader(template_dir))

    template_file = os.path.basename(args.template)
    template = environment.get_template(template_file)

    content = template.render(data)

    with open(args.output, mode='w', encoding='utf-8') as document:
        document.write(content)


if __name__ == "__main__":
    main()
