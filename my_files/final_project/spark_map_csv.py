def spark_job():
    import findspark
    findspark.init()
    from pyspark.sql import SparkSession
    # This resolves pyspark python path issues
    

    # Create a SparkSession
    spark = SparkSession.builder\
        .appName("spark_map")\
        .master("local[*]")\
        .config("spark.jars", "/home/nikos/big_data/python_programs/final_project/jars/spark-avro_2.12-3.2.1.jar")\
        .getOrCreate()

    # Load csv file into DataFrame
    students = spark.read.csv("file:///home/nikos/big_data/python_programs/final_project/student.csv", header=True, sep=",", inferSchema=True)

    # # Print the schema
    # students.printSchema()

    results = []

    # find number of students with admission grade >= 160
    students_160 = students.filter(students.Admission_grade >= 160)
    results.append("Number of students with grade >= 160: " + str(students_160.count()))

    # find number of students that attend in the evening and those that attend in the morning
    students_evening = students.filter(students.Day_evening_attendance == 0)
    students_morning = students.filter(students.Day_evening_attendance == 1)
    results.append("Number of students that attend in the evening: " + str(students_evening.count()))
    results.append("Number of students that attend in the morning: " + str(students_morning.count()))

    # find number of students that attend in the evening with admission grade >= 160 compared to total number of evening students
    students_evening_160 = students.filter(students.Day_evening_attendance == 0).filter(students.Admission_grade >= 160)
    results.append("Number of students that attend in the evening with grade >= 160: " + str(students_evening_160.count()))
    results.append("Percentage of students that attend in the evening with grade >= 160: " + str("{:.2f}".format((students_evening_160.count() / students_evening.count()) * 100)) + "%")

    # find number of students that attend in the morning with admission grade >= 160 compared to total number of morning students
    students_morning_160 = students.filter(students.Day_evening_attendance == 1).filter(students.Admission_grade >= 160)
    results.append("Number of students that attend in the morning with grade >= 160: " + str("{:.2f}".format((students_morning_160.count() / students_morning.count()) * 100)) + "%")

    # find number of students that attend at their top 2 choice college
    students_top2_pick = students.filter(students.Application_order <= 1)
    results.append("Number of students that attend at their first or second choice of college: " + str(students_top2_pick.count()))

    # show values of student that entered in their top choice of college
    student_top_pick = students.filter(students.Application_order == 0)
    results.append("The only student that entered in their top 1 choice of college:\n" + str(student_top_pick.collect()))

    # write All Dataframe findings on HDFS
    students.write.format("avro").options().mode("overwrite").save("/queries/students.avro")
    students_160.write.format("avro").mode("overwrite").save("/queries/students_160.avro")
    students_evening.write.format("avro").mode("overwrite").save("/queries/students_evening.avro")
    students_morning.write.format("avro").mode("overwrite").save("/queries/students_morning.avro")
    students_evening_160.write.format("avro").mode("overwrite").save("/queries/students_evening_160.avro")
    students_morning_160.write.format("avro").mode("overwrite").save("/queries/students_morning_160.avro")
    students_top2_pick.write.format("avro").mode("overwrite").save("/queries/students_top2_pick.avro")
    student_top_pick.write.format("avro").mode("overwrite").save("/queries/student_top_pick.avro")

    return results

# read Dataframe findings from HDFS
# students_160_read = spark.read.format("avro").load("/queries/students_160.avro")
# print("Number of students with grade >= 160: ", students_160_read.count())
