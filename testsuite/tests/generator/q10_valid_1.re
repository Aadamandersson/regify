#ANY(                           # BUG! Any sätter inte in "|" emellan REPEAT o GROUP, fixed
REPEAT(2,
    GROUP(
        ANY(                    # Starts with comma or dot
            @",",
            @"."
        ),                      # Second char is always colon
        VARCHAR(".;:", 2, 3)
    )
)
#,
OR                              # BUG? kommatecken behövs inte, no need
GROUP(
    @"[",
    VARCHAR("/", 1),       # BUG! VARCHAR måste escapa alla specialtecken, fixed
    ANY(                    # Starts with comma or dot
        @"Edna",
        @"George",
        @"Tom",
        @"Phil",
        @"Harry"
    ),
    @"]"
)
#)
