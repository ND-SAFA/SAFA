package edu.nd.crc.safa.features.errors.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.ProjectEntityType;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.Lob;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Responsible for storing parsing errors when
 * uploading projects.
 */
@Entity
@Table(name = "commit_error")
@Data
@NoArgsConstructor
public class CommitError implements Serializable {
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "id")
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "version_id", nullable = false)
    private ProjectVersion projectVersion;

    @Column(name = "activity")
    @JdbcTypeCode(SqlTypes.INTEGER)
    @Enumerated(EnumType.ORDINAL)
    private ProjectEntityType applicationActivity;

    @Column(name = "file_name")
    private String fileName;

    @Column(name = "line_number")
    private Long lineNumber;

    @Column(name = "description", columnDefinition = "mediumtext")
    @Lob
    private String description;

    public CommitError(ProjectVersion projectVersion,
                       String description,
                       ProjectEntityType projectParsingActivity) {
        this();
        this.projectVersion = projectVersion;
        this.description = description;
        this.applicationActivity = projectParsingActivity;
    }

    @JsonIgnore
    public String getErrorId() {
        return this.id.toString();
    }
}
