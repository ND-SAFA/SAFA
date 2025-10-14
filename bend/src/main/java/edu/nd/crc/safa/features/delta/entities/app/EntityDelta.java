package edu.nd.crc.safa.features.delta.entities.app;

import java.util.Map;
import java.util.UUID;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Contains the entity changes that can occur between two projects versions.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EntityDelta<E> {
    private Map<UUID, E> added;
    private Map<UUID, ModifiedEntity<E>> modified;
    private Map<UUID, E> removed;
}
