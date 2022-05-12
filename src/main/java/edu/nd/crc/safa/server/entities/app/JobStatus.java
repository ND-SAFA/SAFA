package edu.nd.crc.safa.server.entities.app;

/**
 * Enumerates the states a job can be found in.
 */
public enum JobStatus {
    IN_PROGRESS {
        public String toString() {
            return "IN_PROGRESS";
        }
    },
    COMPLETED {
        public String toString() {
            return "COMPLETED";
        }
    },
    CANCELLED {
        public String toString() {
            return "CANCELLED";
        }
    },
    FAILED {
        public String toString() {
            return "FAILED";
        }
    }
}
