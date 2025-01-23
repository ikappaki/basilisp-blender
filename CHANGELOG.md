# Changelog

## Unreleased

- Package as a Blender Extension (#6).
- Enhanced the nREPL Control Panel with a directory browser for selecting the Basilisp Project Directory (#7).
- Increased the minimum Basilisp version to 0.3.6 (#7).
- Replaced the internal nREPL server with the basilisp-nrepl-async package (#9).

## 0.3.0

- Made the nREPL control panel destructible.
- Released a Blender Add-on to display the nREPL control panel.

## 0.2.0

- Added async server interface support in `start-server!` with a client work abstraction.
- Implemented the async Blender nREPL server directly in Basilisp.
- Enhanced error handling to return errors at the interface layer.
- Introduced the nREPL server control panel UI component.
- Upgraded Basilisp to 0.2.4.
- Improved on the nREPL server exception messages by matching that of the REPL user friendly format, backported from [basilisp#973](https://github.com/basilisp-lang/basilisp/pull/973).
- Fix incorrect line numbers for compiler exceptions in nREPL when evaluating forms in loaded files, backported from [basilisp#1038](https://github.com/basilisp-lang/basilisp/pull/1038).
- nREPL server no longer sends ANSI color escape sequences in exception messages to clients, backported from [basilisp#1040](https://github.com/basilisp-lang/basilisp/pull/1040).
- Conform to the `cider-nrepl` `info` ops spec by ensuring result's `:file` is URI, also added missing :column number, backported from [basilisp#1068](https://github.com/basilisp-lang/basilisp/pull/1068).

## 0.1.0

- Added support for evaluating Basilisp code from Blender's Python console, file, and Text Editor.
- Implemented functionality to start the nREPL server from Blender.


