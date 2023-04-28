---
title: Command: image_template search
description: List and filter image templates
published: true
date: 2021-08-27T17:34:27.393Z
tags: commands, image_template commands, image_template
editor: markdown
dateCreated: 2021-08-16T00:32:07.003Z
---

*Parent:* [*image\_template*](/commands/image_template)

List and/or filter the avaiable list of image commands.

*Syntax:* `*image_template search [--query=] [--mode {"EITHER"|"0"|"GUILD"|"1"|"GLOBAL"|"2"}=EITHER] [--show_info_view=True]*`

# Permissions

Everyone can run this command.

# Arguments

## \--query=

The query to make. Omit this argument to show all image templates.

*Specifying this argument sets* [*argument show\_info\_view*](#-show_info_view) *to False.*

## \--mode=

The mode of image templates to show.

*Note:* `*Either*` *shows **both** guild and global image templates.*

Type: [Literal Argument](/glossary/argument#literal-arguments)

### Valid Values

| Mode | Values (Case Insensitive) |
| --- | --- |
| [Either](/commands/image_template/modes#priority) | -   `Either`<br>-   `0` |
| [Guild Mode](/commands/image_template/modes#guild-mode) | -   `Guild`<br>-   `1` |
| [Global Mode](/commands/image_template/modes#global-mode) | -   `Global`<br>-   `2` |

## \--show\_info\_view=

Whether or not to show the interactive view. Defaults to True.

**Type**: [Boolean Argument](/glossary/argument#boolean-values)

# Examples

An example usage of the command is `%image_template search --query=bad`

# Interactive Menu

When used without any arguments, a menu is created. The menu has a few criteria, the most important being that only the person who created a menu can use it.

## Query

To clear the set query, the “Clear Data” button must be used. To overwrite a saved query, the button can be used again.

## Search

Once the search button is used, the menu can no longer be used again. The bot also disables all buttons to ensure this is the case.

## Clear Data

The menus have a clear button. This will reset the menu to its default state. The button will be disabled if there is nothing to clear, such as when a menu is newly created or after the button is used.

## Template Mode Dropdown

Only one option is allowed to be chosen by the dropdown. The “Either” option will search in both global templates and guild templates.

# Subcommands

The command has no subcommands.

# Aliases

*Note: This command has* [*additional automatically-created aliases.*](/glossary/alias#automatic-aliases)

-   `list`
-   `show_all`

# Subcommands

No slash commands link to the command.