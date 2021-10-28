package edu.nd.crc.safa.server.db.entities.sql;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for storing the unique identifiers for artifacts
 * in a project.
 */
@Entity
@Table(name = "artifact",
    uniqueConstraints = {
        @UniqueConstraint(
            columnNames = {
                "project_id",
                "name"
            }, name = "UNIQUE_ARTIFACT_NAME_PER_PROJECT")
    })
public class Artifact implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "artifact_id")
    UUID artifactId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "type_id",
        nullable = false)
    ArtifactType type;

    @Column(name = "name")
    String name;

    public Artifact() {
    }

    public Artifact(Project project, ArtifactType type, String name) {
        setProject(project);
        setType(type);
        setName(name);
    }

    public Project getProject() {
        return this.project;
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public ArtifactType getType() {
        return this.type;
    }

    public void setType(ArtifactType artifactType) {
        this.type = artifactType;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getArtifactId() {
        return this.artifactId;
    }

    public String toString() {
        return String.format("{%s:%s}", this.name, this.type.getName());
    }
}
