CREATE TABLE ingestion_batches(
    batch_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_system VARCHAR(20) NOT NULL,
    source_filename VARCHAR(255) NOT NULL,
    started_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP NOT NULL,
    completed_at TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL,
    total_records INTEGER NOT NULL DEFAULT 0,
    accepted_count INTEGER NOT NULL DEFAULT 0,
    quarantined_count INTEGER NOT NULL DEFAULT 0,
    CHECK (source_system IN ('BANK', 'PAYMENT')),
    CHECK (total_records >= 0),
    CHECK (accepted_count >= 0),
    CHECK (quarantined_count >= 0),
    CHECK (
        completed_at IS NULL
        OR completed_at >= started_at
    )
);

CREATE TABLE transactions(
    uniqueid BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    account_id VARCHAR(50) NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    batch_id BIGINT NOT NULL,
    FOREIGN KEY (batch_id) References ingestion_batches(batch_id),
    UNIQUE(batch_id,transaction_id),
    CHECK(amount>0),
    CHECK(status IN ('COMPLETED'))
);


CREATE TABLE quarantine_records(
    uniqueid BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    transaction_id VARCHAR(50),
    raw_record JSONB NOT NULL,
    rejection_reasons TEXT[] NOT NULL,
    batch_id BIGINT NOT NULL,
    FOREIGN KEY(batch_id) References ingestion_batches(batch_id),
    CHECK(cardinality(rejection_reasons)>0)
);


