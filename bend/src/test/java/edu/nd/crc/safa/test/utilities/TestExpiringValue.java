package edu.nd.crc.safa.test.utilities;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;

import java.time.Duration;

import edu.nd.crc.safa.utilities.ExpiringValue;

import org.junit.jupiter.api.Test;

public class TestExpiringValue {

    @Test
    public void testDefaultExpiration() throws InterruptedException {
        ExpiringValue<Integer> testObj = new ExpiringValue<>(0, Duration.ofSeconds(1));
        testObj.set(2);
        assertThat(testObj.get()).isEqualTo(2);
        Thread.sleep(1500);
        assertThat(testObj.get()).isEqualTo(0);
    }

    @Test
    public void testExplicitExpiration() throws InterruptedException {
        ExpiringValue<Integer> testObj = new ExpiringValue<>(0, Duration.ofSeconds(1));
        testObj.set(2, Duration.ofSeconds(2));
        assertThat(testObj.get()).isEqualTo(2);
        Thread.sleep(1500);
        assertThat(testObj.get()).isEqualTo(2);
        Thread.sleep(1500);
        assertThat(testObj.get()).isEqualTo(0);
    }

    @Test
    public void testRefresh() throws InterruptedException {
        ExpiringValue<Integer> testObj = new ExpiringValue<>(0, Duration.ofSeconds(1));
        testObj.set(2);
        assertThat(testObj.get()).isEqualTo(2);
        Thread.sleep(750);
        assertThat(testObj.getAndRefresh()).isEqualTo(2);
        Thread.sleep(750);
        assertThat(testObj.get()).isEqualTo(2);
        Thread.sleep(750);
        assertThat(testObj.get()).isEqualTo(0);
    }
}
