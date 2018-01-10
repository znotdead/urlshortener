
## Installation
You need to installed docker-ce.

For setup:
```bash
 make setup
 ```

GraphiQL: http://127.0.0.1:8000/graphiql/
admin:  http://127.0.0.1:8000/admin

To create a Short URL in GraphiQL run:

```
mutation {
  createShorturl(longUrl: "http://sdfeter") {
    shorturl {
      longUrl
      code
    }
    ok
  }
}
```

To get list of all urls:
```
{
  allShorturls {
    id
    code
    longUrl
  }
}

To get Original URL:
```
{
  exist: getShorturl(code: "abc") {
    longUrl
  }
}
```

To run tests:
```bash
make test
```

To run dev server:
```bash
make run
```

