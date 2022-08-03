package edu.nd.crc.safa.common;

import java.util.ArrayList;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Contains a set of entities along with a series of errors associated with them.
 *
 * @param <E> The type of entity contained.
 * @param <M> The errors associated with entities.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class EntityParsingResult<E, M> {

    List<E> entities = new ArrayList<>();
    List<M> errors = new ArrayList<>();
}
