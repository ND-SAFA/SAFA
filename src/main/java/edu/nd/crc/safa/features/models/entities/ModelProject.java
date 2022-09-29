package edu.nd.crc.safa.features.models.entities;

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
import edu.nd.crc.safa.features.projects.entities.db.Project;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Represents the database entity for a trace generation model
 */
@Entity
@Table(name = "model_project",
    uniqueConstraints = {
        @UniqueConstraint(columnNames = {
            "model_id", "project_id"
        }, name = AppConstraints.UNIQUE_MODEL_PROJECT_RECORD)
    })
@Getter
@Setter
@NoArgsConstructor
public class ModelProject {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column
    UUID id;
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "model_id", nullable = false, unique = true)
    Model model;
    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "project_id", nullable = false, unique = true)
    Project project;

    public ModelProject(Model model, Project project) {
        this.model = model;
        this.project = project;
    }
}
