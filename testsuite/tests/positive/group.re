GROUP(
	@"hello",
	ANY(
		VARCHAR("0-9", 2),	#This is a comment
		@"text",
		VARCHAR("a-z", 1, 10)
	)
)
