# Tagged-Notes-Naive
Command Line front ends to SQLite tables for notes, tags, and many-to-many lookup (note_id|tag_id), by a hobbyist.

Pretty sure you can uncomment the SQL, run it a line at a time (adjust that path!) in SQLite3, then the Python code will work. I think it is appropriate to leave the SQL comments in the main file to remind you of the triggers.

This started as a TCL script. Later I ported it to Python 2.x, then REBOL. That was my favorite incarnation and I used it for years. REBOL, at least the 2.x version, didn't age well and my attempts at REBOL 3 and later RED-Lang were too frustrating. So now here we are on Python 3. Significant Whitespace has not grown on me, but I expect I can count on Python to be around. The  TCL and Rebol versions will appear here before July 2021.

I am foremost a VBA office-automation coder, and the only coder I know of where I work. My imperative bent shows. This code is not elegant, pythonic, or OO. But it works. I have relied on (some version of) it since 2010. If I find someone has forked it and made it pythonic, elegant, OO, etc.. I will study it, smack my forehead, and adopt it. Especially if it truly handles an arbitrary number of tags.

Maybe this is where I should say the code is provided as-is, with no warranty, etc, etc.
