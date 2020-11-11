## Comandos

`flask run` -> Corre el proyecto en el puerto 5000  
`flask db init --multidb` -> Inicializar la base de datos  
`flask db migrate` -> Crear una migracion nueva  
`flask db upgrade` -> Aplicar las migraciones  

## Database

```
CREATE USER dev WITH PASSWORD 'dev';
ALTER ROLE dev SET client_encoding TO 'utf8';
ALTER ROLE dev SET default_transaction_isolation TO 'read committed';
ALTER ROLE dev SET timezone TO 'UTC';
```

```
CREATE DATABASE tap_products;
CREATE DATABASE tap_users;
CREATE DATABASE tap_sales;
```

```
GRANT ALL PRIVILEGES ON DATABASE tap_products TO dev;
GRANT ALL PRIVILEGES ON DATABASE tap_users TO dev;
GRANT ALL PRIVILEGES ON DATABASE tap_sales TO dev;
```