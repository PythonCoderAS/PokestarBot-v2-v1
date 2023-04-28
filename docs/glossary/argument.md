---
title: Glossary: Argument
description: 
published: true
date: 2021-08-27T17:34:24.204Z
tags: 
editor: markdown
dateCreated: 2021-08-10T21:39:40.731Z
---

An argument is a value that can be given to a command. A command will accept zero or more arguments. Arguments are usually separated by spaces, although if you want to pass a value with a string to an argument, you can **enclose the string in quotation marks** (more about that later).

Arguments can be optional or required. Furthermore, arguments can also be repeatable and/or flags.

A limitation of the library running PokestarBot is that no argument can contain unescaped quote symbols.

# Required Arguments

A required argument is an argument that must be present for the command to run. If the argument is not present then the bot will send an error message stating which argument is missing.

# Optional Arguments

An optional argument is an argument that does not need to specify. Specifying an optional argument usually leads to an alternate result from the command.

# Repeatable Arguments

A repeatable argument is an argument that can accept multiple values. For example, a command that might allow a user to run actions on several [members](/glossary/member) will allow you to specify multiple [mentions](/glossary/mention), separated by spaces. When an argument is repeatable, it usually is looking for a certain value and will stop processing new values once a value that does not match the argument type is found.

# Flag Arguments

A flag argument is an argument that has a prefix and a suffix denoting where the argument starts and the data stats. PokestarBot's flags look very similar to UNIX command-line arguments except that there is no need to quote strings with spaces. An example flag argument might be `--name=A Name`, and this would pass the value `A Name` onto the `name` argument. Flag arguments appear at the end of a syntax chain, so there is no ambiguity between a normal argument and a flag argument.

# Quote Escaping Arguments

By default, arguments are separated by spaces. Therefore, special care is needed when entering words with spaces into an argument. Luckily, a mechanism called **quote escaping** makes it possible to provide arguments with spaces. Simply, it means that an argument with spaces has to be surrounded by quotes. An example would be `%command “A Value”`. Normally, the words `A` and `Value` would get interpreted as two different arguments, but in this case, they are provided as one argument to the bot, including the spaces. 

However, not all arguments support quote escaping. Due to the way they work, flag arguments will never be quote escapable. Furthermore, some arguments will not be quote escapable because they automatically ignore spaces, making quoting redundant. However, all non-flag commands that aren't the last command in a syntax chain will always be quote escapable. When quotes are used inside of arguments that do not support quotes, the quotes will be copied as-is to the bot.

## Limitations of Quotes

