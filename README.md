# dmd
>**No society can legitimately call itself civilised if a sick person is denied medical aid because of lack of means.**
>Aneurin Bevan, _In Place of Fear_

NHS Dictionary of medicines and devices (dm+d) SQL parser

These Python and SQL scripts are used to parse the dm+d releases in XML format into a MySQL database. Relational fields are referenced together using foreign keys, and the description of the columns are stored in their comments.

You can download the official releases of dm+d for free from https://isd.digital.nhs.uk.

## Usage
Install MySQL server, unzip the dm+d releases into a folder and clone this repo.

Run `python parser.py -u [your mysql username] -p [your mysql password] -d [relative or absolute path to the directory containing the dm+d folders]`
