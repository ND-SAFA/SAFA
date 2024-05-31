package edu.nd.crc.safa.features.attributes.repositories.definitions;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.definitions.CustomAttribute;

import org.springframework.data.domain.Sort;
import org.springframework.data.repository.CrudRepository;

public interface CustomAttributeRepository extends CrudRepository<CustomAttribute, UUID>  {

    Optional<CustomAttribute> findByProjectIdAndKeyname(UUID projectId, String keyname);

    List<CustomAttribute> findByProjectId(UUID projectId);

    List<CustomAttribute> findByProjectId(UUID projectId, Sort sort);

    boolean existsByProjectIdAndKeyname(UUID projectId, String keyname);

    void deleteByProjectIdAndKeyname(UUID projectId, String key);
}
