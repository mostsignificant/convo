"""
Converts CSV, JSON or XML files to other formats via templates.
"""

import argparse
import csv
import json
import os
import xmltodict

from jinja2 import Environment, FileSystemLoader


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


def read_json(input_file: str):
    file = open(input_file)
    return json.load(file)


def read_xml(input_file: str):
    file = open(input_file)
    return xmltodict.parse(file.read)


def main():
    """
    Parse command line arguments, read CSV, JSON or XML from input file, transform via template and write to output.
    """
    parser = argparse.ArgumentParser(
        description='Converts input files to other formats via templates')
    parser.add_argument('input', type=str)
    parser.add_argument('template', type=str)
    parser.add_argument('output', type=str)

    args = parser.parse_args()

    _, extension = os.path.splitext(args.input)

    data = {}

    if extension == '.json':
        data = read_json(args.input)
    elif extension == '.csv':
        data = read_csv(args.input)
    elif extension == '.xml':
        data = read_xml(args.input)

    template_dir = os.path.dirname(os.path.abspath(args.template))
    environment = Environment(loader=FileSystemLoader(template_dir))

    template_file = os.path.basename(args.template)
    template = environment.get_template(template_file)

    content = template.render(data)

    with open(args.output, mode='w', encoding='utf-8') as document:
        document.write(content)


if __name__ == "__main__":
    main()
