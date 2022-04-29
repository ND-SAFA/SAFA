package edu.nd.crc.safa.server.entities.api;

/**
 * Respresents a request to perform a new job
 */
public class JobSubmission<T> {

    JobType jobType;
    T payload;

    public JobSubmission() {
    }

    public T getPayload() {
        return payload;
    }

    public void setPayload(T payload) {
        this.payload = payload;
    }

    public JobType getJobType() {
        return jobType;
    }

    public void setJobType(JobType jobType) {
        this.jobType = jobType;
    }
}
