import os
from argparse import ArgumentParser
from datetime import timedelta

from lxml import etree

from pymplschapters import MPLS


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-p", "--playlist",
                            help="Input path to an MPLS playlist", required=True)
    arg_parser.add_argument("-d", "--directory", required=False,
                            help="Specify an output directory, by default it will save next to the playlist.")
    args = arg_parser.parse_args()

    with open(args.playlist, "rb") as f:
        print("Processing file...")
        for file_with_chapter in get_chapters(f):
            chapters = etree.Element("Chapters")
            edition_entry = etree.SubElement(chapters, "EditionEntry")
            edition_flag_hidden = etree.SubElement(edition_entry, "EditionFlagHidden")
            edition_flag_hidden.text = "0"
            edition_flag_default = etree.SubElement(edition_entry, "EditionFlagDefault")
            edition_flag_default.text = "0"
            for chapter in file_with_chapter:
                chapter_atom = etree.SubElement(edition_entry, "ChapterAtom")
                chapter_display = etree.SubElement(chapter_atom, "ChapterDisplay")
                chapter_string = etree.SubElement(chapter_display, "ChapterString")
                chapter_string.text = f"Chapter {str(chapter['number']).zfill(2)}"
                chapter_language = etree.SubElement(chapter_display, "ChapterLanguage")
                chapter_language.text = "eng"
                chapter_time_start = etree.SubElement(chapter_atom, "ChapterTimeStart")
                chapter_time_start.text = chapter["timespan"]
                chapter_flag_hidden = etree.SubElement(chapter_atom, "ChapterFlagHidden")
                chapter_flag_hidden.text = "0"
                chapter_flag_enabled = etree.SubElement(chapter_atom, "ChapterFlagEnabled")
                chapter_flag_enabled.text = "1"
            clip = file_with_chapter[0]["clip"]
            with open(os.path.join(
                args.directory or os.path.dirname(args.playlist),
                f"{os.path.splitext(os.path.basename(args.playlist))[0]}_{clip.split('.')[0]}.xml"
            ), "wb") as ff:
                ff.write(
                    etree.tostring(
                        chapters,
                        encoding="utf-8",
                        doctype='<!DOCTYPE Tags SYSTEM "matroskatags.dtd">',
                        xml_declaration=True,
                        pretty_print=True,
                    )
                )
            print("Extracted chapters for " + clip)
        print("Finished...")


def get_chapters(f):
    header, _ = MPLS.load_header(f)

    f.seek(header["PlayListStartAddress"], os.SEEK_SET)
    playlist, _ = MPLS.load_PlayList(f)

    f.seek(header["PlayListMarkStartAddress"], os.SEEK_SET)
    playlist_marks, _ = MPLS.load_PlayListMark(f)
    playlist_marks = playlist_marks["PlayListMarks"]

    for i, play_item in enumerate(playlist["PlayItems"]):
        play_item_marks = [
            x
            for x in playlist_marks
            if x["MarkType"] == 1 and x["RefToPlayItemID"] == i
        ]

        offset = play_item_marks[0]["MarkTimeStamp"]
        if play_item["INTime"] < offset:
            offset = play_item["INTime"]

        chapters = []
        for n, play_item_mark in enumerate(play_item_marks):
            duration = ((play_item_mark["MarkTimeStamp"] - offset) / 45000) * 1000
            timespan = str(timedelta(milliseconds=duration))
            if timespan.startswith("0:"):
                timespan = f"0{timespan}"
            if "." not in timespan:
                timespan = f"{timespan}.000000"
            chapters.append({
                "clip": f"{play_item['ClipInformationFileName']}.{play_item['ClipCodecIdentifier'].lower()}",
                "number": n + 1,
                "duration": duration,
                "timespan": timespan,
            })
        yield chapters
