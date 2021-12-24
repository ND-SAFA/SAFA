package edu.nd.crc.safa.server.entities.app;

/**
 * Represents a generic modification done to some entity.
 *
 * @param <AppEntity> The application entity to be used.
 */
public class ModifiedEntity<AppEntity> {
    AppEntity before;
    AppEntity after;

    public ModifiedEntity(AppEntity before, AppEntity after) {
        this.before = before;
        this.after = after;
    }

    public AppEntity getBefore() {
        return before;
    }

    public void setBefore(AppEntity before) {
        this.before = before;
    }

    public AppEntity getAfter() {
        return after;
    }

    public void setAfter(AppEntity after) {
        this.after = after;
    }
}
