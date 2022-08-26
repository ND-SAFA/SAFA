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
    Map<UUID, E> added;
    Map<UUID, ModifiedEntity<E>> modified;
    Map<UUID, E> removed;
}
