import os
import requests
from bs4 import BeautifulSoup

# Full path of the mockup file
file_name = os.path.realpath(os.path.join(os.path.dirname(__file__), '..')) + '\\Content\\basic_example.htm'

if __name__ == "__main__":

    # Reading xml file and store into soup object
    file_name = os.path.realpath(os.path.join(os.path.dirname(__file__), '..')) + '\\Content\\basic_example.htm'
    with open(file_name, "r", encoding="utf-8") as file:
        example = BeautifulSoup(file, 'xml')


    print(example.prettify())


    # Let's search for objects now

    h1 = example.find('h1')

    # Print entire tag
    print(h1)

    # Print just the text (
    print(h1.string)

    p_tag = example.find('p', id="image")
    print(p_tag)


    # Let's now get all of the links that exist on this page
    a_tags = example.findAll('a')

    for a_tag in a_tags:

        #Access attributes using brackets
        print(a_tag['href'])


    # This even works with webpages!
    madcap_page = 'https://www.madcapsoftware.com/madworld-conferences/madworld-2023'
    madcap_soup = BeautifulSoup(requests.get(madcap_page).content, 'html')


    for tag in madcap_soup.findAll('a'):
        print(tag['href'])

    # Let's go back to our mockup page though and make some changes
    # Improve our h1

    print(h1)
    # Results: <h1>This is h1</h1>
    h1.string = 'This is a better h1!'
    print(h1)
    # Results: <h1>This ia a better h1!</h1>

    # Let's also change our image to a frowny face
    picture = example.find('img')
    print(picture)
    # Results: <img src="Resources/Images/example/smiley_face.jpg"/>
    picture['src'] = 'Resources/Images/example/frowny_face.jpg'
    print(picture)
    # Results: <img src="Resources/Images/example/frowny_face.jpg"/>



    # Let's clear out the p tag now, we don't need it!

    p_tag = example.find('p', id="image")
    print(p_tag)
    # Results: <p id="image"><img src="Resources/Images/example/frowny_face.jpg"/></p>
    p_tag.clear()
    print(p_tag)
    # Results: <p id="image" />

    # Now let's add a new image tag with some new attributes

    new_tag_attrs = {}
    new_tag_attrs['src'] = "Resources/Images/example/smiley_face.jpg"
    new_tag_attrs['class'] = "icon_big"
    new_tag_attrs['alt'] = "Smiley Face"

    new_img = example.new_tag('img', **new_tag_attrs)
    p_tag.append(new_img)

    print(p_tag)
    # Results: <p id="image"><img alt="Smiley Face" class="icon_big" src="Resources/Images/example/smiley_face.jpg"/></p>


    # All of these changes are just local right now - we need to save them back to the file

    with open(file_name, "w", encoding="utf-8") as file:
        # The new line characters are replaced because Python and Flare use different characters. Not switching it causes
        # Extra line breaks all over the place
        file.write(str(example).replace('\r\n', '\n'))


"""


"""







