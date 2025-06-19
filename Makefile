all: clean pdf
clean:
	rm -f ./*.aux ./*.bbl ./*.bcf ./*.blg ./*.fdb_latexmk ./*.fls ./*.gz ./*.ilg ./*.ind ./*.lof ./*.log ./*.lot ./*.nlo ./*.nls ./*.out ./*.tdo ./*.toc ./*.xml \
		./tex/*.dvi ./tex/*.log ./main.pdf
pdf:
	# Allow exit code 12. The double $$ is needed in a Makefile to refer to a shell variable instead of a make variable.
	# https://stackoverflow.com/a/16315249
	latexmk  # -f || [ $$? -eq 12 ]
