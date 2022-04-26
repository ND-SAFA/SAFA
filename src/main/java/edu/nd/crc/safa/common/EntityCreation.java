package edu.nd.crc.safa.common;

import java.util.List;

/**
 * Contains a set of entities along with a series of errors associated with them.
 *
 * @param <EntityType> The type of entity contained.
 * @param <ErrorType>  The errors associated with entities.
 */
public class EntityCreation<EntityType, ErrorType> {

    List<EntityType> entities;
    List<ErrorType> errors;

    public EntityCreation(List<EntityType> entities, List<ErrorType> errors) {
        this.entities = entities;
        this.errors = errors;
    }

    public List<EntityType> getEntities() {
        return entities;
    }

    public void setEntities(List<EntityType> entities) {
        this.entities = entities;
    }

    public List<ErrorType> getErrors() {
        return errors;
    }

    public void setErrors(List<ErrorType> errors) {
        this.errors = errors;
    }
}
