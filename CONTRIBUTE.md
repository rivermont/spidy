# Contributing
We would love your help with anything!<br>
If you find a bug raise an issue, and if you have a suggestion go ahead and fork it.<br>
We will happily look at anything that you build off of spidy; we're not very creative people and we know that there are more/better ideas out there!

***

## Notable TODOs

  - Better documentation ([#23](https://github.com/rivermont/spidy/issues/23)):
    - In `docs.md`, many functions and variables simply have "TODO" as their description. These need filling out.
    - More inline comments is not bad either.
  - Multiple HTTP threads at once, using [mutexes](https://stackoverflow.com/questions/3310049/proper-use-of-mutexes-in-python) to corrdinate lists.
  - Working GUI - the remnants of our efforts can be found in `gui.py`

### Less Important

  - Automatic bug dealing-with with Travis CI and/or Sentry would be nice
  - Respecting of `robots.txt`, with a disable option
  - PyPI/pip/apt?

Very trivial edits may be ignored, but things like spelling and grammar correction is fine.

**If you make changed to `crawler.py`, please adjust the line values in `docs.md`. That way links won't break.**

If you make any changes please update the version as well as the badges on README lines [18 and 19](https://github.com/rivermont/spidy/blob/master/README.md#L18).

* `Lines of Code` is calculated: `len(crawler.py) + len(gui.py) + len(tests.py)`
* `Lines of Docs` is calculated: `len(README.md) + len(DOCS.md) + len(CONTRIBUTE.md)`

Thanks!

***
