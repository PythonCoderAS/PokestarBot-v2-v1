---
title: Removed in Version 2.0
description: A list of what was removed between versions 1.0 and 2.0
published: true
date: 2021-08-27T17:33:44.997Z
tags: versions, changelog
editor: markdown
dateCreated: 2021-08-10T20:34:33.785Z
---

Version 2.0 has been significantly trimmed to get rid of excess commands as some features are now deemed irrelevant by the existence of new Discord features as well as other third party apps for mobile OSes. This is a non-exhuastive list of what has been removed.

# Anime/Manga Updates

Version 1.0 supported a system of periodically polling anime/manga websites for updates. This system has been removed due to the instability of the websites used as well as third party manga apps that handle the functionality much better.

# Reddit Moderation System

Version 1.0 supported a system of periodically polling the modqueue/unmoderated list of certain approved subreddits for new items to moderate as well as polling the modlog to post new items. This system has been removed due to it frequently wasting resources due to the memory used by the Reddit wrapper for Python.

# Color Roles

Version 1.0 supported a system of adding roles to users based on colors. This system has been removed due to requiring managa role permissions as well as conflicting with newly added roles. 2.0 will include a command to prune all color roles.

# Replay Mode

Version 1.0 supported a system of replaying all messages as if they were sent again. This system has been removed due to the complexity behind it.

# Bot Stats

Version 1.0 showed some statistics about the bot. This command has been removed in 2. 0 and it is advised to use the Grafana dashboard.

# Clean Embeds/Clean Message Goals

These commands have never been used since they were added and have been superseded by the mass delete command.

# Extended Help

Extended help can now be found on the bot website.

# Channel ID/User ID

These commands have been removed in favor of using Developer Mode.

# Prune Ad

The feature that deleted the "ad" messages from the Paisley Bot has been removed.