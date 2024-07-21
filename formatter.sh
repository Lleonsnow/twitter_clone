# Форматирование с помощью Black
echo "Форматирование кода с помощью Black"
black --config pyproject.toml .

# Сортировка импортов с помощью isort
echo "Сортировка импортов с помощью isort"
isort --settings-path setup.cfg . --profile black --float-to-top

# Удаление неиспользуемых импортов и переменных с помощью autoflake
echo "Удаление неиспользуемых импортов и переменных с помощью autoflake"
autoflake --in-place --remove-unused-variables --remove-all-unused-imports . --recursive

# Форматирование docstring-ов с помощью docformatter
echo "Форматирование docstring-ов с помощью docformatter"
docformatter --config setup.cfg -r --in-place --recursive .

# Проверка кода с помощью flake8
echo "Проверка кода с помощью flake8"
flake8 --config setup.cfg .
