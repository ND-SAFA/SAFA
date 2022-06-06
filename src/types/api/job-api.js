"use strict";
exports.__esModule = true;
exports.JobStatus = exports.JobType = void 0;
/**
 * Enumerates the jobs that can be performed
 */
var JobType;
(function (JobType) {
    /**
     * Parsing and uploading entities via flat files.
     */
    JobType["FLAT_FILE_PROJECT_CREATION"] = "FLAT_FILE_PROJECT_CREATION";
    /**
     * Scraping and uploading entities from a JIRA project.
     */
    JobType["JIRA_PROJECT_CREATION"] = "JIRA_PROJECT_CREATION";
    /**
     * Creating a project via JSON.
     */
    JobType["PROJECT_CREATION"] = "PROJECT_CREATION";
    /**
     * Updating changed entities from jira projects
     */
    JobType["PROJECT_SYNC"] = "PROJECT_SYNC";
    /**
     * Generating set of trace links.
     */
    JobType["GENERATE_LINKS"] = "GENERATE_LINKS";
    /**
     * Training Bert model for trace link prediction on some domain.
     */
    JobType["TRAIN_MODEL"] = "TRAIN_MODEL";
})(JobType = exports.JobType || (exports.JobType = {}));
/**
 * The state a job can be in.
 */
var JobStatus;
(function (JobStatus) {
    /**
     * The job is being performed as expected.
     */
    JobStatus["IN_PROGRESS"] = "IN_PROGRESS";
    /**
     * The job has finished.
     */
    JobStatus["COMPLETED"] = "COMPLETED";
    /**
     * The job has been cancelled.
     */
    JobStatus["CANCELLED"] = "CANCELLED";
    /**
     * The job has failed.
     */
    JobStatus["FAILED"] = "FAILED";
})(JobStatus = exports.JobStatus || (exports.JobStatus = {}));
