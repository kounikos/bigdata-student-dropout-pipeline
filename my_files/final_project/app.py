from flask import Flask, render_template
import start_servers, producer, spark_map_csv, avro_data

# Initialize Flask app
app = Flask(__name__)

# when the user hits the root route, render the index.html template
@app.route('/')
def homepage():
    return render_template('index.html')

# when the user clicks the button on index, start the servers
# when the servers are started, continue to kafka page
@app.route('/kafka_start', methods=['POST'])
def servers_start():
    start_servers.start_servers()
    return render_template('kafka.html')

# when the user clicks the button on servers, start the kafka job
# when the job is started, continue to spark page
@app.route('/spark_start', methods=['POST'])
def job_kafka():
    producer.kafka_job()
    avro = avro_data.load_avro_data()
    return render_template('spark.html', avro = avro)

# when the user clicks the button on spark, start the spark job
# when the job is started, continue to spark results page
@app.route('/spark_results', methods=['POST'])
def spark_job():
    results = spark_map_csv.spark_job()
    return render_template('spark_results.html', results = results)

# (added 2026) when the user clicks the MLlib button, train and evaluate the
# classifiers and show their scores on the final page
@app.route('/mllib_results', methods=['POST'])
def mllib_job():
    import mllib_2026
    results = mllib_2026.ml_job()
    return render_template('mllib_results.html', results = results)

# serve the app on port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)