# TF*IDF Glossary App

This is an app that parses XLIFF files, then uses the TF*IDF metric to extract the most important words in your translation project. This helps to create a glossary much more efficiently.

The project uses Flask for a server. Python 3.7. Install all libs using the requirements file.

## TO DO:
1. DONE Make the "Export CSV" button download the CSV file.
2. Make it possible to drop multiple files on the upload page.
3. User session: save the TF*IDF results and CSV file per user session, without a database.
4. Make it possible to delete terms before export.
5. Add some nice styles.