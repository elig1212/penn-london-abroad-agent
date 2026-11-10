---
name: calendar-sync
description: Sync key dates from me/deadlines.json (and class times from me/courses.json) to Google Calendar. Use for "put my deadlines in my calendar", "sync calendar".
---
# Calendar sync
- Target: the user's Google Calendar via the calendar tools (`list_calendars` → pick the user's own calendar, e.g. their Penn or
  personal one; ask the first time and store in `profile.preferences.calendar_id`). Tested 2026-11-10: create + delete works.
- Event format: summary "[Abroad] <title>", `notificationLevel: NONE`, `overrideReminders` popup 10080 min (7 days) + 1440 min (1 day).
  All-day for date-only deadlines (`allDay: true`). UK-time deadlines: pass `timeZone: "Europe/London"` with the local UK time.
- For each open deadline without `calendar_event_id`: propose the list of events first (title "[Abroad] …", date, time + tz,
  reminders 7 days and 1 day before). After a yes, create them and store the event id back in `deadlines.json`.
- Class times: only from courses with `status: registered`; mark provisional ones "(provisional)" in the title; recurring weekly
  in the teaching weeks; never create clashes silently.
- Changed dates → update the event (ask first if it's a bulk change). Never delete events the agent didn't create.
