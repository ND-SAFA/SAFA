package edu.nd.crc.safa.features.documents.entities.db;

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

import edu.nd.crc.safa.features.projects.entities.db.Project;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for storing the unique documents present in a project.
 */
@Entity
@Table(name = "document")
@Data
@NoArgsConstructor
public class Document implements Serializable {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "document_id")
    UUID documentId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    @JsonIgnore
    Project project;

    @Column(name = "document_type", nullable = false)
    @Enumerated(EnumType.STRING)
    DocumentType type;

    @Column(name = "name")
    String name;

    @Column(name = "description")
    String description;

    public Document(Document document) {
        this(document.project,
            document.name,
            document.description,
            document.type);
        this.documentId = document.getDocumentId();
    }

    public Document(Project project, String name, String description, DocumentType type) {
        this.project = project;
        this.name = name;
        this.description = description;
        this.type = type;
    }
}
