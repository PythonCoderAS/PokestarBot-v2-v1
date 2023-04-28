---
title: Image Template Modes
description: The modes of an image template
published: true
date: 2021-08-27T17:34:27.076Z
tags: image_template
editor: markdown
dateCreated: 2021-08-15T21:10:11.339Z
---

Image templates have two modes, guild mode, and global mode.

# Guild Mode

[Guild](/glossary/guild) mode is a mode where the image template is local to the guild that it is created in. This would be useful if you have an image template that you want to use with friends but not have shown on other servers.

You can only use this mode inside a guild.

A guild template and a global template can have the same name.

# Global Mode

Global mode is a mode where the image template is shared with everyone.

You can use this mode in all guilds and in bot DMs.

This mode is the default mode for making new image templates.

# Priority

When the bot resolves templates, guild templates are prioritized first. Therefore, if a guild template and a global template shares the same name, the guild template will be used unless the global mode is explicitly declared.