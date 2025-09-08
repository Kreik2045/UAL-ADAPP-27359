-- =======================
-- SP para Clientes
-- =======================
DELIMITER $$

CREATE PROCEDURE sp_insert_cliente (
    IN p_cliente_id INT,
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_email VARCHAR(150),
    IN p_fecha DATETIME
)
BEGIN
    IF (SELECT COUNT(*) FROM clientes WHERE email = p_email) = 0 THEN
        INSERT INTO clientes (cliente_id, nombre, apellido, email, FechaRegistro)
        VALUES (p_cliente_id, p_nombre, p_apellido, p_email, p_fecha);
    END IF;
END$$

DELIMITER ;

-- =======================
-- SP para Usuarios
-- =======================
DELIMITER $$

CREATE PROCEDURE sp_insert_usuario (
    IN p_userId INT,
    IN p_username VARCHAR(100),
    IN p_first_name VARCHAR(100),
    IN p_last_name VARCHAR(100),
    IN p_email VARCHAR(150),
    IN p_password_hash VARCHAR(255),
    IN p_rol VARCHAR(50),
    IN p_fecha DATETIME
)
BEGIN
    IF (SELECT COUNT(*) FROM usuarios WHERE email = p_email OR username = p_username) = 0 THEN
        INSERT INTO usuarios (userId, username, first_name, last_name, email, password_hash, rol, fecha_creacion)
        VALUES (p_userId, p_username, p_first_name, p_last_name, p_email, p_password_hash, p_rol, p_fecha);
    END IF;
END$$

DELIMITER ;

-- =======================
-- SP Rapidfuzz
-- =======================
DELIMITER $$

CREATE PROCEDURE sp_insert_csv_table (
    IN p_table_name VARCHAR(100),
    IN p_columns TEXT,
    IN p_values TEXT
)
BEGIN
    SET @query = CONCAT(
        'INSERT INTO ', p_table_name,
        ' (`', REPLACE(p_columns, ',', '`,`'), '`) ',
        'VALUES (', p_values, ');'
    );
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$

DELIMITER ;
