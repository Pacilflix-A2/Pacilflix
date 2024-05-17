CREATE OR REPLACE FUNCTION manage_subscription()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Transaction
        WHERE username = NEW.username
          AND end_date_time >= CURRENT_TIMESTAMP
    ) THEN
        UPDATE Transaction
        SET end_date_time = NEW.end_date_time,
            nama_paket = NEW.nama_paket,
            metode_pembayaran = NEW.metode_pembayaran,
            timestamp_pembayaran = CURRENT_TIMESTAMP
        WHERE username = NEW.username
          AND end_date_time >= CURRENT_TIMESTAMP
          AND start_date_time = (
              SELECT MAX(start_date_time)
              FROM Transaction
              WHERE username = NEW.username
                AND end_date_time >= CURRENT_TIMESTAMP
          );
    ELSE
        INSERT INTO Transaction(username, nama_paket, start_date_time, end_date_time, metode_pembayaran, timestamp_pembayaran)
        VALUES (NEW.username, NEW.nama_paket, CURRENT_TIMESTAMP, NEW.end_date_time, NEW.metode_pembayaran, CURRENT_TIMESTAMP);
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_transaction_insert
BEFORE INSERT ON Transaction
FOR EACH ROW
EXECUTE FUNCTION manage_subscription();
