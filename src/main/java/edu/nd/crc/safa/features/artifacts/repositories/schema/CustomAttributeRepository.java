package edu.nd.crc.safa.features.artifacts.repositories.schema;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.artifacts.entities.db.schema.CustomAttribute;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.repository.CrudRepository;

public interface CustomAttributeRepository extends CrudRepository<CustomAttribute, UUID>  {

    Optional<CustomAttribute> findByProjectAndKeyname(Project project, String keyname);

    List<CustomAttribute> findByProject(Project project);

    boolean existsByProjectAndKeyname(Project project, String keyname);

    void deleteByProjectAndKeyname(Project project, String key);
}
