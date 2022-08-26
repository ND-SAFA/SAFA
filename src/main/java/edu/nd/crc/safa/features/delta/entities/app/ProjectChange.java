package edu.nd.crc.safa.features.delta.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import javax.validation.Valid;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Container for the possible changes that an entity could have
 * between two versions.
 *
 * @param <T> The type of entity that is changing.
 */
@NoArgsConstructor
@Data
public class ProjectChange<T extends IAppEntity> {
    List<@Valid T> added = new ArrayList<>();
    List<@Valid T> removed = new ArrayList<>();
    List<@Valid T> modified = new ArrayList<>();

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

    @JsonIgnore
    public List<UUID> getUpdatedIds() {
        List<UUID> updatedArtifactIds = new ArrayList<>();
        updatedArtifactIds.addAll(getIds(this.getAdded()));
        updatedArtifactIds.addAll(getIds(this.getModified()));
        return updatedArtifactIds;
    }

    @JsonIgnore
    public List<UUID> getDeletedIds() {
        return getIds(this.getRemoved());
    }

    @JsonIgnore
    public List<UUID> getIds(List<T> entities) {
        return entities.stream().map(IAppEntity::getId).collect(Collectors.toList());
    }
}
