package edu.nd.crc.safa.server.entities.app;

import edu.nd.crc.safa.server.entities.db.TraceLinkVersion;

/**
 * Contains the before and after of a trace link for some delta.
 */
public class ModifiedTraceLink {

    TraceLinkVersion before;
    TraceLinkVersion after;

    public ModifiedTraceLink() {
    }

    public ModifiedTraceLink(TraceLinkVersion before, TraceLinkVersion after) {
        this.before = before;
        this.after = after;
    }

    public TraceLinkVersion getBefore() {
        return before;
    }

    public void setBefore(TraceLinkVersion before) {
        this.before = before;
    }

    public TraceLinkVersion getAfter() {
        return after;
    }

    public void setAfter(TraceLinkVersion after) {
        this.after = after;
    }
}
