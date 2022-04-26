package edu.nd.crc.safa.server.entities.api;

import edu.nd.crc.safa.server.entities.db.Job;

/**
 * Responsible for describing the current status of a job.
 */
public class JobStatus {
    private String jobId;
    private double progress;
    private String message;

    public JobStatus() {

    }

    public JobStatus(String jobId, double progress, String message) {

    }

    public JobStatus(Job job, String message) {
        this.jobId = job.getJobId().toString();
        this.progress = job.getProgress();
        this.message = message;
    }

    public String getJobId() {
        return jobId;
    }

    public void setJobId(String jobId) {
        this.jobId = jobId;
    }

    public double getProgress() {
        return progress;
    }

    public void setProgress(double progress) {
        this.progress = progress;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

}
