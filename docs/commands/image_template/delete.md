---
title: Command: image_template delete
description: Delete an image template
published: true
date: 2021-08-27T17:34:27.085Z
tags: commands, image_template commands, image_template
editor: markdown
dateCreated: 2021-08-15T23:19:37.346Z
---

*Parent:* [*image\_template*](/commands/image_template)

Delete an image template. Note: You need to be the image template owner in order to delete an image template. If no arguments are given, then an interactive [menu](/glossary/menu) is started.

*Syntax:* `*image_template delete [name] [--mode {"EITHER"|"0"|"GUILD"|"1"|"GLOBAL"|"2"}=EITHER]*`

# Permissions

Everyone can run this command.

# Arguments

## name

The name of the image template to delete.

## \--mode=

The mode of the image template to delete.

Type: [Literal Argument](/glossary/argument#literal-arguments)

### Valid Values

| Mode | Values (Case Insensitive) |
| --- | --- |
| [Either](/commands/image_template/modes#priority) | -   `Either`<br>-   `0` |
| [Guild Mode](/commands/image_template/modes#guild-mode) | -   `Guild`<br>-   `1` |
| [Global Mode](/commands/image_template/modes#global-mode) | -   `Global`<br>-   `2` |

# Examples

An example usage of the command is `%image_template delete my_template`

# Interactive Menu

When used without any arguments, a menu is created. The menu has a few criteria, the most important being that only the person who created a menu can use it.

## Set Image Template Name

To overwrite a saved name, the button can be used again.

## Delete

-   In order to delete a template, a name is required. The Delete button will be locked until a name is provided.
-   Once the delete button is used, the menu can no longer be used again. The bot also disables all buttons to ensure this is the case.

## Clear Data

The menus have a clear button. This will reset the menu to its default state. The button will be disabled if there is nothing to clear, such as when a menu is newly created or after the button is used.

## Template Mode Dropdown

Only one option is allowed to be chosen by the dropdown. The “Either” option will delete a guild template if one exists, or a global template if one does not.

# Subcommands

The command has no subcommands.

# Aliases

This command has no aliases.

# Subcommands

No slash commands link to the command.