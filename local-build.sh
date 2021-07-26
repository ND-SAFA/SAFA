(
  sed 's,jdbc:mysql://localhost/safa-db,jdbc:h2:mem:safa-db/,g' ".env" >test.env &&
    ./gradlew build --stacktrace # automatically reads env files
)
echo "DONE"
rm test.env
