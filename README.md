Below there are some pipeline examples, and the command to run them in docker (they can be run locally too)

### Perform plannet data retrieve test
By the terminal run:

```bash
docker exec -it capgemmini_container python src/capgemmini/plannet_data_retrieve_pipeline_test.py
```

### Perform horizon data retrieve test
By the terminal run:

```bash
docker exec -it capgemmini_container python src/capgemmini/horizon_data_retrieve_pipeline_test.py
```

### Perform sauron data retrieve test
By the terminal run:

```bash
docker exec -it capgemmini_container python src/capgemmini/sauron_data_retrieve_pipeline_test.py
```

### Perform multi data retrieve test
By the terminal run:

```bash
docker exec -it capgemmini_container python src/capgemmini/multi_data_retrieve_pipeline_test.py
```

### Check Rq status
By the terminal run:

```bash
docker exec -it capgemmini_container tainer rq info --url redis://docker.internal:6379
```

## Quick ports

### Perform access to redis insight dashboard
In your browser, access the following url:
http://localhost:8001/

### Perform access to grafana
In your browser, access the following url:
http://localhost:3000/

### Perform access to redis queue dashboard
In your browser, access the following url:
http://localhost:9181/

### Perform access to pushgateway dashboard
In your browser, access the following url:
http://localhost:9091/

### Perform access to prometheus dashboard
In your browser, access the following url:
http://localhost:9090/

## Miscellaneous

### Generate client wrapper code

follow the instruction below to install swagger-codegen:

https://github.com/swagger-api/swagger-codegen

if you came across the problem, The incoming YAML document exceeds the limit; you can increase the limit by running the following command:

```bash
export _JAVA_OPTIONS=-DmaxYamlCodePoints=99999999
```

and run again the swagger-codegen command
## Support

For support, email or write on teams to:

- Leonardo Alfonsi -> leonardo.alfonsi@skytv.it
- Giuseppe Tringale -> giuseppe.tringale@sky.uk
