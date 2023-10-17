lint:
	poetry run isort my_site --check-only
	poetry run black my_site --check
	poetry run ruff my_site
fmt:
	poetry run isort my_site
	poetry run black my_site
	poetry run ruff my_site --fix
types:
	poetry run mypy my_site
