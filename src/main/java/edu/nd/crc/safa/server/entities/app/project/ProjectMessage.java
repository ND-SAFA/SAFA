package edu.nd.crc.safa.server.entities.app.project;

/**
 * Container for the project entity to update
 * along with the initiator.
 */
public class ProjectMessage {

    String user;
    ProjectEntityTypes type;

    public ProjectMessage() {
    }

    public ProjectMessage(String user, ProjectEntityTypes type) {
        this.user = user;
        this.type = type;
    }

    public String getUser() {
        return user;
    }

    public void setUser(String user) {
        this.user = user;
    }

    public ProjectEntityTypes getType() {
        return type;
    }

    public void setType(ProjectEntityTypes type) {
        this.type = type;
    }

}
