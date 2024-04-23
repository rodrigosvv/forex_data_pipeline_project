
# Forex Data Pipeline

El objetivo de este proyecto, realizado con la ayuda del curso de Udemy de Marc Lamberti, es procesar datos sobre divisas (Forex data), enviar un correo elecrónico y por último una notificación de Slack sobre el éxito del DagRun. 

## Arquitectura del Proyecto

![Data_pipeline_arquitectura](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/5a916608-29b8-4a99-8350-af913f3dec70)

Fuente: Marc Lamberti 

## Tech Stack
- Python
- Hadoop
- Hive
- Airflow
- Spark
- Docker
- Bash

## Conexiones a crear en Airflow

### FOREX_API

![Forex_api_conn](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/9402c3c2-6fef-48a5-bb90-d079db9b5c64)

### FOREX_PATH

![Forex_path_conn](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/2dbe71db-021d-4b74-af10-f6ea5493f2ce)


### HIVE_CONN

![Hive_conn](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/bc9b36ed-c98e-43fd-88c5-76a7bc5b83e4)


### SPARK_CONN

![Spark_conn](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/77cfbd52-17eb-432b-8bec-28ed1e0c4a5d)


### SLACK_CONN

![Slack_conn](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/cea29c02-9cee-44d5-83ae-c916c9e4d22d)

NOTA: Para SLACK_CONN, además del host, se requiere colocar un Password con la siguiente estructura (ejemplo): /TXXXXXXXXXX/BXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXX

## Tasks y Operators

### Comprobar si la URL donde están las divisas es accesible o no.

![check_forex_rates](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/ed606d1a-ba5c-49ad-8acf-962c023aef91)


### Comprobar si el archivo donde se encuentra la moneda que desea obtener de la URL es accesible o no.

![check_currencies_file](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/5a7fc9eb-ad7d-4bd8-a19d-1d487fcb3dd9)


### Descargar las divisas ejecutando una función Python (PythonOperator).

![download_rates](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/a1195f7c-e85e-4fb3-b9e6-037e4d95c11b)


### Guardaremos los tipos de cambio en HDFS (BashOperator).

![bash_operator](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/f7e137ff-7d41-4fe3-8095-dda9c4738515)


### Crearemos una tabla en Hive (HiveOperator) para interactuar con los tipos de cambio almacenados en HDFS.

![creating_forex_rate_tables](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/e5ff946e-bc9d-4a71-875f-5c54c3beb288)


### Procesaremos los tipos de cambio con Spark (SparkSubmitOperator).

![Spark_submit](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/98a50915-5317-480a-b0b7-ea6a1a8fd83e)


### Por último enviaremos un correo electrónico (EmailOperator) y una notificación de Slack (SlackWebhookOperator).

![email_operator](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/1b92d79a-ec93-4408-84f3-2c36dc0e4ec6)
![slack_operator](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/8c793e2f-753a-4e99-a2e6-7d6bfd28ebe5)

## Visualización de la data cargada en la tabla de Hive

### Email y Slack

#### Configuración de parámetros en airflow.cfg
![Mail_config](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/29da7e6e-b79b-4099-9326-60d9ab2b6348)

#### Email y Notifiación de Slack enviadas

Email:


![Email_sent_success](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/2326917f-f9a2-4589-8ff8-4a57a8c0504f)

Slack: 


![Slack_sent_success](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/f32f3ea5-9cff-42f7-b8ef-db3ef88b1382)

## ¡Data Pipeline en acción!

![data_pipeline_success](https://github.com/rodrigosvv/forex_data_pipeline_project/assets/143859478/ec3c7bf5-3b06-4ee5-a69d-2c0af5ce0f89)






