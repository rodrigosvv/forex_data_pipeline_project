from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.email import EmailOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator


from datetime import datetime, timedelta
import csv, requests, json

default_args = {
    "owner":"airflow",
    "email_on_failure" : False,
    "email_on_retry" : False,
    "email" : "salazarvegarodrigo@gmail.com",
    "retries" : 1,
    "retry_delay" : timedelta(minutes=5)
}

def download_rates():
    BASE_URL = "https://gist.githubusercontent.com/marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b/raw/"
    ENDPOINTS = {
        'USD': 'api_forex_exchange_usd.json',
        'EUR': 'api_forex_exchange_eur.json'
    }
    with open('/opt/airflow/dags/files/forex_currencies.csv') as forex_currencies:
        reader = csv.DictReader(forex_currencies, delimiter=';')
        for idx, row in enumerate(reader):
            base = row['base']
            with_pairs = row['with_pairs'].split(' ')
            indata = requests.get(f"{BASE_URL}{ENDPOINTS[base]}").json()
            outdata = {'base': base, 'rates': {}, 'last_update': indata['date']}
            for pair in with_pairs:
                outdata['rates'][pair] = indata['rates'][pair]
            with open('/opt/airflow/dags/files/forex_rates.json', 'a') as outfile:
                json.dump(outdata, outfile)
                outfile.write('\n')

def _get_message() -> str:
    return "Este es un mensaje de testeo de SlackWebhook Operator, si lo puedes ver, el test fue un éxito."



with DAG("forex_data_pipeline", start_date =datetime(2024, 1, 1), schedule_interval ="@daily", default_args=default_args, catchup=False) as dag:
    
    check_forex_rates = HttpSensor(
        task_id="check_forex_rates",
        http_conn_id="forex_api",
        endpoint="marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b",
        response_check=lambda response: "rates" in response.text,
        poke_interval=5,
        timeout=20
    )

    check_currencies_file = FileSensor(
        task_id="check_currencies_file",
        fs_conn_id="forex_path",
        filepath="forex_currencies.csv",
        poke_interval=5,
        timeout=20
    )

    downloading_rates = PythonOperator(
        task_id="downloading_rates",
        python_callable=download_rates
    )

    saving_rates = BashOperator(
        task_id="saving_rates",
        bash_command="""
            hdfs dfs -mkdir -p /forex && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex
        """
    )

    creating_forex_rates_table = HiveOperator(
        task_id="creating_forex_rates_table",
        hive_cli_conn_id="hive_conn",
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
                )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """
    )

    process_forex_data = SparkSubmitOperator(
        task_id="process_forex_data",
        application="/opt/airflow/dags/scripts/forex_processing.py",
        conn_id="spark_conn",
        verbose=False
    )

    send_email  = EmailOperator(
        task_id="send_email",
        to="salazarvegarodrigo@gmail.com",
        subject="Proyecto de Forex Data Pipeline",
        html_content="Si puedes leer este correo, el test fue un éxito"
    )

    send_slack_notif = SlackWebhookOperator(
        task_id="send_slack_notif",
        http_conn_id="slack_conn",
        message=_get_message(),
        channel="#slack-notif-testing"
    )
    

    check_forex_rates>>check_currencies_file>>downloading_rates
    downloading_rates>>saving_rates>>creating_forex_rates_table
    creating_forex_rates_table>>process_forex_data>>send_email
    send_email>>send_slack_notif