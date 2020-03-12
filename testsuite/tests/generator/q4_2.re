@"["
GROUP(
    ANY(
        INLINE @"Edna", # BUG! NEEDS comma before INLINE
        GROUP(@"P", @"h", GROUP(@"i" OR, @"j"), @"l")
        @"Tom",
        @"George",
        @"Harry"
    )
)
@"->]"
