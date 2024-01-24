package edu.nd.crc.safa.utilities;

import java.time.Duration;
import java.time.Instant;
import java.util.function.Supplier;

/**
 * Represents a value which does not update often and is somewhat expensive to produce.
 * This class will cache the produced value for a specified amount of time so that
 * multiple subsequent requests will use the cached value instead of reproducing the value.
 *
 * @param <T> The type being stored
 */
public class CachedValue<T> {
    public static final Duration DEFAULT_EXPIRATION = Duration.ofMinutes(5);

    private T value;
    private Instant expiryInstant;
    private final Duration expirationTime;
    private final Supplier<T> valueSupplier;

    /**
     * Constructor
     *
     * @param valueSupplier The function that will produce the cached value
     */
    public CachedValue(Supplier<T> valueSupplier) {
        this(valueSupplier, DEFAULT_EXPIRATION);
    }

    /**
     * Constructor
     *
     * @param valueSupplier The function that will produce the cached value
     * @param expirationTime How long the cached value should last
     */
    public CachedValue(Supplier<T> valueSupplier, Duration expirationTime) {
        this.expiryInstant = Instant.now();
        this.expirationTime = expirationTime;
        this.valueSupplier = valueSupplier;
    }

    /**
     * Get the value, updating it if necessary
     *
     * @return The stored value
     */
    public T getValue() {
        if (needsUpdate()) {
            updateValue();
        }

        return value;
    }

    /**
     * Returns whether the value has expired and needs to be updated
     *
     * @return true if the value expired
     */
    private boolean needsUpdate() {
        return expiryInstant.isBefore(Instant.now());
    }

    /**
     * Updates the stored value by calling the supplier and updating the expiration instant
     */
    private void updateValue() {
        value = valueSupplier.get();
        expiryInstant = Instant.now().plus(expirationTime);
    }
}
