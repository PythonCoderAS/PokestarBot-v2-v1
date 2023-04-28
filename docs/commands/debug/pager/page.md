---
title: Command: debug pager page
description: Generates a pager with a given number of pages
published: true
date: 2021-08-27T17:34:26.285Z
tags: commands, debug commands, debug pager commands
editor: markdown
dateCreated: 2021-08-15T18:28:57.132Z
---

*Parent: [debug](/commands/debug) [pager](/commands/debug/pager)*

Generate a [pager](/glossary/pager) with a given amount of pages.

*Syntax: `debug pager page <pages> [--text=True] [--embed=False] [--text_template=This is test line #{number}] [--embed_description_template=This is test embed #{number}]`*

# Permissions

Only the owner can run the command.

# Arguments

## pages

The number of pages to generate.

## \--text=

Whether or not to include text. Defaults to `False`.

**Type**: [Boolean Argument](/glossary/argument#boolean-values)

## \--embed=

Whether or not to include an embed. Defaults to `False`.

**Type**: [Boolean Argument](/glossary/argument#boolean-values)

## \--text\_template=

The text that will be generated for each page when [the text argument](#text) is enabled. By default, the string `This is test text #{number}` is used. The string can contain variable placeholders that take the form `{<variable>}`, where `<variable>` is the name of the variable.

| Variable Name | Description |
| --- | --- |
| `number` | The page number. Starts at 1. |

## \--embed\_description\_template=

The embed description that will be generated for each page when [the embed argument](#embed) is enabled. By default, the string `This is test embed #{number}` is used. The string can contain variable placeholders that take the form `{<variable>}`, where `<variable>` is the name of the variable.

| Variable Name | Description |
| --- | --- |
| `number` | The page number. Starts at 1. |

# Examples

An example usage of the command is `%debug pager page --text=1 --embed=0`.

# Subcommands

The command has no subcommands.

# Aliases

*Note: This command has [additional automatically-created aliases.](/glossary/alias#automatic-aliases)*

-   `pages`
-   `test_page`

# Slash Commands

No slash commands link to the command.