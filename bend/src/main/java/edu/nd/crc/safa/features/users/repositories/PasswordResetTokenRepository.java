package edu.nd.crc.safa.features.users.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.PasswordResetToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PasswordResetTokenRepository extends JpaRepository<PasswordResetToken, UUID> {

    Optional<PasswordResetToken> findByToken(String token);

    void deleteByUser(SafaUser user);
}
