package edu.nd.crc.safa.features.jobs.logging.entities;

import java.sql.Timestamp;
import java.util.UUID;

import edu.nd.crc.safa.features.jobs.entities.db.JobDbEntity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

@Entity
@Table(name = "job_log_entry")
@Getter
@Setter
@ToString
@NoArgsConstructor
public class JobLogEntry {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.BINARY)
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
