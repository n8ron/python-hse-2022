FROM python:3.9
COPY src/generate_tex.py generate_tex.py
RUN apt-get update
RUN apt-get install texlive-latex-base -y && apt-get install graphviz -y
RUN python3.9 -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple fibastvizualizer==1.0.4
RUN python3.9 generate_tex.py

WORKDIR artifacts
RUN pdflatex file.tex
RUN rm file.aux file.log