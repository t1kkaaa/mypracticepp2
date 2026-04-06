CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value OR phone = p_value;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_contacts()
LANGUAGE plpgsql AS $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN SELECT * FROM temp_contacts LOOP
        IF rec.phone ~ '^[0-9]{11}$' THEN
            INSERT INTO phonebook(first_name, phone)
            VALUES (rec.first_name, rec.phone)
            ON CONFLICT (phone) DO NOTHING;
        ELSE
            RAISE NOTICE 'Invalid phone: %', rec.phone;
        END IF;
    END LOOP;
END;
$$;