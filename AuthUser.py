from typing import List, Optional, Dict


class AuthUser:
    _user_name: Optional[str] = None
    _is_auth: bool = False
    _FILE_NAME: str = 'auth-data.txt'
    _LINE_DELIMITER: str = "\n"
    _USER_DATA_DELIMITER: str = '::'

    @property
    def _users_data(self):
        users = {}

        with open(self._FILE_NAME, 'a+') as file:
            for user_data in file.read().split(self._LINE_DELIMITER):
                if user_data and self._USER_DATA_DELIMITER in user_data:
                    user_data_part = user_data.split(self._USER_DATA_DELIMITER)
                    users[user_data_part[0]] = user_data_part[1]

        return users

    @property
    def _users(self) -> List[str]:
        return list(self._users_data)

    @property
    def registration_users(self) -> Optional[List[str]]:
        if not self._is_auth:
            print('Для вывода имени пользователя необходимо авторизоваться')
            return

        return self._users

    @property
    def is_auth(self) -> bool:
        return self._is_auth

    @property
    def user_name(self) -> Optional[str]:
        if not self._is_auth:
            print('Для вывода имени пользователя необходимо авторизоваться')
            return

        return self._user_name

    def register(self) -> None:
        user_name = input('Введите имя пользователя: ').strip()

        if (not user_name or len(user_name) < 4
                or len(user_name) > 8 or self._check_user_name_exist(user_name)):
            print('Имя пользователя не подходит')
            return

        password = input('Введите пароль: ').strip()

        if (not password or len(password) < 4 or len(password) > 8
                or password == user_name):
            print('Пароль не подходит')
            return

        with open(self._FILE_NAME, 'a+') as file:
            file.write(f'{user_name}{self._USER_DATA_DELIMITER}{password}{self._LINE_DELIMITER}')

        print('Регистрация успешна')


    def delete_user(self) -> None:
        if self._is_auth == True:
            action = input("Введите Y -  если хотите удалить пользователя, если нет нажмите N: ")
            if action == 'N':
                return
            if action == 'Y':

                users_temp = {}

            with open(self._FILE_NAME, 'r+') as file:
                for user_data in file.read().split(self._LINE_DELIMITER):
                    if user_data and self._USER_DATA_DELIMITER in user_data:
                        user_data_part = user_data.split(self._USER_DATA_DELIMITER)
                        users_temp[user_data_part[0]] = user_data_part[1]

            del users_temp[self._user_name]

            with open(self._FILE_NAME, 'w') as file:
                for user_name in users_temp:
                    file.write(f'{user_name}{self._USER_DATA_DELIMITER}{users_temp[user_name]}{self._LINE_DELIMITER}')

            print(self._user_name, 'Удален')

        else:
            print('Необходимо авторизоваться')



    def logout(self) -> None:
        self._is_auth = False
        self._user_name = None

    def login(self) -> None:
        user_name = input('Введите имя пользователя: ').strip()

        if user_name not in self._users:
            print('Имя пользователя не подходит')
            return

        password = input('Введите пароль: ').strip()

        if password != self._users_data[user_name]:
            print('Пароль не подходит')
            return

        self._is_auth = True
        self._user_name = user_name
        print('Вы вошли в систему')

    def _check_user_name_exist(self, user_name: str) -> bool:
        return user_name in self._users
