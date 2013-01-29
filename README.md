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
In default, exact match is disabled. Exact match can be turned on/off from
Command Palette.

You can edit the configuration in the user settings.

`Preferences` -> `Package Settings` -> `SublimeManpage` -> `Settings - Default`

Or

`Command Palette` > `Preferences: SublimeManpage Settings - User`

```json
{
    "sections" : [ "2", "3", "3p"],
    "exact_match" : false
}
```

If you need some other sections, just append the section number to this list.

# Usage

Use `Manpage: Open manual page` option, from command palette or on OS X
key binding `super + shift + m` or key binding `ctrl + alt + m` on Linux.
This will pop up a form in which you can write the function name.

Another possibility is to use `super + alt + w` or `ctrl + alt + w`
on OS X and Linux respectively to lookup the word under the cursor directly.

If `exact_match` is set to true, plugin will open manpage for the *first exact match*
in specified sections.

# Contributors

[Levente Varga](https://github.com/crazybyte)

# License

This plugin is licensed under the MIT license.