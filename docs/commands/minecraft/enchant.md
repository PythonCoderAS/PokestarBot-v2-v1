---
title: Command: minecraft enchant
description: Enchant your item.
published: true
date: 2021-08-27T17:34:27.867Z
tags: commands, minecraft commands
editor: markdown
dateCreated: 2021-08-16T02:34:29.465Z
---

*Parent:* [*minecraft*](/commands/minecraft)

Enchant the weapon currently held by the player. This requires a weapon to be present in the player's profile.

Enchatments are broken up into 3 [enchantment tiers](#enchantment-tiers), which represent an in-game enchantment table without any bookshelves, ~7-8 bookshelves, and 15 bookshelves respectively.

| Item | How to Obtain | References |
| --- | --- | --- |
| Weapon | A weapon can be obtained via [minecraft give](/commands/minecraft/give). |     |
| Experience | Experience can be obtained via [minecraft xp add ](/commands/minecraft/xp/add) and [minecraft xp set](/commands/minecraft/xp/set). | The amount of experience required can be seen for the given [enchantment tier](#enchantment-tiers). |
| Lapis Lazuli | Lapis Lazuli can be obtained via [minecraft give](/commands/minecraft/give). | The amount of lapis lazuli required can be seen for the given [enchantment tier](#enchantment-tiers). |

*Syntax:* `*minecraft enchant <tier>*`

# Enchantment Tiers

The bot has three tiers of enchantment, representing an enchantment table without any bookshelves, ~7-8 bookshelves, and 15 bookshelves respectively.

| Enchantment Tier | Minimum Level Required | Lapis Lazuli Needed | XP Levels Lost After Enchant | Enchantment Count Range | Enchantment Name | Enchantment Level Range |
| --- | --- | --- | --- | --- | --- | --- |
| 1   | 6   | 1   | 1   | 1   | Sharpness | 1-2 |
| Unbreaking | 1   |
| Fire Aspect | 1   |
| Knockback | 1   |
| Sweeping Edge | 1   |
| Looting | 1   |
| 2   | 17  | 2   | 2   | 1-2 | Sharpness | 2-3 |
| Unbreaking | 1-2 |
| Fire Aspect | 1-2 |
| Knockback | 1-2 |
| Sweeping Edge | 1-2 |
| Looting | 1-2 |
| 3   | 30  | 3   | 3   | 1-4 | Sharpness | 3-5 |
| Unbreaking | 2-3 |
| Fire Aspect | 2   |
| Knockback | 2   |
| Sweeping Edge | 2-3 |
| Looting | 2-3 |

# Permissions

Everyone can run this command.

# Arguments

## tier

The [enchantment tier](#enchantment-tiers).

# Examples

An example usage of the command is `%minecraft enchant 3`

# Subcommands

The command has no subcommands.

# Aliases

This command has no aliases.

# Slash Commands

-   `/enchant`