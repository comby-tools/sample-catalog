all:
	make -C ../highlight.js
	cp ../highlight.js/build/highlight.pack.js js/highlight-comby.js
	python generate.py
