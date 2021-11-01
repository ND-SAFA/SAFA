package edu.nd.crc.safa.server.entities.db;

import java.io.Serializable;

public enum TraceApproval implements Serializable {
    UNREVIEWED {
        public String toString() {
            return "unreviewed";
        }
    },
    APPROVED {
        public String toString() {
            return "approved";
        }
    },
    DECLINED {
        public String toString() {
            return "declined";
        }
    }
}
