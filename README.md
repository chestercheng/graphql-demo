# graphql-demo
2018/08/01 Python Hsinchu User Group meetup

# Requirement

* [Python 3.6.5](https://www.python.org/downloads/release/python-365/)

* [pipenv](https://github.com/pypa/pipenv.git)

# Setup

Create python virtualenv and install pip packages:

```
$ git clone https://github.com/chestercheng/graphql-demo.git
$ cd graphql-demo
$ pipenv --python /path/to/python3.6.5
$ pipenv install
```

# Usage

Launch the GraphQL API server:

```shell
$ pipenv run python run.py
```

Run GraphQL queries:

```shell
# query
$ curl -s POST 'http://127.0.0.1:9487/graphql' -H 'Content-Type:application/graphql' -d @test-query.graphql | python -m json.tool

# mutation
$ curl -s POST 'http://127.0.0.1:9487/graphql' -H 'Content-Type:application/graphql' -d @test-mutation.graphql | python -m json.tool
```
