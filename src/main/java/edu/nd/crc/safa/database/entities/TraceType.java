package edu.nd.crc.safa.database.entities;

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

/**
 * Responsible for enumerating the different ways traces
 * can be established. The reason this is an entire table
 * is too leave the naming flexible in case we ever want to
 * distinguish between algorithms or variants.
 */
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

    public TraceType() {
    }

    public TraceType(String traceTypeName) {
        this.traceTypeName = traceTypeName;
    }
}
