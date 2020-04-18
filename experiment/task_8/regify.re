ANY(
    REPEAT(2,
        GROUP(
            ANY(                    # Starts with comma or dot
                @",",
                @"."
            ),                      # Second char is always colon
            VARCHAR(".;:", 2, 3)
        )
    ),
    GROUP(
        @"[",
        VARCHAR("\/", 1),
        ANY(
            @"Edna",
            @"George",
            @"Phil",
            @"Harry"
        ),
        @"]"
    )
    @"[/->]"
)