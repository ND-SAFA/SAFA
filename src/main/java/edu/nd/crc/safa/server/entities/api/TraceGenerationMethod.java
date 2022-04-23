package edu.nd.crc.safa.server.entities.api;

/**
 * Enumerates all the different ways to generate trace links.
 */
public enum TraceGenerationMethod {
    VSM {
        public String toString() {
            return "VSM";
        }
    },
    BERT {
        public String toString() {
            return "BERT";
        }
    }
}
