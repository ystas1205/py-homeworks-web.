# Домашнее задание к лекции «Aiohttp»


Для генерации случайного уникального индификатора (токена)создана 
таблица Token. При создании обьявления, по id проверяется, есть ли данный пользователь
в таблице Token,если есть, то создается обьявление в таблице обьявлений. При удалении
и обновлении проверяется токен передаваемый в заголовке запроса и id usera c таблицей Token.