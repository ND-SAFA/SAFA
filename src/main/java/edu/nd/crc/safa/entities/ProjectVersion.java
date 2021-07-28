package edu.nd.crc.safa.entities;

import java.io.Serializable;

import javax.persistence.CascadeType;
import javax.persistence.Column;
import javax.persistence.ConstraintMode;
import javax.persistence.Entity;
import javax.persistence.ForeignKey;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

@Entity
@Table(name = "project_versions")
public class ProjectVersion implements Serializable {

    @Id
    @ManyToOne(cascade = CascadeType.REMOVE)
    @JoinColumn(
        name = "project_id",
        foreignKey = @ForeignKey(value = ConstraintMode.PROVIDER_DEFAULT),
        nullable = false
    )
    Project projectId;

    @Id
    @Column(name = "version_id")
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    String versionId; //todo: generate in sequence relative to project id using GenericGenerator
}
