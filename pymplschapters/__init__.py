#!/usr/bin/python3

import os
import argparse
import datetime
from . import MPLS
from lxml import etree

# --------------------------------
# Arguments
# --------------------------------
def main():
    ArgParser = argparse.ArgumentParser()
    ArgParser.add_argument(
        "-p", "--playlist", help="Input path to an MPLS playlist", required=True
    )
    ArgParser.add_argument(
        "-d",
        "--directory",
        help="Specify an output directory, by default it will save next to the playlist.",
        required=False
    )
    args = ArgParser.parse_args()

    def get_chapters(mpls):
        header, _ = MPLS.load_header(mpls)

        mpls.seek(header["PlayListStartAddress"], os.SEEK_SET)
        pl, _ = MPLS.load_PlayList(mpls)
        pl = pl["PlayItems"]

        mpls.seek(header["PlayListMarkStartAddress"], os.SEEK_SET)
        marks, _ = MPLS.load_PlayListMark(mpls)
        marks = marks["PlayListMarks"]

        for i, playItem in enumerate(pl):
            chapters = []
            playItemMarks = [
                x for x in marks if x["MarkType"] == 1 and x["RefToPlayItemID"] == i
            ]
            offset = playItemMarks[0]["MarkTimeStamp"]
            if playItem["INTime"] < offset:
                offset = playItem["INTime"]
            for n, mark in enumerate(playItemMarks):
                duration = ((mark["MarkTimeStamp"] - offset) / 45000) * 1000
                timespan = str(datetime.timedelta(milliseconds=duration))
                if timespan == "0:00:00":
                    timespan = f"{timespan}.000000"
                if timespan.startswith("0:"):
                    timespan = f"0{timespan}"
                chapters.append({
                    "clip": f"{playItem['ClipInformationFileName']}.{playItem['ClipCodecIdentifier'].lower()}",
                    "number": n + 1,
                    "duration": duration,
                    "timespan": timespan,
                })
            yield chapters

        return chapters

    with open(args.playlist, "rb") as playlist_handle:
        print("Processing file...")
        for file_with_chapter in get_chapters(playlist_handle):
            Chapters = etree.Element("Chapters")
            EditionEntry = etree.SubElement(Chapters, "EditionEntry")
            EditionFlagHidden = etree.SubElement(EditionEntry, "EditionFlagHidden")
            EditionFlagHidden.text = "0"
            EditionFlagDefault = etree.SubElement(EditionEntry, "EditionFlagDefault")
            EditionFlagDefault.text = "0"
            for chapter in file_with_chapter:
                ChapterAtom = etree.SubElement(EditionEntry, "ChapterAtom")
                ChapterDisplay = etree.SubElement(ChapterAtom, "ChapterDisplay")
                ChapterString = etree.SubElement(ChapterDisplay, "ChapterString")
                ChapterString.text = f"Chapter {str(chapter['number']).zfill(2)}"
                ChapterLanguage = etree.SubElement(ChapterDisplay, "ChapterLanguage")
                ChapterLanguage.text = "eng"
                ChapterTimeStart = etree.SubElement(ChapterAtom, "ChapterTimeStart")
                ChapterTimeStart.text = chapter["timespan"]
                ChapterFlagHidden = etree.SubElement(ChapterAtom, "ChapterFlagHidden")
                ChapterFlagHidden.text = "0"
                ChapterFlagEnabled = etree.SubElement(ChapterAtom, "ChapterFlagEnabled")
                ChapterFlagEnabled.text = "1"
            clip = file_with_chapter[0]["clip"]
            with open(os.path.join(
                args.directory or os.path.dirname(args.playlist),
                f"{os.path.splitext(os.path.basename(args.playlist))[0]}_{clip.split('.')[0]}.xml"
            ), "wb") as f:
                f.write(
                    etree.tostring(
                        Chapters,
                        encoding="utf-8",
                        doctype='<!DOCTYPE Tags SYSTEM "matroskatags.dtd">',
                        xml_declaration=True,
                        pretty_print=True,
                    )
                )
            print("Extracted chapters for " + clip)
        print("Finished...")
