CREATE OR REPLACE FUNCTION manage_subscription()
RETURNS TRIGGER AS $$
DECLARE
    latest_active_transaction RECORD;
BEGIN
    SELECT * INTO latest_active_transaction
    FROM Transaction
    WHERE username = NEW.username AND end_date_time >= CURRENT_DATE
    ORDER BY end_date_time DESC
    LIMIT 1;
    
    IF latest_active_transaction IS NOT NULL THEN
        UPDATE Transaction
        SET end_date_time = NEW.end_date_time,
            nama_paket = NEW.nama_paket,
            resolusi_layar = NEW.resolusi_layar,
            dukungan_perangkat = NEW.dukungan_perangkat,
            metode_pembayaran = NEW.metode_pembayaran,
            timestamp_pembayaran = NEW.timestamp_pembayaran
        WHERE username = NEW.username AND transaction_id = latest_active_transaction.transaction_id;
    
    ELSE
        INSERT INTO Transaction(username, nama_paket, start_date_time, end_date_time, metode_pembayaran, timestamp_pembayaran)
        VALUES (NEW.username, NEW.nama_paket, NEW.start_date_time, NEW.end_date_time, NEW.metode_pembayaran, NEW.timestamp_pembayaran);
    END IF;
    
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;


CREATE TRIGGER trigger_manage_subscription
BEFORE INSERT ON Transaction
FOR EACH ROW
EXECUTE FUNCTION manage_subscription();
