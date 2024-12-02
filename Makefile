all: clean pdf
clean:
	rm -f ./*.aux ./*.bbl ./*.bcf ./*.blg ./*.fdb_latexmk ./*.fls ./*.gz ./*.lof ./*.log ./*.lot ./*.nlo ./*.out ./*.tdo ./*.toc ./*.xml
pdf:
	# Allow exit code 12. The double $$ is needed in a Makefile to refer to a shell variable instead of a make variable.
	# https://stackoverflow.com/a/16315249
	latexmk -f || [ $$? -eq 12 ]
