package edu.nd.crc.safa.server.entities.db;

/**
 * The type of activities occurring while parsing a project.
 */
public enum ProjectEntity {
    TIM {
        public String toString() {
            return "TIM";
        }
    },
    ARTIFACTS {
        public String toString() {
            return "ARTIFACTS";
        }
    },
    TRACES {
        public String toString() {
            return "TRACES";
        }
    }
}
