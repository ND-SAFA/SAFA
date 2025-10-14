ALTER TABLE github_project
    ADD COLUMN last_update datetime NOT NULL DEFAULT NOW();