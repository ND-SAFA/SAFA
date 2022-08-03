package edu.nd.crc.safa.server.entities.db;

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
    UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "version_id", nullable = false)
    ProjectVersion projectVersion;

    @Column(name = "activity")
    @Enumerated(EnumType.ORDINAL)
    ProjectEntity applicationActivity;

    @Column(name = "file_name")
    String fileName;

    @Column(name = "line_number")
    Long lineNumber;

    @Column(name = "description", length = 500)
    String description;

    public CommitError(ProjectVersion projectVersion,
                       String description,
                       ProjectEntity projectParsingActivity) {
        this();
        this.projectVersion = projectVersion;
        this.description = description;
        this.applicationActivity = projectParsingActivity;
    }

    public String getErrorId() {
        return this.id.toString();
    }
}
