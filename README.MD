Run project - docker-compose --file build_env/docker-compose/local/docker-compose.yml up -d 
Stop project - docker-compose --file build_env/docker-compose/local/docker-compose.yml down -v
Generate migrations - alembic revision --autogenerate -m 'migration name'
Run migrations - alembic upgrade head