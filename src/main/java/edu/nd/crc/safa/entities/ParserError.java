package edu.nd.crc.safa.entities;

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
}
