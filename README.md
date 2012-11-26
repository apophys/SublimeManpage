# Sublime Manpage

SublimeManpage is small plugin for calling `man` utility from
Sublime Text 2 editor. Result is opened in new tab inside the
editor.

Plugin **does not** work on Windows. At least for now.

# Install

Install with [Package Control](http://wbond.net/sublime_packages/package_control).

`Command Palette` > `Package Control: Install Package` > `SublimeManpage`

Or clone this reporitory from github:

```bash
$ git clone https://apophys@github.com/apophys/SublimeManpage.git
```

# Config

Package is shipped with default configuration prepared
for C language - sections 2, 3 and 3p (system calls, function calls).
You can edit the configuration via the menu entry.

`Preferences` -> `Package Settings` -> `SublimeManpage` -> `Settings - Default`

Or

`Command Palette` > `Preferences: SublimeManpage Settings - Default`

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
