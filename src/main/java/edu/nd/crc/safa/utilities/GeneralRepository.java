package edu.nd.crc.safa.utilities;

import java.util.ArrayList;
import java.util.List;

import org.springframework.data.repository.CrudRepository;

public interface GeneralRepository<T, TID> extends CrudRepository<T, TID> {

    default List<T> getByIds(List<TID> entityIds) {
        List<T> entities = new ArrayList<>();
        findAllById(entityIds).forEach(entities::add);
        return entities;
    }
}
