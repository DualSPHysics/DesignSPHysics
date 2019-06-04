#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics XML Importer.

This script contains functionality useful for
unpacking an XML file from disk and process it as
a dictionary.

"""

import FreeCAD
import FreeCADGui
import Mesh
import json
import sys

from ds_modules import utils
from ds_modules import xmltodict

import xml.etree.ElementTree as ElementTree

"""
Copyright (C) 2019
EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo

This file is part of DesignSPHysics.

DesignSPHysics is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DesignSPHysics is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DesignSPHysics.  If not, see <http://www.gnu.org/licenses/>.
"""


def import_xml_file(filename):
    """ Returns data dictionary with values found
        in a GenCase/DSPH compatible XML file and a
       list of objects to add to simulation """

    with open(filename, "rb") as target_file:
        target_xml = target_file.read().replace('\n', '')

    # Path to xml folder
    path = "/".join(filename.split("/")[0:-1])

    # Converts XML in python dictionary
    raw_data = json.loads(json.dumps(xmltodict.parse(target_xml)))

    try:
        config = filter_data(raw_data)
    except:
        config = dict()

    objects = create_fc_objects(target_xml, path)

    return config, objects


def filter_data(raw):
    """ Filters a raw json representing an XML file to
        a compatible data dictionary. """

    fil = dict()

    # Case constants related code
    fil['lattice_bound'] = int(raw['case']['casedef']['constantsdef']['lattice']['@bound'])
    fil['lattice_fluid'] = int(raw['case']['casedef']['constantsdef']['lattice']['@fluid'])
    fil['gravity'] = [float(raw['case']['casedef']['constantsdef']['gravity']['@x']),
                      float(raw['case']['casedef']['constantsdef']['gravity']['@y']),
                      float(raw['case']['casedef']['constantsdef']['gravity']['@z'])]
    fil['rhop0'] = float(raw['case']['casedef']['constantsdef']['rhop0']['@value'])
    fil['hswl'] = float(raw['case']['casedef']['constantsdef']['hswl']['@value'])
    fil['hswl_auto'] = raw['case']['casedef']['constantsdef']['hswl']['@auto'].lower() == "true"
    fil['gamma'] = float(raw['case']['casedef']['constantsdef']['gamma']['@value'])
    fil['speedsystem'] = float(raw['case']['casedef']['constantsdef']['speedsystem']['@value'])
    fil['speedsystem_auto'] = raw['case']['casedef']['constantsdef']['speedsystem']['@auto'].lower() == "true"
    fil['coefsound'] = float(raw['case']['casedef']['constantsdef']['coefsound']['@value'])
    fil['speedsound'] = float(raw['case']['casedef']['constantsdef']['speedsound']['@value'])
    fil['speedsound_auto'] = raw['case']['casedef']['constantsdef']['speedsound']['@auto'].lower() == "true"
    fil['coefh'] = float(raw['case']['casedef']['constantsdef']['coefh']['@value'])
    fil['cflnumber'] = float(raw['case']['casedef']['constantsdef']['cflnumber']['@value'])
    fil['h'] = float(raw['case']['casedef']['constantsdef']['h']['@value'])
    fil['h_auto'] = raw['case']['casedef']['constantsdef']['h']['@auto'].lower() == "true"
    fil['b'] = float(raw['case']['casedef']['constantsdef']['b']['@value'])
    fil['b_auto'] = raw['case']['casedef']['constantsdef']['b']['@auto'].lower() == "true"
    fil['massbound'] = float(raw['case']['casedef']['constantsdef']['massbound']['@value'])
    fil['massbound_auto'] = raw['case']['casedef']['constantsdef']['massbound']['@auto'].lower() == "true"
    fil['massfluid'] = float(raw['case']['casedef']['constantsdef']['massfluid']['@value'])
    fil['massfluid_auto'] = raw['case']['casedef']['constantsdef']['massbound']['@auto'].lower() == "true"

    # Getting dp
    fil['dp'] = float(raw['case']['casedef']['geometry']['definition']['@dp'])

    # Getting case limits
    fil['limits_min'] = [float(raw['case']['casedef']['geometry']['definition']['pointmin']['@x']),
                         float(raw['case']['casedef']['geometry']['definition']['pointmin']['@y']),
                         float(raw['case']['casedef']['geometry']['definition']['pointmin']['@z'])]
    fil['limits_max'] = [float(raw['case']['casedef']['geometry']['definition']['pointmax']['@x']),
                         float(raw['case']['casedef']['geometry']['definition']['pointmax']['@y']),
                         float(raw['case']['casedef']['geometry']['definition']['pointmax']['@z'])]

    # Execution parameters related code
    execution_parameters = raw['case']['execution']['parameters']['parameter']
    for parameter in execution_parameters:
        if '#' in parameter['@key']:
            fil[parameter['@key'].replace('#', '').lower()] = float(parameter['@value'])
            fil[parameter['@key'].replace('#', '').lower() + "_auto"] = True
        else:
            fil[parameter['@key'].lower()] = float(parameter['@value'])

    # Finding used mkfluids and mkbounds
    fil['mkboundused'] = []
    fil['mkfluidused'] = []
    try:
        mkbounds = raw['case']['casedef']['geometry']['commands']['mainlist']['setmkbound']
        if isinstance(mkbounds, dict):
            # Only one mkfluid statement
            fil['mkboundused'].append(int(mkbounds['@mk']))
        else:
            # Multiple mkfluids
            for setmkbound in mkbounds:
                fil['mkboundused'].append(int(setmkbound['@mk']))
    except KeyError:
        # No mkbounds found
        pass
    try:
        mkfluids = raw['case']['casedef']['geometry']['commands']['mainlist']['setmkfluid']
        if isinstance(mkfluids, dict):
            # Only one mkfluid statement
            fil['mkfluidused'].append(int(mkfluids['@mk']))
        else:
            # Multiple mkfluids
            for setmkfluid in mkfluids:
                fil['mkfluidused'].append(int(setmkfluid['@mk']))
    except KeyError:
        # No mkfluids found
        pass

    return fil


def create_fc_objects(f, path):
    """ Creates supported objects on scene. Iterates over
        <mainlist> items and tries to recreate the commands in
        the current opened scene. """
    movement = (0.0, 0.0, 0.0)
    rotation = (0.0, 0.0, 0.0, 0.0)
    mk = ("void", "0")
    drawmode = "full"
    elementnum = 0
    to_add_dsph = dict()

    root = ElementTree.fromstring(f)
    mainlist = root.findall("./casedef/geometry/commands/mainlist/*")
    for command in mainlist:
        if command.tag == "matrixreset":
            movement = (0.0, 0.0, 0.0)
            rotation = (0.0, 0.0, 0.0, 0.0)
            pass
        elif command.tag == "setmkfluid":
            mk = ("fluid", command.attrib["mk"])
            pass
        elif command.tag == "setmkbound":
            mk = ("bound", command.attrib["mk"])
            pass
        elif command.tag == "setdrawmode":
            drawmode = command.attrib["mode"]
        elif command.tag == "move":
            movement = (float(command.attrib["x"]), float(command.attrib["y"]), float(command.attrib["z"]))
        elif command.tag == "rotate":
            rotation = (float(command.attrib["ang"]), float(command.attrib["x"]), float(command.attrib["y"]),
                        float(command.attrib["z"]))
        elif command.tag == "drawbox":
            for subcommand in command:
                point = (0.0, 0.0, 0.0)
                size = (1.0, 1.0, 1.0)
                if subcommand.tag == "boxfill":
                    pass
                elif subcommand.tag == "point":
                    point = (
                        float(subcommand.attrib["x"]), float(subcommand.attrib["y"]), float(subcommand.attrib["z"]))
                elif subcommand.tag == "size":
                    size = (float(subcommand.attrib["x"]), float(subcommand.attrib["y"]), float(subcommand.attrib["z"]))
                else:
                    utils.warning(
                        "Modifier unknown (" + subcommand.tag + ") for the command: " + command.tag + ". Ignoring...")
            # Box creation in FreeCAD
            FreeCAD.ActiveDocument.addObject("Part::Box", "Box" + str(elementnum))
            FreeCAD.ActiveDocument.ActiveObject.Label = "Box" + str(elementnum)
            # noinspection PyArgumentList
            FreeCAD.ActiveDocument.getObject("Box" + str(elementnum)).Placement = FreeCAD.Placement(
                FreeCAD.Vector((point[0] + movement[0]) * 1000, (point[1] + movement[1]) * 1000,
                               (point[2] + movement[2]) * 1000),
                FreeCAD.Rotation(FreeCAD.Vector(rotation[1], rotation[2], rotation[3]), rotation[0]))
            FreeCAD.ActiveDocument.getObject("Box" + str(elementnum)).Length = str(size[0]) + ' m'
            FreeCAD.ActiveDocument.getObject("Box" + str(elementnum)).Width = str(size[1]) + ' m'
            FreeCAD.ActiveDocument.getObject("Box" + str(elementnum)).Height = str(size[2]) + ' m'
            # Suscribe Box for creation in DSPH Objects
            # Structure: [name] = [mknumber, type, fill]
            to_add_dsph["Box" + str(elementnum)] = [int(mk[1]), mk[0], drawmode]
        elif command.tag == "drawcylinder":
            point = [0, 0, 0]
            top_point = [0, 0, 0]
            radius = float(command.attrib["radius"])
            points_found = 0
            for subcommand in command:
                if subcommand.tag == "point":
                    if points_found == 0:
                        point = [float(subcommand.attrib["x"]), float(subcommand.attrib["y"]),
                                 float(subcommand.attrib["z"])]
                    elif points_found == 1:
                        top_point = [float(subcommand.attrib["x"]), float(subcommand.attrib["y"]),
                                     float(subcommand.attrib["z"])]
                    else:
                        utils.warning("Found more than two points in a cylinder definition. Ignoring")
                    points_found += 1

            # Cylinder creation in FreeCAD
            FreeCAD.ActiveDocument.addObject("Part::Cylinder", "Cylinder" + str(elementnum))
            FreeCAD.ActiveDocument.ActiveObject.Label = "Cylinder" + str(elementnum)
            # noinspection PyArgumentList
            FreeCAD.ActiveDocument.getObject("Cylinder" + str(elementnum)).Placement = FreeCAD.Placement(
                FreeCAD.Vector((point[0] + movement[0]) * 1000, (point[1] + movement[1]) * 1000,
                               (point[2] + movement[2]) * 1000),
                FreeCAD.Rotation(FreeCAD.Vector(rotation[1], rotation[2], rotation[3]), rotation[0]))
            FreeCAD.ActiveDocument.getObject("Cylinder" + str(elementnum)).Radius = str(radius) + ' m'
            FreeCAD.ActiveDocument.getObject("Cylinder" + str(elementnum)).Height = (top_point[2] - point[2]) * 1000
            # Suscribe Cylinder for creation in DSPH Objects
            # Structure: [name] = [mknumber, type, fill]
            to_add_dsph["Cylinder" + str(elementnum)] = [int(mk[1]), mk[0], drawmode]
        elif command.tag == "drawsphere":
            point = [0, 0, 0]
            radius = float(command.attrib["radius"])
            for subcommand in command:
                if subcommand.tag == "point":
                    point = [float(subcommand.attrib["x"]), float(subcommand.attrib["y"]),
                             float(subcommand.attrib["z"])]
            # Sphere creation in FreeCAD
            FreeCAD.ActiveDocument.addObject("Part::Sphere", "Sphere" + str(elementnum))
            FreeCAD.ActiveDocument.ActiveObject.Label = "Sphere" + str(elementnum)
            # noinspection PyArgumentList
            FreeCAD.ActiveDocument.getObject("Sphere" + str(elementnum)).Placement = FreeCAD.Placement(
                FreeCAD.Vector((point[0] + movement[0]) * 1000, (point[1] + movement[1]) * 1000,
                               (point[2] + movement[2]) * 1000),
                FreeCAD.Rotation(FreeCAD.Vector(rotation[1], rotation[2], rotation[3]), rotation[0]))
            FreeCAD.ActiveDocument.getObject("Sphere" + str(elementnum)).Radius = str(radius) + ' m'
            # Suscribe Sphere for creation in DSPH Objects
            # Structure: [name] = [mknumber, type, fill]
            to_add_dsph["Sphere" + str(elementnum)] = [int(mk[1]), mk[0], drawmode]
        elif command.tag == "drawfilestl":
            # Imports the stl file as good as it can
            stl_path = path + "/" + command.attrib["file"]
            Mesh.insert(stl_path, "DSPH_Case")
            # toAddDSPH["STL" + str(elementnum)] = [int(mk[1]), mk[0], drawmode]
            pass
        else:
            # Command not supported, report and ignore
            utils.warning("The command: " + command.tag + " is not yet supported. Ignoring...")

        elementnum += 1

    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return to_add_dsph
