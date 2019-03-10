import argparse
import glob
import os
import xml.etree.ElementTree as ET

import mysql.connector


def monotabular(path, concept_name):
    tree = ET.parse(path)
    root = tree.getroot()
    section = root

    table_name = section.tag
    print("Populating table " + concept_name + "$" + table_name.lower())
    for entry in section:
        columns = []
        values = []
        for field in entry:
            columns.append(field.tag)
            values.append(field.text)
        clmn = ', '.join(["`{}`".format(value) for value in columns])
        sql = "INSERT INTO `{}` ({}) VALUES ({})".format(concept_name + "$" + table_name, clmn,
                                                         ','.join(['%s'] * len(columns)))
        cursor.execute(sql, values)


def polytabular(path, concept_name):
    tree = ET.parse(path)
    root = tree.getroot()
    for section in root:
        table_name = section.tag
        print("Populating table " + table_name)
        for entry in section:
            columns = []
            values = []
            for field in entry:
                columns.append(field.tag)
                values.append(field.text)
            clmn = ', '.join(["`{}`".format(value) for value in columns])
            sql = "INSERT INTO `{}` ({}) VALUES ({})".format(concept_name + "$" + table_name, clmn,
                                                             ','.join(['%s'] * len(columns)))
            cursor.execute(sql, values)


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=str, required=True,
                    help='directory containing the unzipped nhsbsa_dmd... folders')
parser.add_argument('-u', '--username', type=str, required=True,
                    help='username of your mysql database')
parser.add_argument('-p', '--password', type=str, required=True,
                    help='password of the mysql database corresponding to the username')
args = parser.parse_args()

rootpath = args.directory
username = args.username
password = args.password

cnx = mysql.connector.connect(user=username, password=password, database='sys')
cursor = cnx.cursor()

table_structure_path = os.path.dirname(os.path.realpath(__file__)) + '\\dmd_structure.sql'

concepts = [("f_lookup2_3{}.xml", "lookup", polytabular),
            ("f_ingredient2_3{}.xml", "ingredient", monotabular),
            ("f_vtm2_3{}.xml", "vtm", monotabular),
            ("f_vmp2_3{}.xml", "vmp", polytabular),
            ("f_amp2_3{}.xml", "amp", polytabular),
            ("f_vmpp2_3{}.xml", "vmpp", polytabular),
            ("f_ampp2_3{}.xml", "ampp", polytabular)]

os.chdir(rootpath)
dmddirs = glob.glob("nhsbsa_dmd_*_*")
if len(dmddirs) == 0:
    raise Exception("No dm+d directories in the path given")
for dmddir in dmddirs:
    if not os.path.isdir(dmddir):  # we don't want to match zip
        print("Skipping " + dmddir)
        continue

    schema_name = dmddir[7:-6].replace('.', '-')  # no '.' in schema name so we don't have to use back ticks
    print("Creating schema " + schema_name)
    cursor.execute(
        'CREATE DATABASE  IF NOT EXISTS `{}` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;'.format(
            schema_name))
    cursor.execute('USE `{}`;'.format(schema_name))

    print("Importing table structure")
    for line in open(table_structure_path):
        cursor.execute(line)

    print("Parsing xml...")
    os.chdir(dmddir)
    for con in concepts:
        filename = glob.glob(con[0].format("*"))[0]
        print("Parsing concept " + con[1])
        con[2](filename, con[1])
    os.chdir(rootpath)

    cnx.commit()
    print("Done")

cursor.close()
cnx.close()
