package edu.nd.crc.safa.entities.database;

import java.io.Serializable;
import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for storing the unique identifiers for artifacts
 * in a project.
 */
@Entity
@Table(name = "artifacts")
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
}
