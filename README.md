# The Weird Part of YouTube
This is a small script that aims to answer two questions.

1. Is a video in the "weird part" of YouTube?
2. How far is a video from the "weird part" of YouTube?

API secrets have been omitted for obvious reasons.



# Changelog

Original indicators:
--------------------
	["weird", "part", "of"], ["wierd", "part", "of"], ["that's", "enough", "internet"],
	["enough", "for", "today"], ["how", "did", "i", "get", "here"],
	["what", "did", "i", "just", "watch"], ["the", "fuck", "did", "i"],["i'm", "in", "hell"],
	["im", "in", "hell"], ["why", "am", "i", "watching"]

Arrangements of each of the phrases sound like a good starting point.



Changes 7/30/16:
----------------
    ["weird", "part", "of"], ["wierd", "part", "of"], ["that's enough internet"], ["enough for today"],
    ["how", "did i get here"], ["what", "did", "i just watch"], ["the fuck did i", "watch"],
    ["i'm in hell"], ["im in hell"], ["why", "what", "am i watching"]

Trying to reduce the number of false positives. Combining separate words should increase strictness.