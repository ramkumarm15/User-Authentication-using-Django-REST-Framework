# User Authentication using Django REST Framework

This app provides a basic user authentication like registration, login, logout, account activation and it works **CUSTOM_USER_MODEL** to handle SPA frameworks like React, Angular or Vue.

**Configure with your email and password in settings.py** to send activation and confirmation email to user.

## API Endpoints

##### User Register

**API ENDPOINT** : `/users/`

Use this api endpoint register new in db. Your user manger must have `create_user` method and `USERNAME_FILED` and `REQUIRED_FIELDS`.

| Method | Request                      | Response                     |
| ------ | ---------------------------- | ---------------------------- |
| `POST` | `{{ User.USERNAME_FIELD }}`  | `HTTP_201_CREATED`           |
|        | `{{ User.REQUIRED_FIELDS }}` |                              |
|        | `password`                   | `{{ User.USERNAME_FIELD }}`  |
|        | `re_password`                | `{{ User._meta.pk.name }}`   |
|        |                              | `{{ User.REQUIRED_FIELDS }}` |
|        |                              |                              |
|        |                              | `HTTP_400_BAD_REQUEST`       |
|        |                              |                              |
|        |                              | `{{ User.USERNAME_FIELD }}`  |
|        |                              | `{{ User.REQUIRED_FIELDS }}` |
|        |                              | `password`                   |
|        |                              | `re_password`                |

**API ENDPOINT** : `/users/me/`

Use this api endpoint retrive/update/delete user.

| Method   | Request                        | Response                     |
| -------- | ------------------------------ | ---------------------------- |
| `GET`    |                                | `HTTP_200_OK`                |
|          |                                | `{{ User.USERNAME_FIELD }}`  |
|          |                                | `{{ User._meta.pk.name }}`   |
|          |                                | `{{ User.REQUIRED_FIELDS }}` |
|          |                                |                              |
| `PUT`    | `{{{ User.REQUIRED_FIELDS }}}` | `HTTP_200_OK`                |
|          |                                | `{{ User.USERNAME_FIELD }}`  |
|          |                                | `{{ User._meta.pk.name }}`   |
|          |                                | `{{ User.REQUIRED_FIELDS }}` |
|          |                                |                              |
|          |                                | `HTTP_400_BAD_REQUEST`       |
|          |                                | `{{ User.REQUIRED_FIELDS }}` |
|          |                                |                              |
| `DELETE` |                                | `{{ HTTP_200_OK }}`          |

**API ENDPOINT** : `/users/activation/`

For this endpoint you need provide site in frontend application which will send a `POST` request to activation endpoint.

| Method | Request | Response               |
| ------ | ------- | ---------------------- |
| `POST` | `uid`   | `HTTP_204_NO_CONTENT`  |
|        | `token` |                        |
|        |         | `HTTP_400_BAD_REQUEST` |
|        |         | `uid`                  |
|        |         | `token`                |

## JWT Endpoints

###### To obtain JWT

**API ENDPOINT** : `/jwt/create/`

Use this endpoint to obtain a jwt for user. This endpoint will return a access and refresh token for user.

| Method | Request                     | Response                 |
| ------ | --------------------------- | ------------------------ |
| `POST` | `{{ User.USERNAME_FIELD }}` | `HTTP_201_CREATED`       |
|        | `password`                  | `access`                 |
|        |                             | `refresh`                |
|        |                             | `HTTP_400_BAD_REQUEST`   |
|        |                             | `{{ non_field_errors }}` |
|        |                             | `HTTP_401_Unauthorized`  |
|        |                             | `detail`                 |

###### To refresh JWT

**API ENDPOINT** : `/jwt/refresh/`

Use this endpoint to obtain a new jwt access token for user.

| Method | Request   | Response                |
| ------ | --------- | ----------------------- |
| `POST` | `refresh` | `HTTP_200_OK`           |
|        |           | `access`                |
|        |           | `HTTP_400_BAD_REQUEST`  |
|        |           | `refresh`               |
|        |           | `HTTP_401_Unauthorized` |
|        |           | `detail`                |

###### To verify JWT

**API ENDPOINT** : `/jwt/verify/`

Use this endpoint to obtain a verify jwt access token of user.

| Method | Request  | Response                |
| ------ | -------- | ----------------------- |
| `POST` | `access` | `HTTP_200_OK`           |
|        |          | `HTTP_400_BAD_REQUEST`  |
|        |          | `access`                |
|        |          | `HTTP_401_Unauthorized` |
|        |          | `detail`                |
