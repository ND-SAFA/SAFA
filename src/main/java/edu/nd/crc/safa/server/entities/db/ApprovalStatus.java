package edu.nd.crc.safa.server.entities.db;

import java.io.Serializable;

/**
 * The state of approving a trace links for trace links. Note,
 * manual links are defaulted to be approved.
 */
public enum ApprovalStatus implements Serializable {
    /**
     * The state of a generated trace link that has not been
     * approved or declined.
     */
    UNREVIEWED {
        public String toString() {
            return "unreviewed";
        }
    },
    /**
     * The state of a generated trace link that has been
     * marked as valid by an analyst.
     */
    APPROVED {
        public String toString() {
            return "approved";
        }
    },
    /**
     * The state of a generated trace link that has been
     * marked by an analyst.
     */
    DECLINED {
        public String toString() {
            return "declined";
        }
    }
}
