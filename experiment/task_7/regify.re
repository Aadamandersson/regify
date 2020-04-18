GROUP(                      # Pattern for URLS with specific domain names
    @"href='https://",      # Will only match HTTPS websites
    ANY(                    # Domain names to match
        @"github",
        @"imgur"
    ),
    INLINE @"[^']*",        # Match anything until a single quote has been encountered
    @"'"
)
OR
GROUP(                      # match all <span> HTML tags
    @"<span>",
    UNTIL,
    @"</span>"
)

