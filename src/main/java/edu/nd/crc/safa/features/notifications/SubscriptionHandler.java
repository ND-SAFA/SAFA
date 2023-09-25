package edu.nd.crc.safa.features.notifications;

public interface SubscriptionHandler {

    void handleSubscription(String channelName, String channelId);
}
