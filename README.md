# dmd
NHS Dictionary of medicines and devices (dm+d) SQL parser

These Python and SQL scripts are used to parse the dm+d releases in XML format into a MySQL database. Relational fields are referenced together using foreign keys, and the description of the columns are stored in their comments.

You can download the official releases of dm+d for free from https://isd.digital.nhs.uk.

## Usage
Install MySQL server, unzip the dm+d releases into a folder and clone this repo.

Run `python parser.py -u [your mysql username] -p [your mysql password] -d [relative or absolute path to the directory containing the dm+d folders]`

## Disclaimer
This project is not endorsed by the National Health Service or any of its authorities and trusts.

I am not a healthcare professional. As expressed in the LICENSE, this software is provided without warranties or conditions of any kind. Should the software itself or any of its output be used for clinical purposes, it is the healthcare practitioner's sole responsibility to verify the correctness, validity and appropriateness of any information related to this software and its outputs.
