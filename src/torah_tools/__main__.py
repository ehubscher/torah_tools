import json
import io
from pathlib import Path

ALEF_BEIS: str = "\u05D0 \u05D1 \u05D2 \u05D3 \u05D4 \u05D5 \u05D6 \u05D7 \u05D8 \u05D9 \u05DA \u05DB \u05DC \u05DD \u05DE \u05DF \u05E0 \u05E1 \u05E2 \u05E3 \u05E4 \u05E5 \u05E6 \u05E7 \u05E8 \u05E9 \u05EA"
NEKUDOS: str = "\u05B0 \u05B1 \u05B2 \u05B3 \u05B4 \u05B5 \u05B6 \u05B7 \u05B8 \u05B9 \u05BB \u05BC \u05C1 \u05C2 \u05C4"


def is_equal_without_nekudos(with_nekud: str, without: str) -> bool:
    j: int = 0
    for i, char in enumerate(with_nekud):
        if j == len(without):
            break

        if char == without[j]:
            j += 1
            continue

        if char in NEKUDOS:
            continue

        return False

    return True


def remove_nekudos(word: str) -> str:
    result: str = str()

    for char in word:
        if char in NEKUDOS:
            continue

        result += char

    return result


def enrich_with_nekudos(src_path: Path, nekudos_path: Path) -> bool:
    global ALEF_BEIS
    global NEKUDOS

    with open(
        file=str(Path("in/misc/roshi_taivos.json")), mode="r", encoding="utf-8"
    ) as roshi_taivos_file, open(
        file=str(src_path), mode="r", encoding="utf-8"
    ) as src_file, open(
        file=str(nekudos_path), mode="r", encoding="utf-8"
    ) as nekudos_file:
        roshi_taivos: dict[str, str] = json.load(roshi_taivos_file)

        out_dir = Path("out", "enrich-nekudos")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = Path(out_dir, f"{src_path.name[:-4]}_enriched.txt")

        while src_word_generator := next_word(src_file), nekud_word_generator := next_word(nekudos_file):
            print(src_word_generator)
            print(nekud_word_generator)

        for word in nekud_word_generator:
            print(word)

        for nekud_line in nekudos_file:
            if "</b> " in nekud_line:
                chapter_header: int = nekud_line.find("</b> ")
                prepared_nekud_line = nekud_line[chapter_header + len("</b> ") :]
                nekud_words = prepared_nekud_line.split(":")
                continue

        for src_line in src_file:
            pass


def next_word(file: io.TextIOWrapper) -> str:
    bracket_open: bool = False
    parenthesis_open: bool = False
    while line := file.readline():
        if line == "\n":
            continue

        for word in line.split(" "):
            if word == "":
                continue

            if "'" in word or '"' in word:
                # swap roshi taivos
                pass

            if "[" in word and not bracket_open:
                # preserve brackets and swap roshi taivos
                pass

            if "(" in word and not bracket_open:
                # preserve parentheses and swap roshi taivos
                pass

            yield word


def generate_roshi_taivos_json(roshi_taivos_path: Path) -> dict[str, list[str]]:
    roshi_taivos: dict[str, list[str]] = dict()
    split_line: list[str] = list()

    with open(file=str(roshi_taivos_path), mode="r", encoding="utf-8") as file:
        for line in file:
            if line == "\n":
                continue

            if "\uFEFF" in line:
                bom_idx = line.find("\uFEFF")
                split_line = line[bom_idx + 1 :].strip().split(":")

            else:
                split_line = line.strip().split(":")

            expansions = split_line[1].split(",")
            if roshi_taivos.get(split_line[0], None) is None:
                roshi_taivos[split_line[0]] = [
                    expansion.strip() for expansion in expansions
                ]
            else:
                roshi_taivos[split_line[0]] += [
                    expansion.strip() for expansion in expansions
                ]

    result_path = Path(roshi_taivos_path.parent, "roshi_taivos.json")
    with open(file=str(result_path), mode="w", encoding="utf-8") as json_file:
        json.dump(roshi_taivos, json_file)

    return roshi_taivos


def split_books_into_pages(books_path: Path, page_break_symbol: str = "++") -> bool:
    PAGE_BREAK_SYMBOL: str = page_break_symbol

    out_dir = Path("out/split_pages")
    out_dir.mkdir(parents=True, exist_ok=True)

    for book_path in books_path.iterdir():
        book_name = book_path.name[:-4]
        book_dir = Path(out_dir, book_name)
        book_dir.mkdir(parents=True, exist_ok=True)

        with open(file=str(book_path), mode="r", encoding="utf-8") as book_file:
            page: str = ""
            page_num: int = 1

            for line in book_file.readlines():
                page_path = Path(book_dir, f"pg_{page_num}.txt")
                page_break_symbol_idx: str = line.find(PAGE_BREAK_SYMBOL)

                if page_break_symbol_idx > -1:
                    page += line[:page_break_symbol_idx]
                    left_over_line = line[page_break_symbol_idx + 2 :]

                    with open(
                        file=str(page_path),
                        mode="w+",
                        encoding="utf-8",
                    ) as page_file:
                        page_file.write(page)

                    page = left_over_line
                    page_num += 1
                else:
                    page += line

    return True


if __name__ == "__main__":
    word: str = "וצריך"
    word_nekud: str = "וְצָרִיךְ"

    enrich_with_nekudos(
        src_path=Path("in/enrich_nekudos/library_lekkutei_amarim.txt"),
        nekudos_path=Path("in/enrich_nekudos/lekkutei_amarim.txt"),
    )
