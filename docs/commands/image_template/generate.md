---
title: Command: image_template generate
description: Generate an image template.
published: true
date: 2021-08-27T17:34:27.363Z
tags: 
editor: markdown
dateCreated: 2021-08-15T23:23:03.359Z
---

Parent: [image\_template](/commands/image_template)

Generate an image template. If no arguments are given, then an interactive [menu](/glossary/menu) is started.

*Syntax:* `*image_template generate [url] [--name=] [--mode {"GUILD"|"1"|"GLOBAL"|"2"}=GLOBAL] [--message=]*`

# Permissions

Everyone can run this command.

# Arguments

## url

The URL of the image.

*Note: In order to upload an image, send the image in a seperate message (as a DM to PokestarBot, for example) and then copy the media link.*

## \--name=

The name to save the image template as. Setting a name will enable saving the image's url as a template.

## \--mode=

If saving an image, the mode to save it as. Defaults to Global mode.

Type: [Literal Argument](/glossary/argument#literal-arguments)

### Valid Values

| Mode | Values (Case Insensitive) |
| --- | --- |
| [Guild Mode](/commands/image_template/modes#guild-mode) | -   `Guild`<br>-   `1` |
| [Global Mode](/commands/image_template/modes#global-mode) | -   `Global`<br>-   `2` |

## \--message=

An optional message that the bot will send with the image.

# Examples

An example usage of the command is `%image_template generate https://i.pinimg.com/564x/53/84/49/5384495502d8c84abd7e26accafeb223.jpg --message=When your friend starts sprouting antivax propoganda`

# Interactive Menu

When used without any arguments, a menu is created. The menu has a few criteria, the most important being that only the person who created a menu can use it.

## Set URL

The URL has to be valid, meaning that it starts with either `http://` or `https://` and must have a domain or public IP. To overwrite a saved URL, the button can be used again.

## Set Message

In order to set a message, the template needs to have a valid URL. Once a valid URL is provided via the [Set URL](#set-url) button, the Set Message button is unlocked. To overwrite a saved message, the button can be used again.

## Save Image Template on Send / Do Not Save Image Template on Send

By default, the menu will not save the template. This button needs to be clicked in order to allow saving. Once saving is enabled, it can be clicked again to disable saving.

## Set Image Template Name

A name cannot be provided until saving is enabled. To overwrite a saved name, the button can be used again.

**Note: Disabling saving will** ***not*** **clear a name if it has been set.**

## Send

-   In order to send a template, an image URL is required. The Send button will be locked until a URL is provided.
-   When saving is enabled, a name is required. The Send button will be locked until a name is provided.
-   Once the send button is used, the menu can no longer be used again. The bot also disables all buttons to ensure this is the case.

## Template Mode Dropdown

-   The dropdown has no effect until saving is enabled.
-   Only one option is allowed to be chosen.

## Clear Data

The menus have a clear button. This will reset the menu to its default state. The button will be disabled if there is nothing to clear, such as when a menu is newly created or after the button is used.

# Subcommands

The command has no subcommands.

# Aliases

This command has no aliases.

# Subcommands

No slash commands link to the command.