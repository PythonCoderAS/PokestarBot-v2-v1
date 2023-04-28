---
title: Command: debug pager lines
description: Generate a pager with a given amount of lines
published: true
date: 2021-08-27T17:34:26.249Z
tags: commands, debug commands, debug pager commands
editor: markdown
dateCreated: 2021-08-15T17:48:28.435Z
---

*Parent: [debug](/commands/debug) [pager](/commands/debug/pager)*

Generate a pager with a given amount of lines.

*Syntax: `debug pager lines <lines> [--text=False] [--text_template=This is test text #{number}] [--line_template=This is test line #{number}] [--embed_title={number} Test Lines]`*

# Permissions

Only the owner can run the commmand.

# Arguments

## lines

The amount of lines.

## \--text=

Whether or not to include text. Defaults to `False`.

**Type**: [Boolean Argument](/glossary/argument#boolean-values)

## \--text\_template=

The text that will be generated for each page when [the text argument](#text) is enabled. By default, the string `This is test text #{number}` is used. The string can contain variable placeholders that take the form `{<variable>}`, where `<variable>` is the name of the variable.

| Variable Name | Description |
| --- | --- |
| `number` | The page number. Starts at 1. |

## \--line\_template=

The text that each line should contain. By default, the string `This is test line #{number}` is used. The string can contain variable placeholders that take the form `{<variable>}`, where `<variable>` is the name of the variable.

| Variable Name | Description |
| --- | --- |
| `number` | The line number. Starts at 1. |

## \--embed\_title=

The title of the embed. By default, the string `{number} Test Lines` is used. The string can contain variable placeholders that take the form `{<variable>}`, where `<variable>` is the name of the variable.

| Variable Name | Description |
| --- | --- |
| `number` | The number of lines. |

# Examples

An example usage of the command is `%debug pager 5 --text=1 --text_template=Test Text #{number} --line_template=Test Line #{number} --embed_title={number} Lines`.

# Subcommands

The command has no subcommands.

# Aliases

*Note: This command has [additional automatically-created aliases.](/glossary/alias#automatic-aliases)*

-   `lines`
-   `test_line`
-   `test_lines`

This command has no aliases.

# Slash Commands

No slash commands link to the command.