package edu.nd.crc.safa.features.models.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.models.entities.Model;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.repository.CrudRepository;

public interface ModelRepository extends CrudRepository<Model, UUID> {

    List<Model> findByProject(Project project);
}
