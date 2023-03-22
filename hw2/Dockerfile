FROM python:3.9
COPY . .
RUN apt-get update
RUN apt-get install -y texlive graphviz graphviz-dev python3-pygraphviz
RUN pip install networkx pygraphviz
RUN #pip install -i https://test.pypi.org/simple/ astconstructor==0.1.0
RUN python3.9 main.py
WORKDIR artifacts
RUN pdflatex easy_task.tex
RUN pdflatex medium_task.tex
