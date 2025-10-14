package edu.nd.crc.safa.features.documents.entities.db;

import java.io.Serializable;
import java.util.UUID;

import edu.nd.crc.safa.features.projects.entities.db.Project;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.type.SqlTypes;

/**
 * Responsible for storing the unique documents present in a project.
 */
@Entity
@Table(name = "document")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Document implements Serializable {

    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.VARCHAR)
    @Column(name = "document_id")
    private UUID documentId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    @JsonIgnore
    private Project project;

    @Column(name = "name")
    private String name;

    @Column(name = "description")
    private String description;

    public Document(Document document) {
        this(document.documentId,
            document.project,
            document.name,
            document.description
        );
    }
}
