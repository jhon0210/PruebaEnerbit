# Proyecto Enerbit

## Instalacion

### Descargar Repositorio

```bash
git clone https://github.com/jhon0210/PruebaEnerbit
```

### Creacion y Activacion Ambiente Virtual

```bash
python3 -m venv enerbit-venv
source enerbit-venv/bin/activate    # Para linux
```

### Instalacion de Paquetes

```bash
cd enerbit
pip install -r requirements.txt
```

### Instalacion y Ejecucion de Contenedor Postgresl

```bash
docker pull postgres
docker run --name psql_container -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

### Instalacion y Ejecucion de Contenedor Redis

```bash
docker pull redis
docker run -d -p 6379:6379 --name enerbit-redis redis
```

### Creacion Variable de Entorno Conexion Base de Datos

```bash
export DB_URL='postgresql://username:password@localhost:5432/dbname
```

### Ejecucion de Servidor Uvicorn

```bash
cd enerbit
uvicorn main:app --reload
```
