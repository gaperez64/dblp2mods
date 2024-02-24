#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as et
from xml.sax.saxutils import escape


def header():
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
          "<modsCollection xmlns=\"http://www.loc.gov/mods/v3\">")


def footer():
    print("</modsCollection>")


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
        # Notes:
        # (1) DBLP adds a period at the end of the title
        # (2) The title is escaped in case it has &
        print("<titleInfo><title>", end="")
        print(escape(pubtype.find("title").text[:-1]), end="")
        print("</title></titleInfo>")

        # Add the year of the pub
        print("<originInfo><dateIssued>", end="")
        print(pubtype.find("year").text, end="")
        print("</dateIssued></originInfo>")

        # Process all authors
        for author in pubtype.findall("author"):
            # Note: we encode things in XML properly to avoid accent weirdness
            names = author.text.encode(encoding="ascii",
                                       errors="xmlcharrefreplace")
            names = names.decode("ascii")
            names = names.split()
            # Remove the last name if it is an ID from DBLP
            if names[-1].startswith("00"):
                names = names[:-1]
            print("<name type=\"personal\">")
            print("<namePart type=\"family\">", end="")
            print(names[-1], end="")
            print("</namePart><namePart type=\"given\">", end="")
            print(" ".join(names[:-1]), end="")
            print("</namePart></name>")

        # Add the type for FWO, some type-related things too
        pages = pubtype.find("pages")
        if pages is not None:
            pages = pages.text.split("-")
            if len(pages) == 1:
                pages.append(pages[0])
        if pubtype.tag == "inproceedings":  # C1
            print("<extension type=\"pt\">"
                  "<pubtype src=\"vabb\">VABB-5</pubtype>"
                  "</extension>")
            print("<relatedItem type=\"host\"><titleInfo><title>", end="")
            print(pubtype.find("booktitle").text, end="")
            print("</title></titleInfo>")
            if pages is not None:
                print("<part><extent unit=\"page\">")
                print("<start>" + pages[0] + "</start>")
                print("<end>" + pages[1] + "</end>")
                print("</extent></part>")
            print("</relatedItem>")
        else:
            assert pubtype.tag == "article"  # A1
            print("<extension type=\"pt\">"
                  "<pubtype src=\"vabb\">VABB-1</pubtype>"
                  "</extension>")
            # A1 requires a Web-of-Science extension, we'll fake one
            print("<extension type=\"wos\"><if year=\"", end="")
            print(pubtype.find("year").text, end="")
            # FIXME: the actual value is left empty, we don't really have
            # important impact factors in CS journals; AND, the DBLP XML does
            # not have this information
            print("\"></if></extension>")
            print("<relatedItem type=\"host\"><titleInfo><title>", end="")
            print(pubtype.find("journal").text, end="")
            print("</title></titleInfo><part><extent unit=\"page\">")
            print("<start>" + pages[0] + "</start>")
            print("<end>" + pages[1] + "</end></extent>")
            print("<detail type=\"volume\"><number>", end="")
            print(pubtype.find("volume").text + "</number></detail>")
            issue = pubtype.find("number")
            if issue is not None:
                print("<detail type=\"issue\"><number>", end="")
                print(issue.text, end="")
                print("</number></detail>")
            print("<date>" + pubtype.find("year").text + "</date>")
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
