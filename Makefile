# Docker commands
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

rebuild:
	docker-compose build --no-cache

logs:
	docker-compose logs -f

# Development commands
dev:
	docker-compose up -d

stop:
	docker-compose stop

restart:
	docker-compose restart

# Database commands
db-migrate:
	docker-compose exec api npx prisma migrate deploy

db-reset:
	docker-compose exec api npx prisma migrate reset --force

# Cleanup commands
clean:
	docker-compose down -v --remove-orphans

prune:
	docker system prune -af