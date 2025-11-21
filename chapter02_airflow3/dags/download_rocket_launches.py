import json
import pathlib
import datetime
import pendulum
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="download_rocket_launches",
    description="Download rocket pictures of recently launched rockets.",
    start_date=pendulum.today("UTC").add(days=-1),
    schedule_interval=datetime.timedelta(minutes=2),
    catchup=False,
) as dag:
    download_launches = BashOperator(
        task_id="download_launches",
        bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    )

    def _get_pictures():
        # Ensure directory exists
        images_dir = pathlib.Path("/tmp/images")
        images_dir.mkdir(parents=True, exist_ok=True)

        # Download all pictures in launches.json
        launches_path = pathlib.Path("/tmp/launches.json")
        launches = json.loads(launches_path.read_text())

        image_urls = [launch["image"] for launch in launches["results"]]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = images_dir / image_filename
                target_file.write_bytes(response.content)
                print(f"Downloaded {image_url} to {target_file}")
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}.")

    get_pictures = PythonOperator(
        task_id="get_pictures",
        python_callable=_get_pictures,
    )

    notify = BashOperator(
        task_id="notify",
        bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."',
    )

    download_launches >> get_pictures >> notify
