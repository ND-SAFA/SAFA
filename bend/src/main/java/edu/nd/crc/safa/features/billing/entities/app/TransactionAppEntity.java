package edu.nd.crc.safa.features.billing.entities.app;

import java.time.LocalDateTime;
import java.util.UUID;

import edu.nd.crc.safa.features.billing.entities.db.Transaction;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
@NoArgsConstructor
public class TransactionAppEntity {
    private UUID id;
    private Transaction.Status status;
    private int amount;
    private String description;
    private LocalDateTime timestamp;
    private String redirectUrl;

    public TransactionAppEntity(Transaction transaction) {
        this.id = transaction.getId();
        this.status = transaction.getStatus();
        this.amount = transaction.getAmount();
        this.description = transaction.getDescription();
        this.timestamp = transaction.getTimestamp();
        this.redirectUrl = null;
    }

    public TransactionAppEntity(Transaction transaction, String redirectUrl) {
        this(transaction);
        this.redirectUrl = redirectUrl;
    }
}
