package edu.nd.crc.safa.features.attributes.repositories.layouts;

import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.layouts.AttributeLayout;

import org.springframework.data.repository.CrudRepository;

public interface AttributeLayoutRepository extends CrudRepository<AttributeLayout, UUID> {
}
