"use strict";
exports.__esModule = true;
exports.CommitBuilder = void 0;
var util_1 = require("@/util");
var store_1 = require("@/store");
var api_1 = require("@/api");
/**
 * Responsible for creating a commit and saving it to the database.
 */
var CommitBuilder = /** @class */ (function () {
    /**
     * Creates a commit builder.
     * @param version - The project version to commit to.
     */
    function CommitBuilder(version) {
        this.commit = util_1.createCommit(version);
    }
    /**
     * Adds a new artifact to this commit.
     *
     * @param artifact - The artifact to create.
     */
    CommitBuilder.prototype.withNewArtifact = function (artifact) {
        this.commit.artifacts.added.push(artifact);
        return this;
    };
    /**
     * Adds a modified artifact to this commit.
     *
     * @param artifact - The artifact to modify.
     */
    CommitBuilder.prototype.withModifiedArtifact = function (artifact) {
        this.commit.artifacts.modified.push(artifact);
        return this;
    };
    /**
     * Adds a removed artifact to this commit.
     *
     * @param artifact - The artifact to remove.
     */
    CommitBuilder.prototype.withRemovedArtifact = function (artifact) {
        this.commit.artifacts.removed.push(artifact);
        return this;
    };
    /**
     * Adds a new trace link to this commit.
     *
     * @param traceLink - The link to add.
     */
    CommitBuilder.prototype.withNewTraceLink = function (traceLink) {
        this.commit.traces.added.push(traceLink);
        return this;
    };
    /**
     * Adds a modified trace link to this commit.
     *
     * @param traceLink - The link to modify.
     */
    CommitBuilder.prototype.withModifiedTraceLink = function (traceLink) {
        this.commit.traces.modified.push(traceLink);
        return this;
    };
    /**
     * Saves this commit.
     */
    CommitBuilder.prototype.save = function () {
        return api_1.saveCommit(this.commit);
    };
    /**
     * Creates a new commit based on the current project version.
     */
    CommitBuilder.withCurrentVersion = function () {
        var projectVersion = store_1.projectModule.getProject.projectVersion;
        if (projectVersion === undefined) {
            throw Error("No project version is selected.");
        }
        return new CommitBuilder(projectVersion);
    };
    return CommitBuilder;
}());
exports.CommitBuilder = CommitBuilder;
