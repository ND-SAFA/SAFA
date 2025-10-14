package edu.nd.crc.safa.features.delta.entities.app;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.function.Predicate;
import java.util.stream.Collectors;

import edu.nd.crc.safa.features.projects.entities.app.IAppEntity;
import edu.nd.crc.safa.utilities.StringUtil;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.validation.Valid;
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
    private List<@Valid T> added = new ArrayList<>();
    private List<@Valid T> removed = new ArrayList<>();
    private List<@Valid T> modified = new ArrayList<>();

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
    public List<UUID> getEntityIds() {
        List<UUID> entityIds = new ArrayList<>();
        entityIds.addAll(getUpdatedIds());
        entityIds.addAll(getDeletedIds());
        return entityIds;
    }

    @JsonIgnore
    public List<UUID> getUpdatedIds() {
        return getIds(this.getModified());
    }

    @JsonIgnore
    public List<UUID> getAddedIds() {
        return getIds(this.getAdded());
    }

    @JsonIgnore
    public List<UUID> getDeletedIds() {
        return getIds(this.getRemoved());
    }

    @JsonIgnore
    public List<UUID> getIds(List<T> entities) {
        return entities.stream().map(IAppEntity::getId).collect(Collectors.toList());
    }

    /**
     * Returns human-readable summary of changes.
     *
     * @param entityName The name of the entities being changed.
     * @return String noting the changes.
     */
    public String getSummary(String entityName) {
        List<String> summaries = new ArrayList<>();
        List<List<T>> entities = List.of(getRemoved(), getAdded(), getModified());
        List<String> labels = List.of("removed", "added", "modified");

        for (int i = 0; i < entities.size(); i++) {
            int size = entities.get(i).size();
            String label = labels.get(i);
            if (size > 0) {
                summaries.add(String.format("%s %s %s.", entityName, size, label));
            }
        }
        return StringUtil.join(summaries, "\n");
    }
}
