package edu.nd.crc.safa.features.permissions;

import edu.nd.crc.safa.features.permissions.entities.Permission;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;

@JsonIgnoreProperties({"cause", "stackTrace", "suppressed", "localizedMessage"})
@Getter
public class MissingPermissionException extends RuntimeException {

    @JsonIgnore
    private final Permission missingPermission;

    public MissingPermissionException(Permission missingPermission) {
        super("Missing permission.");
        this.missingPermission = missingPermission;
    }

    public String getPermission() {
        return missingPermission.getName();
    }
}
