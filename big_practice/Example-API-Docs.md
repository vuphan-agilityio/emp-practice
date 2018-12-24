**emp APPS Example API docs**
----
  Returns json data about a single user.

* **URL**

  /users/:id

* **Method:**

  `GET`
  
* **URL Params**

**Required:**

`id=[integer]`

* **Data Params**

  None

* **Success Response:**

* **Code:** 200 <br />
    **Content:** `{ id : 12, name : "Michael Bloom" }`

* **Error Response:**

* **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`

OR

* **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

* **Sample Call:**

```Json
Request params:
{
    "email": "abc@gmail.com",
    "password": "123456",
    "retype_password": "123456",
    "first_name": "abc",
    "last_name": "xyz"
}

Response:
{
    "user": {
    "api_key": "0c89daddb0e6a3b872f57b40af1241a89bca2c95",
    "email": "abcde@gmail.com",
    "first_name": "abc",
    "id": 4,
    "last_name": "xyz"
    }
}
```
