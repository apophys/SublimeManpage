# Sublime Manpage

SublimeManpage is small plugin for calling `man` utility from
Sublime Text 2 editor. Result is opened in new tab inside the
editor.

Plugin **does not** work on Windows. At least not now.

# Install

Clone this reporitory from github:

```bash
$ cd Sublime Text 2/Packages
$ git clone https://apophys@github.com/apophys/SublimeManpage.git
```

# Config

Package is shipped with default configuration prepared
for C language - sections 2, 3 and 3p (system calls, function calls)

```json
{
    "sections" : [ "2", "3", "3p"]
}
```

If you need some other sections, just append the section number to this list.

# Usage

Use `Manpage: Open manual page` option, from command palette or on OS X
key binding `super + shift + m` or key binding `ctrl + alt + m` on Linux.


# License

This plugin is licensed under the MIT license.