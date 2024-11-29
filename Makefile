all: clean pdf
clean:
	rm -f ./*.aux ./*.bbl ./*.bcf ./*.blg ./*.fdb_latexmk ./*.fls ./*.gz ./*.lof ./*.log ./*.lot ./*.nlo ./*.out ./*.tdo ./*.toc ./*.xml
pdf:
	latexmk -f main.tex
