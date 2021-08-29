package edu.nd.crc.safa.entities.database;

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

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

/**
 * Responsible for storing parsing errors when
 * uploading projects.
 */
@Entity
@Table(name = "parse_errors")
public class ParserError implements Serializable {
    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "id")
    UUID id;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
    @JoinColumn(name = "version_id", nullable = false)
    ProjectVersion projectVersion;

    @Column(name = "activity")
    @Enumerated(EnumType.ORDINAL)
    ApplicationActivity applicationActivity;

    @Column(name = "file_name")
    String fileName;

    @Column(name = "line_number")
    Long lineNumber;

    @Column(name = "description")
    String description;

    public ParserError() {
        this.applicationActivity = ApplicationActivity.UNKNOWN;
    }

    public ParserError(ProjectVersion projectVersion,
                       String fileName,
                       Long lineNumber,
                       String description,
                       ApplicationActivity applicationActivity) {
        this();
        this.projectVersion = projectVersion;
        this.fileName = fileName;
        this.lineNumber = lineNumber;
        this.description = description;
        this.applicationActivity = applicationActivity;
    }

    public String toLogFormat() {
        String entry = "";

        entry += "File: " + this.fileName + "\n";
        entry += "Line: " + (this.lineNumber != null ? this.lineNumber : "unknown") + "\n";
        entry += "Description: " + this.description + "\n";
        return entry;
    }

    public String getErrorId() {
        return this.id.toString();
    }

    public ApplicationActivity getApplicationActivity() {
        return this.applicationActivity;
    }

    public String getFileName() {
        return this.fileName;
    }

    public String getDescription() {
        return this.description;
    }
}
