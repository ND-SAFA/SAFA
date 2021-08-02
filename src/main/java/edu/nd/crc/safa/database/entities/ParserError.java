package edu.nd.crc.safa.database.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

/**
 * Responsible for storing parsing errors when
 * uploading projects.
 */
@Entity
@Table(name = "parse_errors")
public class ParserError implements Serializable {
    @Id
    @GeneratedValue
    @Column(name = "id")
    UUID id;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(name = "project_id", nullable = false)
    Project project;

    @Column(name = "file_name")
    String fileName;

    @Column(name = "line_number")
    Long lineNumber;

    @Column(name = "description")
    String description;

    public ParserError() {
    }

    public ParserError(Project project,
                       String fileName,
                       Long lineNumber,
                       String description) {
        this.project = project;
        this.fileName = fileName;
        this.lineNumber = lineNumber;
        this.description = description;
    }
}
