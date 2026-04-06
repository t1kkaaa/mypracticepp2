-- 1. Функция поиска по шаблону (имя или телефон)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(search_term TEXT)
RETURNS TABLE(contact_name VARCHAR, contact_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    WHERE name ILIKE '%' || search_term || '%' 
       OR phone ILIKE '%' || search_term || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Функция для пагинации
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(contact_name VARCHAR, contact_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    ORDER BY name 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;