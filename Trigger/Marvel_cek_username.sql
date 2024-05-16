CREATE OR REPLACE FUNCTION check_username_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM pengguna WHERE username = NEW.username) THEN
        RAISE EXCEPTION 'Username % already exists.', NEW.username;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_username_before_insert
BEFORE INSERT ON pengguna
FOR EACH ROW
EXECUTE FUNCTION check_username_exists();