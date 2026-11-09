# Plane Tracker

A repository containing Plane.so project management automation scripts and standardized agent skills.

## Features

- **Plane Automation Scripts**: Python scripts interacting with the Plane.so API for issue tracking, project states, modules, and work item verification.
  - `inspect_plane.py`: Query projects, states, labels, and issue counts.
  - `create_all_items.py`: Bulk create work items and modules.
  - `populate_metadata.py`: Populate labels and project metadata.
  - `finish_remaining_items.py`: Script to complete remaining task transitions.
  - `delete_tutorials.py`: Clean up default tutorial items.
  - `verify_all.py`: Verify project and issue states.
  - `test_subitem.py`: Test sub-item hierarchy creation.
  - `get_states.py`: Fetch workspace state identifiers.
- **Agent Skills Hub**: Synchronized skills for AI coding agents (`.agents`, `.claude`, `.kilo`, and `skills/`) sourced from [`panupong1212312121/skill-template`](https://github.com/panupong1212312121/skill-template).

## Skills Management

- Sync skills across agent platforms:
  ```powershell
  powershell -File scripts\sync-skills.ps1
  ```
- Run skills audit:
  ```powershell
  powershell -File scripts\audit-skills.ps1
  ```
