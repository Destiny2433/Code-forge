# CodeForge Task Tracker

## Completed in this pass

- [x] Add a direct first-lesson action to the course page for signed-in and guest learners.
- [x] Show per-module and per-lesson completion status from saved user progress.
- [x] Include the CSRF token in lesson-completion requests.
- [x] Save lesson progress once and move to the next lesson after successful completion.
- [x] Send guests to sign in and return them to the lesson when they try to save progress.
- [x] Add Ctrl/Cmd+Enter as a shortcut for checking lesson code.
- [x] Add error feedback and retry behavior when progress cannot be saved.
- [x] Add an eight-lesson HTML-from-scratch sequence covering elements, headings, paragraphs, links, images, lists, and semantics.
- [x] Replace the generic first HTML lesson with meaningful checks and progressive hints.
- [x] Fix live preview using iframe srcdoc to avoid cross-origin browser errors.
- [x] Collapse the tutor initially so it does not block lesson controls.
- [x] Make startup seed new lessons additively without deleting existing accounts or progress.

## Verification still required

- [ ] Install project requirements into the workspace virtual environment.
- [x] Run the Flask app and confirm course and lesson routes render with the updated curriculum.
- [x] Test lesson checks and first-to-next navigation in a browser.
- [ ] Finish verifying saved progress display after sign-in.
- [ ] Confirm the existing local database contains the latest curriculum seed.
- [ ] Run the project's automated tests, if available.

## Product identity

- Product: CodeForge
- Company: HiveryTech
- Learning experience: original, beginner-friendly web development lessons with clear progression.

## Notes

Do not mark runtime or browser validation complete until it has actually been run successfully. Preserve learner progress when updating existing course data.
