package edu.nd.crc.safa.features.users.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.PasswordResetToken;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PasswordResetTokenRepository extends CrudRepository<PasswordResetToken, UUID> {

    Optional<PasswordResetToken> findByToken(String token);
}
