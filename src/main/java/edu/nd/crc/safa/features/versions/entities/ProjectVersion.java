package edu.nd.crc.safa.features.versions.entities;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.config.AppConstraints;
import edu.nd.crc.safa.features.organizations.entities.db.IEntityWithMembership;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.PositiveOrZero;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Identifies each project's version.
 */
@Entity
@Table(name = "project_version",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "project_id", "major_version", "minor_version", "revision"
        }, name = AppConstraints.UNIQUE_VERSION_ID_PER_PROJECT)
    }
)
@Data
@NoArgsConstructor
public class ProjectVersion implements Serializable, IEntityWithMembership {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "version_id")
    @NotNull
    private UUID versionId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_id", nullable = false)
    @JsonIgnore
    private Project project;

    @NotNull
    @Positive
    @Column(name = "major_version", nullable = false)
    private int majorVersion;

    @NotNull
    @PositiveOrZero
    @Column(name = "minor_version", nullable = false)
    private int minorVersion;

    @NotNull
    @PositiveOrZero
    @Column(name = "revision", nullable = false)
    private int revision;

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
        return this.isLessThan(other) || this.isEqualTo(other);
    }

    public boolean isLessThan(ProjectVersion other) {
        if (this.majorVersion < other.majorVersion) {
            return true;
        } else if (other.majorVersion == this.majorVersion) {
            if (this.minorVersion < other.minorVersion) {
                return true;
            } else if (other.minorVersion == this.minorVersion) {
                return this.revision < other.revision;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    public boolean isEqualTo(ProjectVersion other) {
        return this.majorVersion == other.majorVersion
            && this.minorVersion == other.minorVersion
            && this.revision == other.revision;
    }

    public boolean isGreaterThan(ProjectVersion other) {
        return !this.isLessThanOrEqualTo(other);
    }

    public String toString() {
        return String.format("%s.%s.%s", majorVersion, minorVersion, revision);
    }

    @Override
    @JsonIgnore
    public UUID getId() {
        return versionId;
    }
}
