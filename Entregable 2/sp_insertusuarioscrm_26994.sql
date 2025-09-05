DELIMITER $$

CREATE PROCEDURE sp_insert_csv_table_001 (
    IN p_table_name VARCHAR(100),
    IN p_columns TEXT,
    IN p_values TEXT
)
BEGIN
    /*
      p_table_name = nombre de la tabla destino
      p_columns    = columnas separadas por coma (ej: "nombre,apellido,email")
      p_values     = valores separados por comillas simples y coma (ej: "'Juan','Perez','juan@mail.com'")
    */

    -- Encerramos cada columna en backticks para evitar errores con nombres reservados o espacios
    SET @query = CONCAT('INSERT INTO ', p_table_name, ' (`', REPLACE(p_columns, ',', '`,`'), '`) VALUES (', p_values, ');');
    PREPARE stmt FROM @query;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END$$

DELIMITER ;
