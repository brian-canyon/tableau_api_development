README.txt

The purpose of this project is to share some of Tableau API development I have
curated. The high level summary of this project revolves around using the
Tableau supported library 'TableauServerClient' in python. Tableau is a visual
analytics platform transforming the way we use data to solve problems—empowering
people and organizations to make the most of their data.

The use case for this development arrised when attempting to migrate a Tableau
enviroment to both a newer version of Tableau, that was also part of a larger 
server migration from a VM hosting RH7 to RH8. I never could quite identify
why some of the out of the box solutions for server migrations did not work,
however, even with trail alongside a cloud team, we were forced to go with
API development. I was tasked with this migration with moderate support
from a network engineer.

Tableau has a wide variety of metadata that can be passed through the API,
below is a list of the various relevant data variables showcased in this project:

    - Users
    - User Groups (access control, ACL)
    - Projects (file folders)
    - Data Sources
    - Workbooks

The bulk of this project will focus on migrating data from one Tableau enviroment to
another. This should provide a framework for anyone looking to migrate enviroments 
themselves and wants a bit more customizability. 

While Tableau does support documentation for this library, the amount of code snip
examples are few and far between. Specifically in situations where elements of 
a Tableau server want to be copied to a different enviroment, this project
should provide the reader with an extensive blueprint of what is possible.