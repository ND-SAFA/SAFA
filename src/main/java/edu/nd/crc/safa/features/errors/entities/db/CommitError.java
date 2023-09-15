package edu.nd.crc.safa.features.errors.entities.db;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import edu.nd.crc.safa.features.projects.entities.db.ProjectEntity;
import edu.nd.crc.safa.features.versions.entities.ProjectVersion;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

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
    @Type(type = "uuid-char")
    @Column(name = "id")
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "version_id", nullable = false)
    private ProjectVersion projectVersion;

    @Column(name = "activity")
    @Enumerated(EnumType.ORDINAL)
    private ProjectEntity applicationActivity;

    @Column(name = "file_name")
    private String fileName;

    @Column(name = "line_number")
    private Long lineNumber;

    @Column(name = "description", length = 500)
    private String description;

    public CommitError(ProjectVersion projectVersion,
                       String description,
                       ProjectEntity projectParsingActivity) {
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
