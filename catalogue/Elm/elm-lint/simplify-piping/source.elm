typeRefs
        |> allRefs
        |> importsWithoutSelf apiSubmodule importingFrom
        |> List.map toModuleName
        |> List.map toImportString
        |> String.join "\n"
