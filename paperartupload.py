import os
from bs4 import BeautifulSoup

# Path to your images folder
images_folder = "dirart/Paper"

# Path to your gallery HTML file
gallery_html_file = "dirart/paper.html"

# Get list of image files in the images folder
images = sorted([f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))])

numberOfImages = len(images)

# Read the gallery HTML file
with open(gallery_html_file, 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table with id "imageTable"
table = soup.find('table', {'id': 'imageTable'})

soup.table.clear()

# Add each image to the table
for i in range(0,int(numberOfImages/4)+1):
    # Create a new table row and cell for the image
    print(i)
    
    row = soup.new_tag('tr')
    for j in [0,1,2,3]:
        if 4*i+j<numberOfImages:
            cell = soup.new_tag("td", attrs={"class": "arttd"})
            img = soup.new_tag('img', src=f'Paper/{images[4*i+j]}', alt=images[4*i+j], width="400")
            cell.append(img)
            row.append(cell)
    table.append(row)
    

# Write the updated HTML content back to the file
with open(gallery_html_file, 'w') as file:
    file.write(str(soup))

print("Gallery updated successfully!")
