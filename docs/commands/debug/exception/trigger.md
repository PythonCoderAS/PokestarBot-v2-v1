---
title: Command: debug exception trigger
description: Triggers an exception.
published: true
date: 2021-08-27T17:34:25.852Z
tags: commands, debug commands, debug exception commands
editor: markdown
dateCreated: 2021-08-15T01:30:04.742Z
---

*Parent: [debug](/commands/debug) [exception](/commands/debug/exception)*

Triggers an exception. The exception can be chosen from a pool of builtin exceptions and `discord`/`discord.ext.commands` exceptions.

*Syntax: `debug exception trigger [--name=Exception] [--arg=]`*

# Permissions

Only the owner can run the command.

# Arguments

## \--name=

The name of the exception. Defaults to `Exception`

## \--arg=

Option arg to pass to the exception.

# Examples

An example usage of the command is `%debug exception trigger --name=ValueError --arg="Test"`.

# Subcommands

The command has no subcommands.

# Aliases

*Note: This command has [additional automatically-created aliases.](/glossary/alias#automatic-aliases)*

-   `error`
-   `throw_exception`
-   `trigger_error`
-   `trigger_exception`

This command has no aliases.

# Slash Commands

No slash commands link to the command.