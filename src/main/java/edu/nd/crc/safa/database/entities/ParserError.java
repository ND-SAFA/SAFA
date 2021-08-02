package edu.nd.crc.safa.database.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "parse_errors")
public class ParserError implements Serializable {
    @Id
    @GeneratedValue
    @Column(name = "id")
    UUID id;

    @Column(name = "file_name")
    String fileName;

    @Column(name = "line")
    String line;

    @Column(name = "description")
    String description;

    public ParserError() {
    }

    public ParserError(String fileName,
                       String line,
                       String description) {
        this.fileName = fileName;
        this.line = line;
        this.description = description;
    }
}
