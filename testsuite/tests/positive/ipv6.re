REPEAT(4,
    VARCHAR("0-9A-Fa-f", 0, 4),
    @":"
)
REPEAT(4,
    VARCHAR("0-9A-Fa-f", 0, 4),
    INLINE @":?" 
)
