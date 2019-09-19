package edu.nd.crc.safa.models;

import java.util.List;

import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

@RepositoryRestResource
public interface HazardTreeRepository extends CrudRepository<HazardTree, Long> {

    List<HazardTree> findByName(@Param("name") String name);

}