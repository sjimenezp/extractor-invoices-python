import configparser
import logging
import os
import xml.etree.ElementTree as ET
from collections import namedtuple
from datetime import datetime

import pyperclip
from tabulate import tabulate

logging.basicConfig(filename='Invoice-XML-Extractor.log', filemode='w', level=logging.ERROR)


def credits():
    print(
        """

    #################################################
    #                                               #
    #   GitHub profile:                             #
    #   https://github.com/sjimenezp                #
    #                                               #
    #   Copyright © 2024                            #
    #                                               #
    #################################################
    """
    )


def title():
    print(
        """
    #################################################
    #                                               #
    #           Facturas XML a Portapapeles         #
    #                                               #
    #################################################
    """
    )


def guide():
    print(
        """
    Guía rápida para usar este script:

    1. Ingrese el directorio donde se encuentran las facturas cuando se le solicite.
    2. El script procesará todos los archivos XML en el directorio.
    3. Los datos se ordenarán por fecha y se imprimirán en la terminal.
    4. Si las facturas están organizadas en directorios, el nombre del directorio se
       agregará como el 'Tipo de Gasto'. Si no es así, por defecto se considerarán
       de tipo 'Gasolina'.
    5. Los datos también se copiarán al portapapeles para que pueda pegarlos en Excel.

    
    Nota: El directorio de trabajo se guardará en un archivo de configuración llamado 
    'config.ini' la primera vez que ejecute este script. Para cambiar el directorio 
    de trabajo en el futuro, deberá editar este archivo manualmente.

    Presione Enter para continuar...
    """
    )


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


WORKING_DIRECTORY_KEY = "working_directory"
DEFAULT_SECTION = "DEFAULT"
CONFIG_FILE = "config.ini"

WORKING_DIRECTORY_PROMPT = (
    "\nIngrese el directorio de trabajo (presione enter para usar el predeterminado): "
)
WORKING_DIRECTORY_SAVED_MESSAGE = "\nEl directorio de trabajo se ha guardado en el archivo de configuración 'config.ini'."
CHANGE_WORKING_DIRECTORY_MESSAGE = "Para cambiar el directorio de trabajo en el futuro, use la opción 'Cambiar directorio de trabajo' en el programa."


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def write_config(config):
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


def save_working_directory(config, working_directory):
    config[DEFAULT_SECTION] = {WORKING_DIRECTORY_KEY: working_directory}
    write_config(config)

    print(WORKING_DIRECTORY_SAVED_MESSAGE)
    print(CHANGE_WORKING_DIRECTORY_MESSAGE)


def get_working_directory(config):
    if DEFAULT_SECTION in config and WORKING_DIRECTORY_KEY in config[DEFAULT_SECTION]:
        return config[DEFAULT_SECTION][WORKING_DIRECTORY_KEY]
    else:
        working_directory = input(WORKING_DIRECTORY_PROMPT)
        if not working_directory:
            working_directory = os.getcwd()

        save_working_directory(config, working_directory)
        return working_directory


def set_working_directory(config, working_directory):
    if not os.path.isfile(CONFIG_FILE):
        save_working_directory(config, working_directory)


XML_NAMESPACE = "{http://www.sat.gob.mx/cfd/4}"
XML_TFD_NAMESPACE = "{http://www.sat.gob.mx/TimbreFiscalDigital}"
EMISOR_PATH = f"{XML_NAMESPACE}Emisor"
TFD_PATH = f".//{XML_TFD_NAMESPACE}TimbreFiscalDigital"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
DISPLAY_DATE_FORMAT = "%d/%m/%Y"

ParsedData = namedtuple("ParsedData", ["uuid", "fecha", "rfc", "nombre", "total"])


def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        fecha = datetime.strptime(root.get("Fecha"), DATE_FORMAT).strftime(
            DISPLAY_DATE_FORMAT
        )
        total = root.get("Total")
        emisor = root.find(EMISOR_PATH)
        nombre = emisor.get("Nombre")
        rfc = emisor.get("Rfc")

        tfd = root.find(TFD_PATH)
        uuid = tfd.get("UUID").split("-")[0]

        return uuid, fecha, rfc, nombre, total
    except (ET.ParseError, AttributeError, TypeError):
        logging.error(f"Error al leer el archivo: {file_path}")
        return ParsedData(None, None, None, None, None)


def sort_data(data):
    return sorted(data, key=lambda row: (row[4], row[1]), reverse=False)


def print_table(data):
    headers = ["UUID", "Fecha", "RFC", "Nombre", "Tipo de Gasto", "Total"]
    table = tabulate(data, headers, tablefmt="grid")
    print("\n")
    print(table)


def copy_to_clipboard(data):
    clipboard_data = [
        f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t\t\t\t{row[4]}\t\t\t{row[5]}"
        for row in data
    ]
    try:
        pyperclip.copy("\n".join(clipboard_data))
    except Exception as e:
        logging.error(f"Error al copiar al portapapeles: {e}")


def validate_directory(directory):
    if not os.path.exists(directory):
        print(f"El directorio {directory} no existe.")
        return False
    if not os.path.isdir(directory):
        print(f"{directory} no es un directorio.")
        return False
    return True


def process_files(working_dir):
    data = []
    for root, dirs, files in os.walk(working_dir):
        if root == working_dir and not dirs:
            folder_name = "Gasolina"
        else:
            folder_name = os.path.basename(root)
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                uuid, fecha, rfc, nombre, total = parse_xml(file_path)
                data.append([uuid, fecha, rfc, nombre, folder_name, total])
    return data


def main():
    working_dir = input("Folder de XML's (Enter para predeterminado): ")
    config = read_config()
    if not working_dir:
        working_dir = get_working_directory(config)
    else:
        if not validate_directory(working_dir):
            return
        set_working_directory(config, working_dir)

    data = process_files(working_dir)

    data = sort_data(data)
    print_table(data)
    copy_to_clipboard(data)


def start_application():
    title()
    guide()
    input()
    clear_terminal()


if __name__ == "__main__":
    try:
        start_application()
        main()
        credits()
    except Exception as e:
        logging.error(f"Se produjo un error inesperado: {e}")
    finally:
        input("\nPresione cualquier tecla para salir...")
