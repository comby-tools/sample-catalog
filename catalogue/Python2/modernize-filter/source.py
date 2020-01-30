def read_source_and_diff(path, files):
    sources = filter(lambda x: x.startswith("source"), files)
    source = filter(lambda x: not x.endswith("diff"), sources)
    if source != []:
        source = source[0]
    else:
        print("No source file in {}, please add one.".format(path))
        sys.exit(1)
