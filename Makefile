LATEX=pdflatex
PREFIX=wp-degree

all: $(PREFIX).pdf

%.pdf: %.tex
	$(LATEX) $<

clean:
	$(RM) $(PREFIX).pdf $(PREFIX).aux $(PREFIX).log
