GROUP(
    VARCHAR("A-Za-z0-9_", 1, MORE), # Username
    @"@" VARCHAR("A-Za-z", 1, MORE), # Email domain name
    ANY(
        @".com",
        @".net"
    )
)