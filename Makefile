LATEX=pdflatex

all: wp-degree.pdf

%.pdf: %.tex
	$(LATEX) $<

clean:
	$(RM) *.pdf *.aux *.log
