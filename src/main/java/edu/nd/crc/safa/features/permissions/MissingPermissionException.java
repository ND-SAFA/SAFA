package edu.nd.crc.safa.features.permissions;

import edu.nd.crc.safa.features.permissions.entities.Permission;
import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;

@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage", "exception", "errors"})
@Getter
public class MissingPermissionException extends SafaError {

    @JsonIgnore
    private final Permission missingPermission;

    public MissingPermissionException(Permission missingPermission) {
        super("Missing permission: " + missingPermission.getName());
        this.missingPermission = missingPermission;
    }

    public String getPermission() {
        return missingPermission.getName();
    }
}
