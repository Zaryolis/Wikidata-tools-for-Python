## Wikidata tools for Python
These are some scripts I wrote to explore the massive Json file available through [Wikidata downloads](https://www.wikidata.org/wiki/Wikidata:Database_download).
It's a 1.5T compacted Json file, and so it can be cumbersome to peruse and manipulate. Currently there are two files in there:
  * One let's you choose a line number, and pretty-prints the JSON for that line. Allows you to see the structure of the file more easily.
  * Another slices all the data for just one locale, and prints the __label__, __description__, and __id__ for that line. It's much smaller, and lets you see the sheer bulk of topics that Wikipedia covers.

All said, this file is just a big, locale-driven colletcion of pointers to where the real information is stored. For me, it's a starting point to understand the full system
and structure for what is the largest collection of data about the world there is.

More scripts to be added as I discover more.
