package edu.nd.crc.safa.entities.database;

import java.util.UUID;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import org.hibernate.annotations.OnDelete;
import org.hibernate.annotations.OnDeleteAction;
import org.hibernate.annotations.Type;

@Entity
@Table(name = "warnings")
public class Warning {

    @Id
    @GeneratedValue
    @Type(type = "uuid-char")
    @Column(name = "warning_id")
    UUID warningId;

    @ManyToOne
    @OnDelete(action = OnDeleteAction.CASCADE)
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
