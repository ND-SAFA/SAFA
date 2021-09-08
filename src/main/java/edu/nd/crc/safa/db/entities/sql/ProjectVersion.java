package edu.nd.crc.safa.db.entities.sql;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.ConstraintMode;
import javax.persistence.Entity;
import javax.persistence.ForeignKey;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;
import org.json.JSONObject;

/**
 * Responsible for identifying each project's version.
 */
@Entity
@Table(name = "project_version",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "project_id", "major_version", "minor_version", "revision"
        })
    }
)
public class ProjectVersion implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "version_id")
    UUID versionId; //todo: generate in sequence relative to project id using GenericGenerator

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        foreignKey = @ForeignKey(value = ConstraintMode.PROVIDER_DEFAULT),
        nullable = false
    )
    Project project;

    @Column(name = "major_version", nullable = false)
    int majorVersion;

    @Column(name = "minor_version", nullable = false)
    int minorVersion;

    @Column(name = "revision", nullable = false)
    int revision;

    public ProjectVersion() {
    }

    public ProjectVersion(Project project,
                          int majorVersion,
                          int minorVersion,
                          int revision) {
        this.majorVersion = majorVersion;
        this.minorVersion = minorVersion;
        this.revision = revision;
        this.project = project;
    }

    public boolean isLessThanOrEqualTo(ProjectVersion other) {
        if (this.majorVersion < other.majorVersion) {
            return true;
        } else if (other.majorVersion == this.majorVersion) {
            if (this.minorVersion < other.minorVersion) {
                return true;
            } else if (other.minorVersion == this.minorVersion) {
                return this.revision <= other.revision;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    public Project getProject() {
        return this.project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public UUID getVersionId() {
        return this.versionId;
    }

    public void setVersionId(UUID versionId) {
        this.versionId = versionId;
    }

    public int getMajorVersion() {
        return this.majorVersion;
    }

    public void setMajorVersion(int majorVersion) {
        this.majorVersion = majorVersion;
    }

    public int getMinorVersion() {
        return this.minorVersion;
    }

    public void setMinorVersion(int minorVersion) {
        this.minorVersion = minorVersion;
    }

    public int getRevision() {
        return this.revision;
    }

    public void setRevision(int revision) {
        this.revision = revision;
    }

    public String toString() {
        JSONObject json = new JSONObject();
        json.put("majorVersion", majorVersion);
        json.put("minorVersion", minorVersion);
        json.put("revision", revision);
        json.put("project", project);
        return json.toString();
    }
}
