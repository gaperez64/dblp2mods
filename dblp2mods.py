#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as et


def header():
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
          "<modsCollection xmlns=\"http://www.loc.gov/mods/v3\">")


def footer():
    print("</mods></modsCollection>")


# Single pass: one read, and output on the fly
def trans(filename):
    tree = et.parse(filename)
    root = tree.getroot()
    # All pubs are r-tags, this gets us all pubs
    for pub in root.findall("r"):
        # Print all info from the pub, if it is not informal
        pubtype = pub[0]
        publtype = pubtype.get("publtype")
        if publtype is not None and publtype == "informal":
            continue
        print("<mods version=\"3.3\">")

        # Add the title
        print("<titleInfo><title>")
        print(pubtype.find("title").text)
        print("</title></titleInfo>")

        # Add the year of the pub
        print("<originInfo><dateIssued>")
        print(pubtype.find("year").text)
        print("</dateIssued></originInfo>")

        # Process all authors
        for author in pubtype.findall("author"):
            names = author.text.split()
            # Remove the last name if it is an ID from DBLP
            if names[-1].startswith("00"):
                names = names[:-1]
            print("<name type=\"personal\">")
            print("<namePart type=\"family\">")
            print(names[-1])
            print("</namePart><namePart type=\"given\">")
            print(" ".join(names[:-1]))
            print("</namePart></name>")

        # Add the type for FWO, some type-related things too
        pages = pubtype.find("pages").text.split("-")
        if len(pages) == 1:
            pages.append(pages[0])
        if pubtype.tag == "inproceedings":
            print("<extension type=\"pt\">"
                  "<pubtype src=\"vabb\">VABB-5</pubtype>"
                  "</extension>")
            print("<relatedItem type=\"host\"><titleInfo><title>")
            print(pubtype.find("booktitle").text)
            print("</title></titleInfo><part><extent unit=\"page\">")
            print("<start>" + pages[0] + "</start>")
            print("<end>" + pages[1] + "</end>")
            print("</extent></part></relatedItem>")
        else:
            assert pubtype.tag == "article"
            print("<extension type=\"pt\">"
                  "<pubtype src=\"vabb\">VABB-1</pubtype>"
                  "</extension>")
            print("<relatedItem type=\"host\"><titleInfo><title>")
            print(pubtype.find("journal").text)
            print("</title></titleInfo><part><extent unit=\"page\">")
            print("<start>" + pages[0] + "</start>")
            print("<end>" + pages[1] + "</end></extent>")
            print("<detail type=\"volume\"><number>")
            print(pubtype.find("volume").text + "</number></detail>")
            issue = pubtype.find("number")
            if issue is not None:
                print("<detail type=\"issue\"><number>")
                print(issue.text + "</number></detail>")
            print("</part></relatedItem>")
        print("</mods>")


# Preparing the arguments' parser and calling the transformation in case of
# this being the main script
parser = argparse.ArgumentParser(description='Translate a DBLP XML to MODS')
parser.add_argument('source', type=str, help='an integer for the accumulator')


if __name__ == "__main__":
    args = parser.parse_args()
    header()
    trans(args.source)
    footer()
    exit(0)
