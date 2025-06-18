#!/usr/bin/env sh

if command -v 7z &> /dev/null; then :; else
  echo "7-Zip was not found. Installing."
  sudo apt-get update
  sudo apt-get install 7zip
fi
if command -v rsync &> /dev/null; then :; else
  echo "rsync was not found. Installing."
  sudo apt-get update
  sudo apt-get install rsync
fi

if [ ! -f main.bbl ]; then
  echo "main.bbl was not found. Compiling the LaTeX files to create it."
  make all
fi

echo "Removing existing arxiv folder and zip file."
rm -rf arxiv arxiv.zip

echo "Creating the arxiv folder and adding files."
mkdir arxiv
mkdir arxiv/anc
# Rsync is used to enable excluding.
rsync -av --exclude=fig/*-converted-to.pdf --exclude=fig/lecture_notes --exclude=fig/tampere --exclude=tex/other_models.tex \
  fig tex \
  .latexmkrc babelbst.tex englbst.tex finnbst.tex LICENSE main.bbl main.tex Makefile swedbst.tex tktl.bst UH-logo.png UH_TCM_MSc.cls \
  arxiv
# Ancillary files are placed in the anc directory.
# https://info.arxiv.org/help/ancillary_files.html
rsync -av --exclude='**/__pycache__' --exclude='*.pyc' --exclude=msc2_python/logs --exclude=msc2_python/tampere \
  msc2_python create_arxiv.sh arxiv/anc
cp -r .github arxiv/anc/github

echo "Creating arxiv.tar.gz"
tar -czvf arxiv.tar.gz arxiv

echo "arxiv.tar.gz created successfully."
