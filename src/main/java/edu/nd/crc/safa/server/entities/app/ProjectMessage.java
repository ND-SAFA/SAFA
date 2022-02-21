package edu.nd.crc.safa.server.entities.app;

/**
 * Container for the project entity to update
 * along with the initiator.
 */
public class ProjectMessage {

    String user;
    ProjectEntities type;

    public ProjectMessage() {
    }

    public ProjectMessage(String user, ProjectEntities type) {
        this.user = user;
        this.type = type;
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public ProjectEntities getType() {
        return type;
    }

    public void setType(ProjectEntities type) {
        this.type = type;
    }

}
