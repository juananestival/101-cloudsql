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

https://javascript.plainenglish.io/angular-translating-the-application-language-using-angular-localize-and-deploying-it-to-firebase-d2b127e64496

download https://poedit.net/
https://dev.to/batbrain9392/internationalization-with-angular-v10-693

https://medium.com/dailyjs/maintaining-multi-language-angular-applications-26b74df8d085
#  Create the app
1. Create an application with routing
2. Common steps
* material
* configure routes
* Home Screen 
* First component
* router outlet

```sh
ng add @angular/material
```
#  Install and setup the localize package
1. Install
```sh
ng add @angular/localize
```

2. edit
Edit the angular .json
When workinng with projece the json chain will be 
root (the first open bracket )->projects->(name of the project)
Just below the name of the project. (att the same level than project type or schematic)
We will need 
* the locale in which sourc code is written (sourceLocale)
* the locales to be tranlated and where the translation file is:
    Note: you can choose json or xliff. Xliff has the advnagege that witn online editor you can translate easily
        http://xliff.brightec.co.uk/index.php
        https://poeditor.com/

* at the same level of what we are creating root (the first open bracket )->projects->(name of the project). 
* architect-> build -> options ->


```json
  "projects": {
    "101-angular-internacinalization": {
      "i18n":{
        "sourceLocale":"en-US",
        "locales": {"es-ES":"src/locale/messages.es.xlf"}
      },
      ...
      "architect": {
        "build": {
          "builder": "@angular-devkit/build-angular:browser",
          "options": {
            "localize":["es-ES"],

```

Take into account that ng serve "naked" will fail now. 

3. Prepare components
Edit templates
```html
<p i18n>for test sample-component works!</p>
<p i18n> for dates like {{"05/01/2022" | date}} use pipe</p>
<p i18n> for currencies like {{129 | currency}} use pipe</p>
<p i18n> for test of images</p>
<img alt="just me" i18n-alt src="../assets/yo.jpeg">
```

edit code 
```ts
import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser'

@Component({
  selector: 'app-sample-component',
  templateUrl: './sample-component.component.html',
  styleUrls: ['./sample-component.component.scss']
})
export class SampleComponentComponent implements OnInit {

  title = 'your title'
  constructor(private titleService:Title) { 
    this.titleService.setTitle($localize`${this.title}`)
  }

  ngOnInit(): void {
  }

}
```

4. Extract
```sh
ng extract-i18n --output-path src/locale
```
the folder locale is created
in json
```sh
ng extract-i18n --output-path src/locale --format json
```

In json we will see a file like
```json
{
  "locale": "en-US",
  "translations": {
    "8286437328803353698": "for test sample-component works!",
    "1586441093982144361": " for dates like {$INTERPOLATION} use pipe",
    "8230667035758312692": " for currencies like {$INTERPOLATION} use pipe",
    "3271070469815256851": " for test of images",
    "4323851768315885124": "just me",
    "1737753151350322492": "{$PH}"
  }
}
``` 
5. translate
Just create a copy and name it with the lang proper extension. Remeber the file name of the angular.json

Now ng serve will serve only the localized version (es)

Build the app
```sh
ng build --localize  
```
and serve it with a local server
```sh
serve dist/101-angular-internacinalization
```
Now you can call both url 
http://localhost:3000/en-US/home
http://localhost:3000/es-ES/home


# Inject a switcher
configure providers in app.module.ts
```json
 providers: [
    {
    provide:LOCALE_ID,
    useValue:"en-US"
    },

```
this mean that we will inject a locale id and that if not the default is en-US

