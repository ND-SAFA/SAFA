package edu.nd.crc.safa.features.attributes.repositories.layouts;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;
import edu.nd.crc.safa.features.attributes.entities.db.layouts.AttributeLayout;
import edu.nd.crc.safa.features.attributes.entities.db.layouts.AttributePosition;

import org.springframework.data.repository.CrudRepository;

public interface AttributePositionRepository extends CrudRepository<AttributePosition, UUID> {
    List<AttributePosition> findByLayout(AttributeLayout layout);

    Optional<AttributePosition> findByAttributeAndLayout(CustomAttribute attribute, AttributeLayout layout);

    void deleteByLayout(AttributeLayout layout);
}
