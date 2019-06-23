**What it does:** Replaces `where` type checks with a more readable `whereType`
**Reference:** See [Effective Dart](https://v1-dartlang-org.firebaseapp.com/guides/language/effective-dart/usage#dont-use-length-to-see-if-a-collection-is-empty). Reference [implementation](https://github.com/dart-lang/linter/blob/master/lib/src/rules/prefer_is_empty.dart) in [dart-lang linter](https://github.com/dart-lang/linter).
**Author:** Anonymous
**Id:** effective-dart-where-type-1000
**Tags:** ["Readability"]
**Known problems:** Only works if `whereType` is implemented.
