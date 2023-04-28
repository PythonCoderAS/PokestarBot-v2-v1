---
title: Glossary: Alias
description: 
published: true
date: 2021-08-27T17:34:25.224Z
tags: glossary
editor: markdown
dateCreated: 2021-08-12T19:56:23.033Z
---

An alias is another name for a command or subcommand. Aliases will not show up on any lists or command helps, but work as drop-in replacements wherever needed. It is possible to nest aliases, or provide an alias of a parent command and then provide a different alias for a subcommand.

# Automatic Aliases

To make it easier to enter commands from a mobile device, PokestarBot automatically creates aliases. All command names and aliases with an underscore will have additional aliases including an alias of the command where the underscore is replaced with a hyphen, and an alias of the command where the underscore is omitted completely.

-   Scenario 1: A command has an alias of `an_alias`. The command would also have the aliases `an-alias` and `analias`.
-   Scenario 2: A command has the name of `example_command` (not an alias but the actual name). The command would have the aliases `example-command` and `examplecommand`.
-   Scenario 3: A command has the name of `example_command` as well as aliases `an_alias` and `another_alias`. This command would have 6 aliases:
    -   `example-command` and `examplecommand`
    -   `an-alias` and `analias`
    -   `another-alias` and `anotheralias`