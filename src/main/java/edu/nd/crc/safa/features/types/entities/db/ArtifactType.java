package edu.nd.crc.safa.features.types.entities.db;

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
import edu.nd.crc.safa.config.DefaultArtifactTypeIcons;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for defining which types are available
 * to which projects.
 */
@Entity
@Data
@Table(name = "artifact_type",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "project_id", "name"
        }, name = AppConstraints.UNIQUE_ARTIFACT_TYPE_PER_PROJECT)
    }
)
@NoArgsConstructor
public class ArtifactType implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "id")
    private UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    @JsonIgnore
    private Project project;

    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "icon", nullable = false)
    private String icon;

    @Column(name = "color", nullable = false)
    private String color;

    public ArtifactType(Project project, String name, String color) {
        this.project = project;
        this.name = name;
        this.icon = DefaultArtifactTypeIcons.getArtifactIcon(name);
        this.color = color;
    }

    @Override
    public String toString() {
        return this.name;
    }
}
