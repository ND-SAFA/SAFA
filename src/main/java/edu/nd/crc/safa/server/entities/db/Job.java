package edu.nd.crc.safa.server.entities.db;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.annotations.Type;

/**
 * Responsible for storing the information needed to create jobs.
 */
@Entity
@Table(name = "job")
public class Job {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "[COLUMN_NAME]")
    UUID jobId;
    @Column(name = "progress")
    double progress;
    @Column(name = "last_message")
    String lastMessage;

    public Job() {
    }

    public String getLastMessage() {
        return lastMessage;
    }

    public void setLastMessage(String lastMessage) {
        this.lastMessage = lastMessage;
    }

    public UUID getJobId() {
        return jobId;
    }

    public void setJobId(UUID jobId) {
        this.jobId = jobId;
    }

    public double getProgress() {
        return progress;
    }

    public void setProgress(double progress) {
        this.progress = progress;
    }
}
