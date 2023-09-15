package edu.nd.crc.safa.features.delta.entities.app;

import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * Represents a generic modification done to some entity.
 *
 * @param <A> The application entity to be used.
 */
@Data
@AllArgsConstructor
public class ModifiedEntity<A> {
    private A before;
    private A after;
}
