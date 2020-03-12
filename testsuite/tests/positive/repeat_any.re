
REPEAT(5,
    ANY(
        @"cat",
        @"dog",
        @"bird",
        @"fish"
        REPEAT(
            1,
            @"hello",
            VARCHAR("aad", 1)
        )
    )
)