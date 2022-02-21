package edu.nd.crc.safa.server.entities.app;

/**
 * Container for the versioned entity to update
 * along with the initiator.
 */
public class VersionMessage {

    String user;
    VersionEntityTypes type;

    public VersionMessage() {
    }

    public VersionMessage(String user, VersionEntityTypes type) {
        this.user = user;
        this.type = type;
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public VersionEntityTypes getType() {
        return type;
    }

    public void setType(VersionEntityTypes type) {
        this.type = type;
    }

}
