package edu.nd.crc.safa.repositories;

import java.util.UUID;

import edu.nd.crc.safa.entities.Layout;
import edu.nd.crc.safa.entities.Project;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LayoutRepository extends CrudRepository<Layout, UUID> {

    Layout findByProjectAndTreeId(Project project, String treeId);
}
