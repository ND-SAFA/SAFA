package edu.nd.crc.safa.features.artifacts.repositories.schema;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.ArtifactSchemaField;
import edu.nd.crc.safa.features.artifacts.entities.db.schema.SelectionFieldOption;

import org.springframework.data.repository.CrudRepository;

public interface SelectionFieldOptionRepository extends CrudRepository<SelectionFieldOption, UUID> {
    List<SelectionFieldOption> findBySchemaField(ArtifactSchemaField schemaField);
}
