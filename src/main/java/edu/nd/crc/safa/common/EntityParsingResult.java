package edu.nd.crc.safa.common;

import java.util.ArrayList;
import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Contains a set of entities along with a series of errors associated with them.
 *
 * @param <Entity> The type of entity contained.
 * @param <Error>  The errors associated with entities.
 */
@NoArgsConstructor
@AllArgsConstructor
@Data
public class EntityParsingResult<Entity, Error> {
    List<Entity> entities = new ArrayList<>();
    List<Error> errors = new ArrayList<>();
}