Due to the way that quote escaping works, **unescaped quote symbols** cannot be used inside of arguments supporting quote escaping. Instead, they must be **escaped** with a backslash (`\)`. An example of quote symbol escaping would be `%another_command A_\"value_with_quotes\"`.

# Argument Types

Some arguments accept custom values while other arguments expect members, channels, and so on. There are multiple ways to specify these data types, but they are the same for all arguments that accept the given type. This means that any of the member formats are accepted for any argument taking a Member.

## Literal Arguments

A literal argument is an argument when there is a predefined list of exact values to submit. If a value that is not on the list is submitted, an error will be raised.  Literal arguments will contain a list of the valid values. Literal values are usually case-sensitive, but case-insensitive literals will be noted.

## Boolean Arguments

Boolean values are a subset of literal arguments that will always accept the same set of values. A boolean has two lists of accepted values: one list meaning “True” and one list meaning “False”. Boolean values are not case sensitive, unlike most literal values.

### Valid Boolean Values

| True Values | False Values |
| --- | --- |
| -   `yes`<br>-   `true`<br>-   `on`<br>-   `enable`<br>-   `y`<br>-   `t`<br>-   `1` | -   `no`<br>-   `false`<br>-   `off`<br>-   `disable`<br>-   `n`<br>-   `f`<br>-   `0` |

## User Arguments

When a user is required, this means that the user does not have to be in the same guild as the channel in which the command is being run. The following values are accepted for user arguments:

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `id` | The numeric user id. | `480521405427875842` |
| 2   | `@user` | A mention | `@PokestarBot#9763` |
| 3   | `Username#Discriminator` | The username and the user's discriminator, separated by an `#` | `PokestarBot#9763` |
| 4   | `Username` | The username. **Note: Multiple people can share the same username including people in guilds the bot is in but you are not, please do not use this!** | `PokestarBot` |

## Member Arguments

A member argument is very similar to a user argument. However, when a member is required, this means that the target user has to be in the same guild as the channel in which the command is being run. Furthermore, this also means that the username search is also scoped to the guild, and is, therefore, safe to use if only one user with the same name exists in the guild. Finally, nickname search is supported as well, although it has the same pitfalls as the username search.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `id` | The numeric user id. | `480521405427875842` |
| 2   | `@user` | A mention | `@PokestarBot#9763` |
| 3   | `Username#Discriminator` | The username and the user's discriminator, separated by an `#` | `PokestarBot#9763` |
| 4   | `Username` | The username. **Note: Multiple people can share the same username, please do not use this unless you are 100% sure only one person has this username!** | `PokestarBot` |
| 5   | `Nickname` | The nickname. **Note: Multiple people can share the same nickname, please do not use this unless you are 100% sure only one person has this nickname!** | `MyNick` |

## Message Arguments

A message argument requires a specific message. This message must not be deleted.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `<channel_id>-<message_id>` | The channel-message ID combo (retrieved by shift-clicking on `Copy ID` when copying a message's ID). | `480523985151459329-874505189514678282` |
| 2   | `id` | The numeric message id. | `874505226219057173` |
| 3   | `jump_url` | The URL that links to this message (obtained via `Copy Message Link`) | [`https://discord.com/channels/@me/480523985151459329/874501820414849064`](https://discord.com/channels/@me/480523985151459329/874501820414849064) |

## Channel Arguments

A channel argument targets a channel in a guild. It does not work inside of a DM.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `id` | The numeric channel id. | `480523985151459329` |
| 2   | `#channel` | A channel mention. Usually used only with text channels, since you would have to manually construct a mention for any other type of channel. | `#general` |
| 3   | `channel` | The channel's name. **Note: Multiple channels can share the same name, please do not use this unless you are 100% sure only one channel has this name!** | `general` |

## Role Arguments

A role argument targets a role in a guild. It does not work inside of a DM.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `id` | The numeric role id. | `480523985151459329` |
| 2   | `@role` | A role mention. | `@everyone` |
| 3   | `role` | The role's name. **Note: Multiple roles can share the same name, please do not use this unless you are 100% sure only one role has this name!** | `everyone` |

## Guild Arguments

A guild argument targets a guild. This is primarily intended for the bot owner.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `id` | The numeric guild id. | `480523985151459329` |
| 2   | `guild` | The guild's name. **Note: Multiple guilds can share the same name, please do not use this!** | `PokestarBot Management` |

## Invite Arguments

An invite argument targets an invite link.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `id` | The invite ID, or the part after `discord.gg`. | `MnHuvuHR` |
| `url` | The invite URL. | `https://discord.gg/MnHuvuHR` |

## Color Arguments

A color argument targets a specific color.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `0xhex` | The 3 or 6-character hex representation of a color. | `0xffffff` |
| `#hex` | `#ffffff` |
| `0x#hex` | `0x#ffffff` |
| `rgb(r, g, b)` | The values of red, green, and blue in the color. Each component must be an integer from 0 to 255. | `rgb(255, 255, 255)` |
| `name` | One of the names from the predefined color list, which can be found below. | `blurple` |

### Predefined Color List

This table contains the list of predefined colors recognized by the bot.

| Color name |     |     |     |
| --- | --- | --- | --- |
| `blue` | `dark_orange` | `fuchsia` | `magenta` |
| `blurple` | `dark_purple` | `gold` | `og_blurple` |
| `dark_blue` | `dark_red` | `green` | `orange` |
| `dark_gold` | `dark_teal` | `greyple` | `purple` |
| `dark_gray` | `dark_theme` | `light_gray` | `red` |
| `dark_green` | `darker_gray` | `light_grey` | `teal` |
| `dark_grey` | `darker_grey` | `lighter_gray` | `yellow` |
| `dark_magenta` | `default` | `lighter_grey` |     |

## Emoji Arguments

An emoji argument targets a custom emoji only. Note: You most likely will not be able to use emojis from other guilds that the bot does not have access to.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `id` | The numeric emoji id. | `480523985151459329` |
| 2   | `:emoji:` | The emoji's “mention”. | `:lmaodf:` |
| 3   | `emoji` | The emoji's name. **Note: Multiple emojis can share the same name including emojis in guilds the bot is in but you are not, please do not use this!** | `lmaodf` |

## Thread Arguments

A thread argument targets a thread. This requires threads to be enabled.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `id` | The numeric thread id. | `480523985151459329` |
| 2   | `#thread` | A thread mention. | `#mythread` |
| 3   | `thread` | The thread's name. **Note: Multiple threads can share the same name, please do not use this unless you are 100% sure only one thread has this name!** | `mythread` |

## Command Arguments

A command argument targets a command.

| Priority | Format | Description | Example |
| --- | --- | --- | --- |
| 1   | `name` | The command's name. Aliases can be used | `setup channels` |