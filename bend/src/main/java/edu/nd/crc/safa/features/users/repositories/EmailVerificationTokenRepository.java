package edu.nd.crc.safa.features.users.repositories;

import java.util.Optional;
import java.util.UUID;

import edu.nd.crc.safa.features.users.entities.db.EmailVerificationToken;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EmailVerificationTokenRepository extends JpaRepository<EmailVerificationToken, UUID> {

    Optional<EmailVerificationToken> findByToken(String token);

    void deleteByUser(SafaUser user);

    EmailVerificationToken findByUserUserId(UUID id);
}
