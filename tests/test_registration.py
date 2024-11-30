import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    test = add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:

def test_authenticate_user(setup_database, connection):
    """Тест успешной аутентификации пользователя."""
    user = authenticate_user('testuser', 'password123')
    assert user == True
    no_user = authenticate_user('testuser2', 'password1')
    assert no_user == False

def test_display_users(capsys):
    """Тест отображения списка пользователей."""
    display_users()
    captured = capsys.readouterr()
    assert 'Логин: testuser, Электронная почта: testuser@example.com' in captured.out

    

"""
Тест добавления пользователя с существующим логином.

Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.

"""