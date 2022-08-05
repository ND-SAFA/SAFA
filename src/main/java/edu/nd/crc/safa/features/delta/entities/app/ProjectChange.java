package edu.nd.crc.safa.features.delta.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import com.fasterxml.jackson.annotation.JsonIgnore;

/**
 * Container for the possible changes that an entity could have
 * between two versions.
 *
 * @param <T> The type of entity that is changing.
 */
public class ProjectChange<T extends IAppEntity> {
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

    @JsonIgnore
    public int getSize() {
        return this.added.size() + this.modified.size() + this.removed.size();
    }

    public T filterAdded(Predicate<T> filter) {
        return this.added
            .stream()
            .filter(filter)
            .collect(Collectors.toList())
            .get(0);
    }
}
