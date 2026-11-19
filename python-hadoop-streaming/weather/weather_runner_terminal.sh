hadoop jar /home/nikos/big_data/python_programs/hadoop-streaming-3.3.2.jar \
-input /weather_python/ \
-output output/weather_python/output1 \
-mapper /home/nikos/big_data/python_programs/weather/weather_mapper_d.py \
-reducer /home/nikos/big_data/python_programs/weather/weather_reducer_d.py