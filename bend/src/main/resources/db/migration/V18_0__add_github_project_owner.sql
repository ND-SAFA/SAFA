/*
    Wipe github_project table since we cannot figure out what the owner should have been.
    The only reference to a user is through the project object by looking at the project
    owner, but that is not necessarily the person who added the integration.

    Plus, this feature hasn't been flushed out yet, so it will just be a couple of developers who
    have to reimport things.
*/
DELETE FROM github_project;

ALTER TABLE github_project
    ADD COLUMN owner VARCHAR(255) NOT NULL DEFAULT '';