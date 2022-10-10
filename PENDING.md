enviroment variables
permision secret manager
brew install libpq
echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

https://cloud.google.com/sql/docs/postgres/connect-instance-cloud-shell?utm_source=codelabs&utm_medium=et&utm_campaign=CDR_jkl_databases_dbcodelabs_&utm_content=-


ensure that the account has access to "cepf-l300-juananestival:us-central1:main-instance" (and make sure there's no typo in that name). Error during generateEphemeral for cepf-l300-juananestival:us-central1:main-instance: googleapi: Error 403: The client is not authorized to make this request., notAuthorized

the service account of the cloud function must to have sql client


\connect library;
CREATE TABLE books (title VARCHAR(100));
INSERT into books (title) VALUES ('Cloud SQL for Winners');;



CREATE TABLE entries (guestName VARCHAR(255), content VARCHAR(255),
                        entryID SERIAL PRIMARY KEY);
INSERT INTO entries (guestName, content) values ('first guest', 'I got here!');
INSERT INTO entries (guestName, content) values ('second guest', 'Me too!');


stmt = sqlalchemy.text('insert into {} ({}) values ({})'.format(table_name, table_field, table_field_value))

```py
stmt = sqlalchemy.text('insert into {} ({}, {}) values ({}, {})'.format(table_name, table_field1, table_field_value1, table_field2, table_field_value2))
```