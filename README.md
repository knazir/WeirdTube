# The Weird Part of YouTube
This is a small, fun project that aims to answer two questions.

1. Is a video in the "weird part" of YouTube?
2. How far is a video from the "weird part" of YouTube?

This aims to answer the question of how far any given video is from the "weird" part of YouTube. You provide a link to a YouTube video and it tells you how far the video is from the "weird" part of YouTube in number of clicks (where each click is from the related videos). The output will also show you the path that was followed from the original video. From testing, it seems that most "weird" videos are identified. Ongoing efforts are to reduce the rate of false positives, normal videos that are marked as weird. Also even though it's called "WeirdTube," no list of weird videos are stored. This may be added in the future though... 

One MAJOR issue is that the search space increases exponentially the farther you get from the original video. Each video searches 10 related videos and those videos search 10 of their related videos. By the time you're 6 clicks away, 1,000,000 videos have to be explored. Therefore, some searches can take an incredibly long time to complete. I'm currenlty thinking about some kind of heuristic to make a guess about which videos are "weirder" than hours. 

It's still very much in testing and has a lot of rough edges. And yes, I mean A LOT of rough edges. The output of the script is just served as plain text... I'll be updating it as time goes on. If you encounter an error or weird behavior, please open an issue for this repo. I'll try to add some kind of feedback button eventually... This is just for fun, don't kill me if it isn't complete... ^^;

Most code changes are being pushed to the Heroku app, but this is a working barebones implementation. API secrets have been omitted for obvious reasons.


# Known Issues
* Search space increases exponentially. Anything more than 4 clicks away takes an inconceivably frustrating amount of time to complete.
* High false positive rate (especially for videos with many comments).


# ToDo List
- [ ] Add feedback button
- [ ] Make output appear dynamically (show progress while running)
- [ ] Make the output prettier
- [ ] Find heuristic to determine if a video is more "weird" than others
- [ ] Aggregate list of "weird" videos users find and add them to a list


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
    ["i'm in hell"], ["im in hell"], ["am i watching"], ["side of the internet"], ["side of YouTube"]

Trying to reduce the number of false positives. Combining separate words should increase strictness.



Changes 7/31/16:
----------------
    ["weird", "part", "of"], ["wierd", "part", "of"], ["that's enough internet"], ["enough for today"],
    ["how", "did i get here"], ["what", "did", "i just watch"], ["the fuck did i", "watch"],
    ["i'm in hell"], ["im in hell"], ["am i watching"], ["side of the internet"], ["side of YouTube"],
    ["what", "is this shit"], ["strangest boner"]

Thought of some more phrases...