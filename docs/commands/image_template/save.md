---
title: Command: image_template save
description: Save an image template
published: true
date: 2021-08-27T17:34:27.395Z
tags: commands, image_template commands, image_template
editor: markdown
dateCreated: 2021-08-15T23:41:41.836Z
---

*Parent:* [*image\_template*](/commands/image_template)

Save an image template. If no arguments are given, then an interactive [menu](/glossary/menu) is started.

*Syntax:* `*image_template save [url] [name] [--mode {"GUILD"|"1"|"GLOBAL"|"2"}=GLOBAL]*`

# Permissions

Everyone can run this command.

# Arguments

## url

The URL of the template.

## name

The name of the template.

## \--mode=

The mode to save it as. Defaults to Global mode.

Type: [Literal Argument](/glossary/argument#literal-arguments)

### Valid Values

| Mode | Values (Case Insensitive) |
| --- | --- |
| [Guild Mode](/commands/image_template/modes#guild-mode) | -   `Guild`<br>-   `1` |
| [Global Mode](/commands/image_template/modes#global-mode) | -   `Global`<br>-   `2` |

# Examples

An example usage of the command is `%image_template save https://i.pinimg.com/564x/53/84/49/5384495502d8c84abd7e26accafeb223.jpg my_template`

# Interactive Menu

When used without any arguments, a menu is created. The menu has a few criteria, the most important being that only the person who created a menu can use it.

## Set URL

The URL has to be valid, meaning that it starts with either `http://` or `https://` and must have a domain or public IP. To overwrite a saved URL, the button can be used again.

## Set Image Template Name

To overwrite a saved name, the button can be used again

## Save

-   In order to save a template, an image URL and a name is required. The Save button will be locked until a URL and name are provided.
-   Once the save button is used, the menu can no longer be used again. The bot also disables all buttons to ensure this is the case.

## Template Mode Dropdown

Only one option is allowed to be chosen.

## Clear Data

The menus have a clear button. This will reset the menu to its default state. The button will be disabled if there is nothing to clear, such as when a menu is newly created or after the button is used.

# Subcommands

The command has no subcommands.

# Aliases

This command has no aliases.

# Subcommands

No slash commands link to the command.