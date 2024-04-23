package edu.nd.crc.safa.features.chat.repositories;

import java.util.List;
import java.util.UUID;

import edu.nd.crc.safa.features.chat.entities.persistent.Chat;
import edu.nd.crc.safa.features.users.entities.db.SafaUser;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ChatRepository extends CrudRepository<Chat, UUID> {

    List<Chat> findByOwner(SafaUser owner);

}
