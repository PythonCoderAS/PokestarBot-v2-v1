---
title: Command: minecraft gamemode
description: Control the current user's gamemode
published: true
date: 2021-08-27T17:34:27.880Z
tags: commands, minecraft commands
editor: markdown
dateCreated: 2021-08-16T19:58:33.511Z
---

*Parent:* [*minecraft*](/commands/minecraft)

Change the "gamemode" of a user. All gamemode changes other than `survival` will be reverted in 30 seconds of being granted unless specified otherwise. This command requires that certain roles are defined via the [setup roles command](/commands/setup/roles).

*Syntax:* `*minecraft gamemode <gamemode> [--user=] [--expires=True]*`

# Gamemodes

## Survival

The base gamemode. This means the user does not have any special roles.

### Roles Required to be Defined

-   [Muted](/commands/setup/roles#muted) in order to remove the role. 
-   [Send All](/commands/setup/roles#send-all) in order to remove the role.

## Adventure

A gamemode where the user can view but not interact with the server. Mutes the users in all text channels and voice channels.

### Roles Required to be Defined

-   [Muted](/commands/setup/roles#muted) in order to mute the user.

## Creative

A gamemode where the user can talk in any text channel. All messages sent under this gamemode to channels the user would not be able to talk in normally will be deleted once the gamemode is changed. 

*Note: This command will not let the user speak in any voice channels due to the fact that you cannot undo speech.*

### Roles Required to be Defined

-   [Send All](/commands/setup/roles#send-all) in order to give the privileges needed.

# Permissions

This command can only be run inside a guild.

### Bot Permissions

The bot needs to have the **Manage Roles** permission.

# Arguments

## gamemode

The [gamemode](#gamemodes) to grant.

## \--user=

The user to grant the user to. When left blank, defaults to the user calling the command.

Note: You will need to have the **Manage Roles** permission in order to use the command on other users.

Type: [Member Argument](/glossary/argument#member-arguments)

## \--expires=

Whether or not to make the role assignment temporary. Defaults to True.

Note: You will need to have the **Manage Roles** permission in order to make the role assignment permanent.

Type: [Boolean Argument](/glossary/argument#boolean-arguments)

# Examples

An example usage of the command is `%minecraft gamemode creative`

# Subcommands

The command has no subcommands.

# Aliases

This command has no aliases.

# Slash Commands

-   `/gamemode`