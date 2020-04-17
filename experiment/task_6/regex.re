@"("
    REPEAT(3,
        VARCHAR("0-9", 1, 3),
        @"."
    )
    # Since there shouldnt be a dot after the last number,
    # this has to be outside of the REPEAT
    VARCHAR("0-9", 1, 3)
@")"
