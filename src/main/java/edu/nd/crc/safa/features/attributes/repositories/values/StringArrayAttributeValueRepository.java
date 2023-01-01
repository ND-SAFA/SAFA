package edu.nd.crc.safa.features.attributes.repositories.values;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.values.ArtifactAttributeVersion;
import edu.nd.crc.safa.features.attributes.entities.db.values.StringArrayAttributeValue;

import org.springframework.data.repository.CrudRepository;

public interface StringArrayAttributeValueRepository extends CrudRepository<StringArrayAttributeValue, UUID> {
    List<StringArrayAttributeValue> getByAttributeVersion(ArtifactAttributeVersion attributeVersion);

    void deleteByAttributeVersion(ArtifactAttributeVersion attributeVersion);
}
