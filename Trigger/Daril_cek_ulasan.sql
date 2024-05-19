CREATE OR REPLACE FUNCTION check_existing_review()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM ulasan
        WHERE id_tayangan = NEW.id_tayangan AND username = NEW.username
    ) THEN
        RAISE EXCEPTION 'User has already submitted a review for this tayangan';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_insert_ulasan
BEFORE INSERT ON ulasan
FOR EACH ROW
EXECUTE FUNCTION check_existing_review();