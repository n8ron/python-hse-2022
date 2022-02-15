import functools
import os
import datetime
from typing import List, Any
from fibastvizualizer import generate_png


def to_tex_table(matrix: List[List[Any]]) -> str:
    return _to_tex_table(matrix) if _is_valid_table(matrix) else "Incorrect table\n"


def _is_valid_table(matrix: List[List[Any]]) -> bool:
    return len(matrix) > 0 and \
           len(matrix[0]) > 0 and \
           all(
               map(
                   lambda x: len(x) == len(matrix[0]),
                   matrix
               )
           )


def _to_tex_table(matrix: List[List[Any]]) -> str:
    return f"\\begin{{tabular}}" \
           f"{{{_generate_col_desc(len(matrix[0]))}}}" \
           f"\n\\hline\n" + \
           functools.reduce(
               lambda prv, nxt: prv + "\\\\\n\\hline\n" + nxt,
               map(
                   functools.partial(
                       functools.reduce,
                       lambda l, r: str(l) + " & " + str(r)
                   ),
                   matrix
               )
           ) + \
           "\\\\\n\\hline\n" \
           "\\end{tabular}\n"


def _generate_col_desc(n_column: int) -> str:
    return "| c " * n_column + "|"


def include_image(path: str, scale: float = 0.2) -> str:
    return f"\\newline\\newline\\\\\n\\includegraphics[scale={scale}]{{{path}}}\\\\\n"


def latex_header(title: str, author: str, date: str) -> str:
    return (
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{graphicx}\n"
        f"\\title{{{title}}}\n"
        f"\\author{{{author}}}\n"
        f"\\date{{{date}}}\n"
        "\\begin{document}\n"
        "\\maketitle\n\n"
    )


def latex_footer() -> str:
    return "\\end{document}"


if __name__ == "__main__":
    sample = [
        ['14', '2', '30', "232323"],
        ['hello', '555', '6', "2"],
        ['7', '8123123', 'check', "test"]
    ]

    today = datetime.date.today()
    formatted_date = today.strftime("%B %d")

    file_param = {
        "title": "Tex from Python!",
        "author": "n8ron",
        "date": formatted_date
    }
    if not os.path.exists("../artifacts"):
        os.mkdir("../artifacts")

    img_path = "img.png"
    generate_png("../artifacts/" + img_path)

    with open('../artifacts/file.tex', 'w') as f:
        f.write(latex_header(**file_param))
        f.write(to_tex_table(sample))
        f.write(include_image(img_path))
        f.write(latex_footer())
