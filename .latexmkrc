@default_files = ('main.tex');

# https://mg.readthedocs.io/latexmk.html#advanced-options
# https://tex.stackexchange.com/a/105978/214874
add_cus_dep( 'nlo', 'nls', 0, 'makenlo2nls' );
sub makenlo2nls {
    system( "makeindex -s nomencl.ist -o \"$_[0].nls\" \"$_[0].nlo\"" );
}

# $pdf_mode = 1;
# $pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode --shell-escape';

$lualatex = 'lualatex -interaction=nonstopmode --file-line-error --shell-escape %O %S';
$pdflatex = 'xelatex -synctex=1 -interaction=nonstopmode --file-line-error --shell-escape %O %S';
