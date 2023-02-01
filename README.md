# fastapi-stripe-demo

ref: https://qiita.com/ryori0925/items/722cd64045e0142122a5

## Usage

set and copy sample.env to .env

```shell
docker-compose up -d
```

## Access

http://localhost:8080/docs

---

## Setup Deta.sh

2023/1/2時点にてDeta.shのmicrosのPython Runtimeは3.9までしか対応していない。

```shell
# install Deta CLI
curl -fsSL https://get.deta.dev/cli.sh | sh
```

Open another Terminal

```shell
# login
deta login
>> Please, log in from the web page. Waiting...
>> https://web.deta.sh/cli/65027
>> Logged in successfully.

# create new application
# and get endpoint-url
deta new --python --name stripe-demo-api app
# comi .deta

cd app
# create auth
deta auth enable
deta auth create-api-key --name stripe_demo_api_key --desc "api key for agent 1"

# visor
deta visor enable
```

Is it safe to commit the .deta folder created by the cli?

> Yes it is safe to commit your .deta folder and push it to public repositories.
> ref: https://docs.deta.sh/docs/micros/faqs_micros/

```shell
# if change file
cd app
deta deploy
```

```shell
# if server error
deta logs

# or browser access to Visor at Deta.sh
```

ref:
https://fastapi.tiangolo.com/ja/deployment/deta/
https://docs.deta.sh/docs/micros/api_keys
https://docs.deta.sh/docs/cli/commands#deta-deploy
