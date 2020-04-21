ANY(                                # Can be any of these three patterns
    REPEAT(2,
        GROUP(
            ANY(                    # Starts with comma or dot
                @",",
                @"."
            ),                      # Second char is always colon
            VARCHAR(".;:", 2, 3)
        )
    ),
    GROUP(                      # Name pattern
        @"[",                       # Opens with bracket
        VARCHAR("\/", 1),           # Can be forward or backslash
        ANY(                        # Any of these names
            @"Edna",
            @"George",
            @"Phil",
            @"Harry"
        ),
        @"]"                        # Ends with bracket
    )
    @"[/->]"                        # Static pattern
)



