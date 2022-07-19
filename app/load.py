import typing as T
import uuid

import pandas as pd
import docx as dx
from Levenshtein import distance as lev

from app.const import COLUMNS, QUESTIONS, CONSTRUAL_QUESTIONS


class Region(T.TypedDict):
    files_method: T.Callable[[], T.List[str]]
    name: str


def _gen_df():
    columns = COLUMNS
    columns.extend([f"q{num+1}" for num in range(27)])
    columns.extend([f"cq{num+1}" for num in range(5)])
    df = pd.DataFrame(columns=columns)
    return df


def _remove_rlgn(row: T.List):
    rlgns = ["Sunni", "Shia", "SUNNI", "SHIA"]
    for rlgn in rlgns:
        try:
            ix = row.index(rlgn)
        except ValueError:
            continue
        if(row[ix] == row[ix + 1]):
            del row[ix]


def _add_table_cnt(row: T.List, doc: dx.Document, region: Region):
    table = doc.tables[0]
    row.extend([cell.text for cell in table.rows[2].cells[2:5]])
    row.extend([cell.text for cell in table.rows[2].cells[6:]])
    row.extend(
        [cell.text for cell in table.columns[2].cells[3:11]])
    row.extend([cell.text for cell in table.columns[-1].cells[3:-3]])
    if(region["name"] == "kabul"):
        row.extend([cell.text for cell in table.columns[-1].cells[-3:]])
    else:
        row.extend([cell.text for cell in table.columns[-1].cells[-2:]])
    _remove_rlgn(row)


def _simplify(txt: str):
    return txt.replace(" ", "").replace("-", "").replace(",", "").lower()


def _add_q_index(paragraphs: T.List[str], q_: str, q_indices: T.List[int]):
    ixs = []
    for pix, p_ in enumerate(paragraphs):
        if(not len(p_)):
            continue
        lev_pct = lev(_simplify(p_), _simplify(q_)) / len(p_)
        if(lev_pct < .3):
            ixs.append([pix, lev_pct])
    if(not len(ixs)):
        raise ValueError(f"Question: {q_} not found in the file.")

    ixs_ = [ix for ix in ixs if ix[0] > max(q_indices, default=0)]
    ix = min(ixs_, key=lambda x: x[1])[0]
    q_indices.append(ix)


def _get_q_indices(paragraphs: T.List[str], qs: T.List[str]) -> T.List[int]:
    q_indices = []
    for q_ in qs:
        _add_q_index(paragraphs, q_, q_indices)
    return q_indices


def _fix_inconsistent_qs(paragraphs):
    inconsistent_q = "Was the interviewee ever reluctant in responding to questions? If yes, did they share why"
    if(inconsistent_q in paragraphs):
        iq_ix = paragraphs.index(inconsistent_q)
        new_q = paragraphs[iq_ix] + " " + paragraphs[iq_ix+1]
        paragraphs[iq_ix] = new_q
        del paragraphs[iq_ix+1]


def _add_q(paragraphs: T.List[str], q_ix: int, q_indices: T.List[int], ix: int, row: T.List):
    try:
        ans_end_ix = paragraphs[q_ix:].index("") + q_ix \
            if ix == len(q_indices) - 1 \
            else q_indices[ix+1]
    except ValueError:
        ans_end_ix = len(paragraphs)
    ans = "".join(paragraphs[q_ix+1: ans_end_ix])
    row.append(ans)


def _add_qs(row: T.List, doc: dx.Document, qs: T.List[str]):
    paragraphs: T.List[str] = [
        p.text for p in doc.paragraphs if not p.text.startswith("On") and not p.text.startswith("Regarding")]

    _fix_inconsistent_qs(paragraphs)

    paragraphs = [p.replace("revenue office", "") for p in paragraphs]

    q_indices = _get_q_indices(paragraphs, qs)

    for ix, q_ix in enumerate(q_indices):
        _add_q(paragraphs, q_ix, q_indices, ix, row)


def transform_load(region: Region):
    files = region["files_method"]()
    data = _gen_df()

    for file in files:
        doc = dx.Document(file)
        row = [str(uuid.uuid4())[:8]]
        _add_table_cnt(row, doc, region)
        _add_qs(row, doc, QUESTIONS)
        _add_qs(row, doc, CONSTRUAL_QUESTIONS)
        data.loc[len(data)] = row

    data.set_index("Interview ID", inplace=True)
    data.to_csv(f"out/{region['name']}.csv")
