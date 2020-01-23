**What it does:** Replaces `lambda` + `filter` usage with list comprehensions compatible with Python 3.
**Reference:** See [python-modernize](https://github.com/python-modernize/python-modernize) for problem description and [filter() in Python 2](https://docs.python.org/2/library/functions.html#filter) documentation.
**Author:** Anonymous
**Id:** python2-lambda-filter-to-list
**Tags:** ["Compatibility"]
**Known problems:** Should break Python 3 programs if applied, because there filter() returns a generator.
