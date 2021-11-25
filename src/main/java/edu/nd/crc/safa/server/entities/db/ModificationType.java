package edu.nd.crc.safa.server.entities.db;

import java.io.Serializable;

/**
 * The types of modifications possible for a project entity.
 */
public enum ModificationType implements Serializable {
    ADDED {
        public String toString() {
            return "added";
        }
    },
    MODIFIED {
        public String toString() {
            return "modified";
        }
    },
    REMOVED {
        public String toString() {
            return "removed";
        }
    }
}
