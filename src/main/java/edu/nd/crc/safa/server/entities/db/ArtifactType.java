package edu.nd.crc.safa.server.entities.db;

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

import edu.nd.crc.safa.config.AppConstraints;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for defining which types are available
 * to which projects.
 */
@Entity
@Table(name = "artifact_type",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "project_id", "name"
        }, name = AppConstraints.UNIQUE_ARTIFACT_TYPE_PER_PROJECT)
    }
)
public class ArtifactType implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "type_id")
    UUID typeId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

    @Column(name = "name", nullable = false)
    String name;

    public ArtifactType() {
    }

    public ArtifactType(Project project, String name) {
        this.project = project;
        this.name = name.toLowerCase();
    }

    public String toString() {
        return this.name;
    }

    public UUID getTypeId() {
        return this.typeId;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name.toLowerCase();
    }

    public void setProject(Project project) {
        this.project = project;
    }

    public boolean equals(ArtifactType other) {
        return this.typeId.equals(other.typeId);
    }
}
