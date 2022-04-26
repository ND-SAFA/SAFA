package edu.nd.crc.safa.server.entities.api;

import java.util.ArrayList;
import java.util.List;

/**
 * Container for the possible changes that an entity could have
 * between two versions.
 *
 * @param <T> The type of entity that is changing.
 */
public class ProjectChange<T> {
    List<T> added;
    List<T> removed;
    List<T> modified;

    public ProjectChange() {
        this.added = new ArrayList<>();
        this.removed = new ArrayList<>();
        this.modified = new ArrayList<>();
    }

    public List<T> getAdded() {
        return added;
    }

    public void setAdded(List<T> added) {
        this.added = added;
    }

    public List<T> getRemoved() {
        return removed;
    }

    public void setRemoved(List<T> removed) {
        this.removed = removed;
    }

    public List<T> getModified() {
        return modified;
    }

    public void setModified(List<T> modified) {
        this.modified = modified;
    }

    public int getSize() {
        return this.added.size() + this.modified.size() + this.removed.size();
    }
}
