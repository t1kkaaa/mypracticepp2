-- 1. Процедура Upsert (вставка или обновление номера по имени)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Массовая вставка с циклом и валидацией номера
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    p_names VARCHAR[], 
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        -- Простая валидация: номер должен состоять из цифр и быть длиннее 10 символов
        IF p_phones[i] ~ '^[0-9+]+$' AND length(p_phones[i]) >= 10 THEN
            INSERT INTO contacts (name, phone)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
        ELSE
            RAISE NOTICE 'Skipping invalid phone for user %: %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;

-- 3. Удаление по имени или телефону
CREATE OR REPLACE PROCEDURE delete_contact(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_identifier OR phone = p_identifier;
END;
$$;