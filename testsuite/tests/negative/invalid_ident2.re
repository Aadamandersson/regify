VARCHA("a-z", 1)
GROUP(
	@"hello"
	ANY(
		VARCHAR("0-9", 2),
		@"text",
		VARCHAR("a-z")
	)
)
