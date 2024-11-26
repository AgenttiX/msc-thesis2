# $pdf_mode = 1;
# $pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode --shell-escape';

$lualatex = 'lualatex -interaction=nonstopmode --file-line-error --shell-escape %O %S';
$pdflatex = 'xelatex -synctex=1 -interaction=nonstopmode --file-line-error --shell-escape %O %S';
