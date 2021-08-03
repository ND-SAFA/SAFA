package edu.nd.crc.safa.database.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
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

    @Column(name = "activity")
    @Enumerated(EnumType.ORDINAL)
    ApplicationActivity activity;

    @Column(name = "file_name")
    String fileName;

    @Column(name = "line_number")
    Long lineNumber;

    @Column(name = "description")
    String description;

    public ParserError() {
        this.activity = ApplicationActivity.UNKNOWN;
    }

    public ParserError(Project project,
                       String fileName,
                       Long lineNumber,
                       String description,
                       ApplicationActivity activity) {
        this();
        this.project = project;
        this.fileName = fileName;
        this.lineNumber = lineNumber;
        this.description = description;
        this.activity = activity;
    }

    public String toLogFormat() {
        String entry = "";

        entry += "File: " + this.fileName + "\n";
        entry += "Line: " + (this.lineNumber != null ? this.lineNumber : "unknown") + "\n";
        entry += "Description: " + this.description + "\n";
        return entry;
    }

    public ApplicationActivity getActivity() {
        return this.activity;
    }
}
