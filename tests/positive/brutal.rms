GROUP(
    VARCHAR("A-Za-z0-9", 10, 15),
    @"example",
    @"text",
    REPEAT(15,
        ANY(
            VARCHAR("0-9A-F", 8)
        )
    )
)
GROUP(
    ANY(
        @"223123",
        VARCHAR("ACEG", 123)
    )
)
