# Sublime Manpage

SublimeManpage is small plugin for calling `man` utility from
Sublime Text 2 editor. Result is opened in new tab inside the
editor.

Plugin now works also on platforms other than Linux and OS X. Though
in a limited way.

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

## Exact match

The plugin now supports an `exact match` functionality. You can turn it on/off either
manually or from command palette.

# Usage

Use `Manpage: Open manual page` option, from command palette or on OS X
key binding `super + shift + m` or key binding `ctrl + alt + m` on Linux.
This will pop up a form in which you can write the function name.

Another possibility is to use `super + alt + w` or `ctrl + alt + w`
on OS X and Linux respectively to lookup the word under the cursor directly.

If `exact_match` is set to true, plugin will open manpage for the *first exact match*
in specified sections.

# Windows (*) support

On windows ((*) any platform other than linux and os x), manual page is opened
in web browser. The plugin currently uses [www.linuxmanpages.com](http://www.linuxmanpages.com).
In this case, plugin does not support listing matching functions but opens
first exact match according to sections as defined in settings.

If functions is not found, an error message is raised.

# Contributors

[Levente Varga](https://github.com/crazybyte), 
[Hector Hurtarte](https://github.com/hectorh30)
[nirm03](https://github.com/nirm03)

# License

This plugin is licensed under the MIT license.
