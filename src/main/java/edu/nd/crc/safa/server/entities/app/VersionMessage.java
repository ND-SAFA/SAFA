package edu.nd.crc.safa.server.entities.app;

/**
 * Container for the versioned entity to update
 * along with the initiator.
 */
public class VersionMessage {

    String user;
    VersionedEntities type;

    public VersionMessage() {
    }

    public VersionMessage(String user, VersionedEntities type) {
        this.user = user;
        this.type = type;
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public VersionedEntities getType() {
        return type;
    }

    public void setType(VersionedEntities type) {
        this.type = type;
    }

}
