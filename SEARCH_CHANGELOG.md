# Changes to search parameters

Original indicators:
--------------------
	["weird", "part", "of"], ["wierd", "part", "of"], ["that's", "enough", "internet"],
	["enough", "for", "today"], ["how", "did", "i", "get", "here"],
	["what", "did", "i", "just", "watch"], ["the", "fuck", "did", "i"],["i'm", "in", "hell"],
	["im", "in", "hell"], ["why", "am", "i", "watching"]

Reasoning: Arrangements of each of the phrases sound like a good starting point.


Change 7/30/16:
---------------
    ["weird", "part", "of"], ["wierd", "part", "of"], ["that's", "enough", "internet"],
    ["enough", "for", "today"], ["how", "did", "i", "get", "here"],
    ["what", "did", "i just watch"], ["the fuck did i"],["i'm", "in", "hell"],
    ["im", "in", "hell"], ["why", "am", "i", "watching"]

Reasoning: Trying to reduce the number of false positives. Combining separate words would increase strictness.