package edu.nd.crc.safa.server.db.entities.sql;

import java.io.Serializable;

/**
 * Responsible for enumerating the different ways traces
 * can be established.
 */
public enum TraceType implements Serializable {
    MANUAL {
        public String toString() {
            return "MANUAL";
        }
    },
    GENERATED {
        public String toString() {
            return "GENERATED";
        }
    }
}
