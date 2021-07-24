(sed 's,jdbc:mysql://localhost/safa-db,jdbc:h2:mem:safa-db/,g' ".env" >test.env &&
  set -a && source test.env && env && ./gradlew build --stacktrace)
rm test.env
