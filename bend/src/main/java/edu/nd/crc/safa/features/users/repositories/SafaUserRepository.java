package edu.nd.crc.safa.features.users.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface SafaUserRepository extends CrudRepository<SafaUser, UUID> {

    Optional<SafaUser> findByEmail(String email);
}
