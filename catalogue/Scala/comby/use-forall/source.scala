val l = List(true, false, false, true)
val andAll = l.foldLeft(true)(_ && _)
