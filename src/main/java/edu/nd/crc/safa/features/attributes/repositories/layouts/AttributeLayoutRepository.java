package edu.nd.crc.safa.features.attributes.repositories.layouts;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.attributes.entities.db.layouts.AttributeLayout;
import edu.nd.crc.safa.features.projects.entities.db.Project;

import org.springframework.data.repository.CrudRepository;

public interface AttributeLayoutRepository extends CrudRepository<AttributeLayout, UUID> {
    List<AttributeLayout> findByProject(Project project);
}
