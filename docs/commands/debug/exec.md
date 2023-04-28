---
title: Command: debug exec
description: Execute code.
published: true
date: 2021-08-27T17:34:25.864Z
tags: commands, debug commands
editor: markdown
dateCreated: 2021-08-15T14:31:42.741Z
---

*Parent:* [*debug*](/commands/debug)

Executes code in a function. This allows for more complex multi-line code blocks to be run.

*Syntax:* `*debug exec <block>*`

# Permissions

Only the owner can run the command.

# Arguments

## block

The code block to process.

# Examples

An example usage of the command is

```python
%debug eval ```python
guilds = self.bot.guilds
for guild in guilds:
    print(guild.name, len(guild.members))
return [guild.channels for guild in guilds]```
```

# Subcommands

The command has no subcommands.

# Aliases

*Note: This command has* [*additional automatically-created aliases.*](/glossary/alias#automatic-aliases)

-   `exec_code`
-   `execute`
-   `execute_code`

# Slash Commands

No slash commands link to the command.