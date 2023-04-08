#!/usr/bin/env python3

#
# Process JLCPCB Fabrication Toolkit in Kicad 7.x to satisfy JLCBPCB assembly service input format
#

import sys, os, csv

#
# App
#
def main():
    if len(sys.argv) < 2:
        print("usage: {0} <production dir>".format(os.path.basename(sys.argv[0])))
        sys.exit(4)

    prod_dir = sys.argv[1]
    if not os.path.exists(prod_dir):
        print("{0}: production dir {1} does not exist".format(os.path.basename(sys.argv[0]), prod_dir))
        sys.exit(1)
    
    bom = os.path.join(prod_dir, "bom.csv")
    positions = os.path.join(prod_dir, "positions.csv")
    if not os.path.exists(bom):
        print("{0}: bom file {1} does not exist".format(os.path.basename(sys.argv[0]), bom))
        sys.exit(2)
    if not os.path.exists(positions):
        print("{0}: positions file {1} does not exist".format(os.path.basename(sys.argv[0]), positions))
        sys.exit(3)
    
    process_bom(bom)
    process_positions(positions)

def process_bom(input):
    """Designator,Footprint,Quantity,Value,LCSC Part #
    
    =>
    
    Comment/Value,Designator,Footprint,Part#"""
    
    IN_DESIGNATOR=0
    IN_FOOTPRINT=1
    IN_VALUE=3
    IN_PART=4

    print("processing BOM {}...".format(input), end='')

    header_read = False
    output = []
    with open(input) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if not header_read:
                if row[0] == "Comment" and row[1] == "Designator" and row[2] == "Footprint":
                    print("already processed, stopping.")
                    return
                header_read = True
                output.append(["Comment", "Designator", "Footprint", "JLCPCB Part #"])
                continue
                
            output.append([row[IN_VALUE], row[IN_DESIGNATOR], row[IN_FOOTPRINT], row[IN_PART]])

    with open(input, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for row in output:
            writer.writerow(row)

    print("done, stored to same file")

def process_positions(input):
    """Designator,Mid X,Mid Y,Rotation,Layer

    =>

    Designator,Mid X,Mid Y,Layer,Rotation"""
    
    IN_DESIGNATOR=0
    IN_MIDX=1
    IN_MIDY=2
    IN_ROTATION=3
    IN_LAYER=4

    print("processing CPL {}...".format(input), end='')

    header_read = False
    output = []
    with open(input) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if not header_read:
                if row[0] == "Designator" and row[1] == "Mid X" and row[2] == "Mid Y" and row[3] == "Layer":
                    print("already processed, stopping.")
                    return
                header_read = True
                output.append(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])
                continue
                
            output.append([row[IN_DESIGNATOR], row[IN_MIDX], row[IN_MIDY], row[IN_LAYER], row[IN_ROTATION]])

    with open(input, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        for row in output:
            writer.writerow(row)

    print("done, stored to same file")

if __name__ == '__main__':
    main()


