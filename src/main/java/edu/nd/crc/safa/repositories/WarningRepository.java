package edu.nd.crc.safa.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.entities.Project;
import edu.nd.crc.safa.entities.Warning;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface WarningRepository extends CrudRepository<Warning, UUID> {

    List<Warning> findAllByProject(Project project);
}
