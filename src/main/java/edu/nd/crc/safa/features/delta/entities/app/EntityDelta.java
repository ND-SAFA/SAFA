package edu.nd.crc.safa.features.delta.entities.app;

import java.util.Map;

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
    Map<String, E> added;
    Map<String, ModifiedEntity<E>> modified;
    Map<String, E> removed;
}
