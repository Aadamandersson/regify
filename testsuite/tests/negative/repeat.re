
REPEAT(5,
    ANY(
        @"cat",
        REPEAT(
            1,
            @"hello",
            VARCHAR("aad", 1)
        ),
        ANY(
            @"cat",
            @"dog"
        )
    )
)
