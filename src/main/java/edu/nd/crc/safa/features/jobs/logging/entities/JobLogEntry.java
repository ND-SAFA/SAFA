package edu.nd.crc.safa.features.jobs.logging.entities;

import java.sql.Timestamp;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.Lob;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;

@Entity
@Table(name = "job_log_entry")
@Getter
@Setter
@ToString
@NoArgsConstructor
public class JobLogEntry {

    @Id
    @GeneratedValue
    @Column
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "job_id", nullable = false)
    private JobDbEntity job;

    @Column
    private short stepNum;

    @Column
    private Timestamp timestamp;

    @Lob
    @Column(columnDefinition = "mediumtext")
    private String entry;

    public JobLogEntry(JobDbEntity job, short stepNum, Timestamp timestamp, String entry) {
        this.job = job;
        this.stepNum = stepNum;
        this.timestamp = timestamp;
        this.entry = entry;
    }
}
