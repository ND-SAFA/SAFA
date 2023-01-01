package edu.nd.crc.safa.features.attributes.repositories.definitions;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.definitions.SelectionAttributeOption;

import org.springframework.data.repository.CrudRepository;

public interface SelectionAttributeOptionRepository extends CrudRepository<SelectionAttributeOption, UUID> {
    List<SelectionAttributeOption> findByAttribute(CustomAttribute attribute);

    void deleteByAttribute(CustomAttribute attribute);
}
