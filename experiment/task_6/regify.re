GROUP(
    VARCHAR("A-Za-z0-9_", 1, MORE),
    @"@" VARCHAR("A-Za-z", 1, MORE),
    ANY(
        @".com",
        @".net"
    )
)