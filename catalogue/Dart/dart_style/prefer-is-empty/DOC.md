**What it does:** Replaces length checks with a more readable and performant getters.
**Reference:** See [Effective Dart](https://v1-dartlang-org.firebaseapp.com/guides/language/effective-dart/usage#dont-use-length-to-see-if-a-collection-is-empty). Reference [implementation](https://github.com/dart-lang/linter/blob/master/lib/src/rules/prefer_is_empty.dart) in [dart-lang linter](https://github.com/dart-lang/linter).
**Author:** Anonymous
**Id:** effective-dart-prefer-is-empty-1000
**Tags:** ["Performance", "Readability"]
**Known problems:** Only works if :[container] is a type implementing the `isNotEmpty` property.
**Improvements:** Add an `isEmpty` variant.
