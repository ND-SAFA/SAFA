package edu.nd.crc.safa.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

@Entity
@Table(name = "trace_type")
public class TraceType implements Serializable {

    @Id
    @GeneratedValue
    @Column(name = "trace_type_id")
    UUID traceTypeId;

    @Column(name = "name")
    String traceTypeName;

    public void setName(String name) {
        this.traceTypeName = name.toLowerCase();
    }

}
