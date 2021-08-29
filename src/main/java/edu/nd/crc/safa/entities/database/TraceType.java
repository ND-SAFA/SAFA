package edu.nd.crc.safa.entities.database;

import java.io.Serializable;

/**
 * Responsible for enumerating the different ways traces
 * can be established.
 */
public enum TraceType implements Serializable {
    MANUAL,
    GENERATED
}
