---
name: trip-planner
description: Plan weekend and holiday trips from London — when you're free, itineraries, prices, entry rules, bookings (only with approval). Use for "plan a weekend in X", "find cheap flights", "book this".
---
# Trip planner
1. Free windows: avoid class days in `courses.json`, exam period, mandatory dates in `deadlines.json`. Host schools warn
   against travel during teaching weeks with provisional timetables.
2. Options: rail (Eurostar, National Rail), flights, coaches; compare total door-to-door time and cost in USD. Check live
   prices on official sites; prices change — cite time of check.
3. Entry: Schengen 90/180-day rule and EU EES/ETIAS status for the user's passport — check live official sources.
4. Booking: only if `preferences.allow_booking` is true. Show the exact booking (who, what, dates, fare rules, total) and
   wait for "yes, book it". Use saved payment or password-manager card fill — never type card numbers. Record in
   `bookings.json` and expenses; add to calendar if the user wants.
