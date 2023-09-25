package edu.nd.crc.safa.utilities;

import java.util.ArrayList;
import java.util.List;

import lombok.AccessLevel;
import lombok.NoArgsConstructor;
import org.springframework.data.repository.CrudRepository;

/**
 * Implements utility methods in a compositional manner.
 */
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class GeneralRepositoryUtility {

    /**
     * Returns the entities whose ID is contained in list.
     *
     * @param entityIds  List of entity IDs.
     * @param repository The repository used to get iterable.
     * @param <T>        The type of entities being returned.
     * @param <TID>      The type of ID for the entities.
     * @return The list of entities.
     */
    public static <T, TID> List<T> getByIds(List<TID> entityIds, CrudRepository<T, TID> repository) {
        List<T> entities = new ArrayList<>();
        repository.findAllById(entityIds).forEach(entities::add);
        return entities;
    }
}
