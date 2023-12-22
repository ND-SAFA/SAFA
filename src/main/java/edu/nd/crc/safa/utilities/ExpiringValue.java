package edu.nd.crc.safa.utilities;

import java.time.Duration;
import java.time.Instant;
import java.time.temporal.TemporalAmount;

import lombok.Getter;
import lombok.Setter;

/**
 * A holder for a value that will expire at some point in the future
 *
 * @param <T> The type of value to hold
 */
public class ExpiringValue<T> {
    private T currentValue;
    private Instant expirationTime;

    @Getter
    @Setter
    private T defaultValue;

    @Getter
    @Setter
    private TemporalAmount defaultExpiration;

    /**
     * Construct a new object with a default value of {@code null} and a
     * default expiration time of 1 hour
     */
    public ExpiringValue() {
        this(null);
    }

    /**
     * Construct a new object with a given default value and a default expiration
     * time of 1 hour
     *
     * @param defaultValue The default value to fall back on when the value expires
     */
    public ExpiringValue(T defaultValue) {
        this(defaultValue, Duration.ofHours(1));
    }

    /**
     * Construct a new object with a given default value and default expiration time
     *
     * @param defaultValue The default value to fall back on when the value expires
     * @param defaultExpiration The default amount of time for a value to last
     */
    public ExpiringValue(T defaultValue, TemporalAmount defaultExpiration) {
        this.currentValue = defaultValue;
        this.defaultValue = defaultValue;
        this.defaultExpiration = defaultExpiration;
        this.expirationTime = null;
    }

    /**
     * Get the current value of the object. If the value has expired, this
     * will be the default value. Otherwise, it is the last value the object
     * was set to
     *
     * @return The current value of the object
     */
    public T get() {
        if (expirationTime != null && isExpired()) {
            currentValue = defaultValue;
            expirationTime = null;
        }
        return currentValue;
    }

    /**
     * Set the value of the object with a given expiration time
     *
     * @param value The value to set
     * @param expiration The amount of time for the value to last
     */
    public void set(T value, TemporalAmount expiration) {
        setExpiration(expiration);
        currentValue = value;
    }

    /**
     * Set the value of the object using the default expiration time
     *
     * @param value The value to set
     */
    public void set(T value) {
        set(value, defaultExpiration);
    }

    /**
     * Refresh the stored value's expiration using the default
     * expiration time
     */
    public void refresh() {
        refresh(defaultExpiration);
    }

    /**
     * Refresh the stored value's expiration. The value will now expire
     * at the current instant plus the given amount of time.
     *
     * @param expiration The amount of time until the value should expire
     */
    public void refresh(TemporalAmount expiration) {
        if (!isExpired()) {
            setExpiration(expiration);
        }
    }

    /**
     * Get the current value and refresh its expiration
     *
     * @return The current value
     */
    public T getAndRefresh() {
        return getAndRefresh(defaultExpiration);
    }

    /**
     * Get the current value and refresh its expiration
     *
     * @param expiration The new expiration - the current value will last
     *                   until the current instant plus this amount
     * @return The current value
     */
    public T getAndRefresh(TemporalAmount expiration) {
        T value = get();
        refresh(expiration);
        return value;
    }

    /**
     * Set the expiration time of the value
     *
     * @param expiration The time until expiration
     */
    private void setExpiration(TemporalAmount expiration) {
        expirationTime = Instant.now().plus(expiration);
    }

    /**
     * Returns whether the current value is expired or not. This will be true
     * after an expiration but also before a value has been set
     *
     * @return Whether the current value is expired
     */
    private boolean isExpired() {
        return expirationTime == null || Instant.now().isAfter(expirationTime);
    }
}
