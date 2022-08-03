package edu.nd.crc.safa.features.delta.entities.app;

/**
 * Represents a generic modification done to some entity.
 *
 * @param <A> The application entity to be used.
 */
public class ModifiedEntity<A> {
    A before;
    A after;

    public ModifiedEntity(A before, A after) {
        this.before = before;
        this.after = after;
    }

    public A getBefore() {
        return before;
    }

    public void setBefore(A before) {
        this.before = before;
    }

    public A getAfter() {
        return after;
    }

    public void setAfter(A after) {
        this.after = after;
    }
}
