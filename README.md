# file-bookmarks

Organize bookmarks by keeping them in your file system! `file-bookmarks` keeps your web bookmarks neatly organized with your file so whatever you're working on, you'll always have at hand exactly the bookmarks you need.

Besides opening URLs, `file-bookmarks`, or `fbm` for short, can also place text into you clipboard so you'll no longer have to look up those pesky Meeting passcodes.

## Recommended installation

Clone this repository and create a shell alias or symbolic link `fbm` to the script `fbm.py`.

## Usage

`fbm` can be executed in one of the following modes.

- `fbm NAME, DIR/NAME`\
  opens the closest matching file-bookmark (fbm for short). `NAME` and (optionally) `DIR` are Regular Expressions describing the bookmark's name and directory to look for.

- `fbm -l, --list`\
  lists all fbms found in the current directory tree, organized by directories.

- `fbm -g, --git-remote`\
  opens git remote if cwd has git repository

- `fbm -n, --new NAME URL [COPY-TEXT]`\
  creates a new fbm `NAME` for `URL` that (optionally) places `COPY-TEXT` into the clipboard when opened. The fbm will be created in the closest parent directory (or current working directory) that already has fbms associated with it.

- `fbm -ni, --new-in DIR NAME URL [COPY-TEXT]`\
  like `-n`, but chooses closest directory matching `DIR` RegEx.

- `fbm -nh --new-here NAME URL [COPY-TEXT]`\
  creates new fbm associated with current working directory, regardless of wether it is already associated with fbms. Use this to create your first fbm.

- `fbm -rm --remove`\
  work in progress

