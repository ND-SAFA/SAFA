package edu.nd.crc.safa.entities;

import java.util.UUID;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "warnings")
public class Warning {

    @Id
    @Column
    @GeneratedValue
    UUID warningId;

    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id",
        nullable = false
    )
    Project project;

    @Column
    String nShort;

    @Column
    String nLong;

    @Column
    String rule;

    public Warning(Project project, String nShort, String nLong, String rule) {
        this.project = project;
        this.nShort = nShort;
        this.nLong = nLong;
        this.rule = rule;
    }

    public String getNShort() {
        return this.nShort;
    }

    public String getNLong() {
        return this.nLong;
    }

    public String getRule() {
        return this.rule;
    }
}
