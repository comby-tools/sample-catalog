#!/usr/bin/env python

import json
import re
import sys
import os
import subprocess

from collections import defaultdict

comby_path = "comby"

def parse_doc_markdown(doc_file_path):
    doc_md = defaultdict(lambda: "[]")
    doc_line = re.compile(r'''^\*\*([\w\s]+?)[:?.!]?\*\*(.*)''')
    with open(doc_file_path) as doc_file_path:
        for line in doc_file_path:
            match = re.match(doc_line, line)
            if match:
                heading = match.groups()[0].lstrip()
                text = match.groups()[1].lstrip()
                doc_md[heading] = text
            else:
                print ("Bad doc.md format in {}".format(doc_file_path))
                os.exit(1)
        tags = doc_md["Tags"]
        doc_md["Tags"] = eval(tags)
    return doc_md


def read_templates(path):
    match_rule = ""
    rewrite_rule = ""

    try:
        with open(os.path.join(path, "match")) as f:
            match = f.read().rstrip()
    except:
        print ("No match file")
        os.exit(1)

    try:
        with open(os.path.join(path, "match_rule")) as f:
            match_rule = f.read()
        with open(os.path.join(path, "rewrite_rule")) as f:
            rewrite_rule= f.read()
    except:
        pass

    try:
        with open(os.path.join(path, "rewrite")) as f:
            rewrite = f.read().rstrip()
    except:
        print ("No rerwite file")
        os.exit(1)

    return match, match_rule, rewrite_rule, rewrite


def generate_diff_file(path, source):
    suffix = source.split('.')[1]
    command = "{} -d {} -f .{} -templates {} -i".format(comby_path, path, suffix, path)
    print("Running: {}".format(command))
    with open(os.devnull, 'w') as devnull:
        _ = subprocess.check_output(command, shell=True, stderr=devnull)
    command = "git diff {}".format(os.path.join(path, source))
    print("Running: {}".format(command))
    diff = subprocess.check_output(command, shell=True)
    _ = subprocess.check_output("git checkout -- {}".format(os.path.join(path, source)), shell=True)
    diff = '\n'.join((diff.split('\n')[5:]))
    diff_out_path = os.path.join(path, "source.diff")
    with open(diff_out_path, "w") as outfile:
        outfile.write(diff)


def read_source_and_diff(path, files):
    sources = [x for x in files if x.startswith("source")]
    source = [x for x in sources if not x.endswith("diff")]
    if source != []:
        source = source[0]
    else:
        print("No source file in {}, please add one.".format(path))
        sys.exit(1)

    with open(os.path.join(path, source)) as f:
        source_content = f.read()

    generate_diff_file(path, source)
    with open(os.path.join(path, "source.diff")) as f:
        diff_content = f.read()
    return source_content, diff_content


def required_files_exist(files, subdirs):
    leaf = "DOC.md" in files and "match" in files and "rewrite" in files
    leaf_with_variants = "DOC.md" in files and subdirs != []
    return leaf or leaf_with_variants


def generate_entry_doc(language, doc, path, files):
    doc = dict(doc)
    doc.pop("Tags", None)

    match, match_rule, rewrite_rule, rewrite = read_templates(path)
    doc["match"] = "```comby\n{}\n```".format(match)
    doc["rewrite"] = "```comby\n{}\n```".format(rewrite)
    if match_rule != "":
        doc["match_rule"] = "```comby\n{}```".format(match_rule)
    if rewrite_rule != "":
        doc["rewrite_rule"] = "```comby\n{}```".format(rewrite_rule)

    source, diff = read_source_and_diff(path, files)
    doc["source"] = "```{}\n{}```".format(language.lower(), source)
    doc["diff"] = "```diff\n{}```".format(diff)
    return doc

def extension_of_language(language):
    if language == "Go":
        return ".go"
    elif language == "Dart":
        return ".dart"
    elif language == "Rust":
        return ".rs"
    elif language == "C" or language == "C++":
        return ".c"
    elif language == "Erlang":
        return ".erl"
    elif language == "Elm":
        return ".elm"
    elif language == "OCaml":
        return ".ml"
    elif language == "Scala":
        return ".scala"
    elif language == "Python":
        return ".py"
    elif language == "Clojure":
        return ".clj"
    else:
        return ".generic"

# {"source":"x","match":"hello","rule":"where%20true","rewrite":"motto","language":".go","substitution_kind":"in_place","id":0}
def generate_live_json(language, path, files):
    match, match_rule, rewrite_rule, rewrite = read_templates(path)
    source = read_source_and_diff(path, files)[0]
    d = {}
    d['source'] = source.replace("%","%25")
    d['match'] = match
    d['rewrite'] = rewrite
    d['rule'] = match_rule # FIXME
    d['id'] = 0
    d['substitution_kind'] = 'in_place'
    d['language'] = extension_of_language(language)
    return json.dumps(d, ensure_ascii=False)


def process_leaf(path, files, subdirs, language):
    leaf = "DOC.md" in files and "match" in files and "rewrite" in files
    entry = {}
    parent = os.path.basename(path)
    if leaf:
        doc = parse_doc_markdown(os.path.join(path, "DOC.md"))
        entry["tags"] = doc["Tags"]
        entry["language"] = language
        entry["doc"] = generate_entry_doc(language, doc, path, files)
        entry["name"] = parent
        entry["live"] = generate_live_json(language, path, files)
        return entry
    else: # TODO
        return {}


def parse_directory(path, level, language):
    parent, basename = os.path.split(path)
    if level == 1: language = basename
    if basename == ".git": return {}
    files = os.listdir(path)
    absolute_path_files = map(lambda f: os.path.join(path, f), files)
    subdirs = filter(os.path.isdir, absolute_path_files)
    subdirs = map(os.path.basename, subdirs)
    if required_files_exist(files, subdirs):
        entry = process_leaf(path, files, subdirs, language)
        return True, entry
    else:
        d = {}
        l = []
        for subdir in subdirs:
            succeed, doc = parse_directory(os.path.join(path, subdir), level + 1, language)
            if succeed:
                l.append(doc)
        if l == []:
            return False, {}
        else:
            d[basename] = l
            return True, d

# flatten for doc gen
def flatten(l, acc):
    for e in l:
        if "name" in e:
            acc.append(e)
            continue
        else:
            if isinstance(e, dict):
                flatten(e.values(), acc)
            elif isinstance(e, list):
                flatten(e, acc)
            else:
                continue
    return acc


def main():
    path = os.path.join(os.getcwd(), "catalogue")
    _, catalogue = parse_directory(path, 0, "undefined language")
    catalogue = flatten(catalogue["catalogue"], [])
    # print catalogue
    with open("catalogue.json", "w") as outfile:
        json.dump(catalogue, outfile, indent=2)

def check_python_version():
    if sys.version_info[0] != 2:
        raise Exception("Must be using Python 2")

if __name__ == "__main__":
    check_python_version()
    main()
