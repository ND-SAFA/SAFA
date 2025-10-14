package edu.nd.crc.safa.features.traces.entities.db;

import java.io.Serializable;

import lombok.AllArgsConstructor;

/**
 * The state of approving a trace links for trace links. Note,
 * manual links are defaulted to be approved.
 */
@AllArgsConstructor
public enum ApprovalStatus implements Serializable {
    /**
     * The state of a generated trace link that has not been
     * approved or declined.
     */
    UNREVIEWED("unreviewed"),
    /**
     * The state of a generated trace link that has been
     * marked as valid by an analyst.
     */
    APPROVED("approved"),
    /**
     * The state of a generated trace link that has been
     * marked by an analyst.
     */
    DECLINED("declined");

    private final String value;

    @Override
    public String toString() {
        return this.value;
    }
}
