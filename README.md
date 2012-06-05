# Sublime Manpage

SublimeManpage is small plugin for calling `man` utility from
Sublime Text 2 editor. Result is opened in new tab inside the
editor.

Plugin **does not** work on Windows.

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

Copyright (C) 2012 Milan Kubik <apophys@kubikmilan.sk>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.