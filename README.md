# sample-catalog

A sample catalog with rewrite templates. Feel free to fork and modify with your own! 

## Layout

The `catalogue` folder contains a directory tree of templates. Each leaf folder is one rewrite pattern, containing the following files.

  - `match` - contains the match pattern
  - `rewrite` - the rewrite pattern
  - `rule` - optional file with a `where ...` rule

When a directory tree is specified with `comby -templates catalogue`, the `catalogue` directory tree is traversed fully and every rewrite pattern is run against the file in the leaf folders. 

Note that when running the `-templates` option without any other flags, all files in the directory will be run against the rewrite patterns. In general, use `-f file-pattern.extension` and/or `-d src` to run against a particular filepath pattern or directory, respectively. However, you don't need to worry about doing that for this catalog, since the generator script takes care of that for you.

The top level language under the `catalogue` directory defines the language label in the rendered site. Use the format in the newline-separated `DOC.md` files ([example](https://raw.githubusercontent.com/comby-tools/sample-catalog/master/catalogue/Dart/dart_style/prefer-is-empty/DOC.md)) to produce output entries as in the [rendered catalog website](https://catalog.comby.dev). 


## Generating

Run `python generate.py` (uses Python 2). This creates a `catalogue.json`. The JSON file is refenced in `index.html` to generate the site.

## Examples

See the [rendered catalog](https://catalog.comby.dev/) for this repository.

See the [comby](https://github.com/comby-tools/comby) tool or [docs](https://comby.dev/) for using it!


