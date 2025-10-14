package edu.nd.crc.safa.features.users.entities;

import java.util.UUID;

public interface IUser {
    UUID getUserId();

    String getEmail();

    boolean equals(Object user);

    int hashCode();
}
