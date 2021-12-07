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

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.json.JSONObject;

/**
 * Responsible for storing parsing errors when
 * uploading projects.
 */
@Entity
@Table(name = "commit_error")
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
    ProjectParsingActivities applicationActivity;

    @Column(name = "file_name")
    String fileName;

    @Column(name = "line_number")
    Long lineNumber;

    @Column(name = "description", length = 500)
    String description;

    public CommitError() {
        this.applicationActivity = ProjectParsingActivities.UNKNOWN;
    }

    public CommitError(ProjectVersion projectVersion,
                       String description) {
        this();
        this.projectVersion = projectVersion;
        this.description = description;
    }

    public CommitError(ProjectVersion projectVersion,
                       String description,
                       ProjectParsingActivities projectParsingActivity) {
        this(projectVersion, description);
        this.applicationActivity = projectParsingActivity;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("id", this.id);
        json.put("description:", this.description);
        json.put("activity:", this.applicationActivity);
        return json.toString();
    }

    public String getErrorId() {
        return this.id.toString();
    }

    public ProjectParsingActivities getApplicationActivity() {
        return this.applicationActivity;
    }

    public void setApplicationActivity(ProjectParsingActivities applicationActivity) {
        this.applicationActivity = applicationActivity;
    }

    public String getDescription() {
        return this.description;
    }
}
