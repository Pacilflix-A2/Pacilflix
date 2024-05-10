CREATE OR REPLACE FUNCTION check_delete_tayangan_terunduh()
RETURNS TRIGGER AS
$$
BEGIN
    IF OLD.timestamp >= CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta' - INTERVAL '24 hours' AND
       OLD.timestamp <= CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Jakarta' THEN
        RAISE EXCEPTION 'Tayangan terunduh harus lebih dari satu hari untuk dihapus';
    ELSE
        RETURN OLD;
    END IF;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER before_delete_tayangan_terunduh
BEFORE DELETE ON TAYANGAN_TERUNDUH
FOR EACH ROW
EXECUTE FUNCTION check_delete_tayangan_terunduh();