package edu.nd.crc.safa.features.delta.entities.db;

import java.io.Serializable;

/**
 * The types of modifications possible for a project entity.
 */
public enum ModificationType implements Serializable {
    ADDED {
        public String toString() {
            return "ADDED";
        }
    },
    MODIFIED {
        public String toString() {
            return "MODIFIED";
        }
    },
    REMOVED {
        public String toString() {
            return "REMOVED";
        }
    },
    NO_MODIFICATION {
        public String toString() {
            return "NO_MODIFICATION";
        }
    }
}
