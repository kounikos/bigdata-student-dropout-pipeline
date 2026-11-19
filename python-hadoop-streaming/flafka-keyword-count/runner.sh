hadoop jar /home/nikos/big_data/python_programs/hadoop-streaming-3.3.2.jar \
-input /Flafka_weather_data/ \
-output /Flafka_reduce_weather/ \
-mapper /home/nikos/big_data/python_programs/flafka_weather/mapper.py \
-reducer /home/nikos/big_data/python_programs/flafka_weather/reducer.py