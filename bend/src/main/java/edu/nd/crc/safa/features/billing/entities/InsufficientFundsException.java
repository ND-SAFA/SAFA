package edu.nd.crc.safa.features.billing.entities;

import edu.nd.crc.safa.features.projects.entities.app.SafaError;

import lombok.EqualsAndHashCode;
import lombok.Getter;

/**
 * Exception thrown when a transaction is attempted that the user does not have funds for
 */
@Getter
@EqualsAndHashCode(callSuper = true)
public class InsufficientFundsException extends SafaError {
    private final int currentBalance;
    private final int chargeAmount;

    public InsufficientFundsException(int currentBalance, int chargeAmount) {
        super(String.format("Insufficient funds: Attempted to deduct %d but current balance is %d",
            chargeAmount, currentBalance));
        this.currentBalance = currentBalance;
        this.chargeAmount = chargeAmount;
    }
}
