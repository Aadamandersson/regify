ANY(
    GROUP(
        @"(",
        VARCHAR("\/.,", 2),
        @")"
    ),
    GROUP(
        VARCHAR("-><+", 6)
    )
)
