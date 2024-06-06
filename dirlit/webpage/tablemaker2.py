from bs4 import BeautifulSoup
import os
import pandas as pd

# Import data 
astroinfo = pd.read_excel('17stars1.xlsx')

astroinfo = astroinfo.astype(str)
object_ID = astroinfo.iloc[:,1]
sub_field = astroinfo.iloc[:,2]
coordinate = astroinfo.iloc[:,3]
SNAD_distance = astroinfo.iloc[:,4]
mag_range = astroinfo.iloc[:,10]
colour_index = astroinfo.iloc[:,11]
period_mpa = astroinfo.iloc[:,5]
period_zg = astroinfo.iloc[:,6]
period_zr = astroinfo.iloc[:,7]
period_zi = astroinfo.iloc[:,8]
comments = astroinfo.iloc[:,16]

# Create a new BeautifulSoup object
html = BeautifulSoup(features='html.parser')

# Create a table
table = html.new_tag('table')
html.append(table)

source_names = ["MPA", "ZTF-zg", "ZTF-zi", "ZTF-zr"]
captions = [" Lightcurve", " Periodogram", " #1 period", " #2 period", " #3 period"]

results_path = "starwise/"

plot_preffixes = ["MPA","zg","zi","zr"]
plot_suffixes = ["_lightcurve.png", "_lk.png", "_phase_lc_1.png", "_phase_lc_2.png", "_phase_lc_3.png"]

# Create a 17 x 2 table
for i in range(1,18):
    tr = html.new_tag('tr')
    table.append(tr)
    
    # First td contains the row number in text format
    td1 = html.new_tag('td', style= 'border: 1px solid black')
    h2 = html.new_tag('h2')
    h2.string = str(i)
    td1.append(h2)
    tr.append(td1)
    
    # Second td contains a 2 x 1 table
    td2 = html.new_tag('td')
    tr.append(td2)
    
    # Create a 2 x 1 table
    sub_table = html.new_tag('table')
    td2.append(sub_table)
    
    # Create the first tr in the 2 x 1 table
    sub_tr1 = html.new_tag('tr')
    sub_table.append(sub_tr1)
    
    # First td contains data table
    sub_td1 = html.new_tag('td', style= 'border: 1px solid black')
    sub_tr1.append(sub_td1)

    data_table1 = html.new_tag('table')
    sub_td1.append(data_table1)
    data_table2 = html.new_tag('table')
    sub_td1.append(data_table2)

    data_tr1 = html.new_tag('tr') #The first column will contain astronomical information about the star
    data_tr2 = html.new_tag('tr') #The second column will contain more local information about the star
    data_tr3 = html.new_tag('tr') #The third column will contain more local information about the star
    comments_tr = html.new_tag('tr') #The fourth column will contain my comments
    data_table1.append(data_tr1)
    data_table1.append(data_tr2)
    data_table2.append(data_tr3)
    data_table2.append(comments_tr)

    coord_td = html.new_tag('td', style='padding:10px')
    mag_td = html.new_tag('td', style='padding:10px')
    colour_td = html.new_tag('td', style='padding:10px')
    ID_td = html.new_tag('td', style='padding:10px')
    field_td = html.new_tag('td', style='padding:10px')
    distance_td = html.new_tag('td', style='padding:10px')
    period_mpa_td = html.new_tag('td', style='padding:10px')
    period_zg_td = html.new_tag('td', style='padding:10px')
    period_zi_td = html.new_tag('td', style='padding:10px')
    period_zr_td = html.new_tag('td', style='padding:10px')
    
    comment_td = html.new_tag('td', colspan="4", style='padding:10px; text-align:center')

    coord_td.string = "J2000 Coordinates: "+coordinate[i-1]
    mag_td.string = "Magnitude range: "+mag_range[i-1]
    colour_td.string = "J-K colour index: "+colour_index[i-1]
    ID_td.string = "Local Object ID: "+object_ID[i-1]
    field_td.string = "Local sub-field: "+sub_field[i-1]
    distance_td.string = "Distance (arcsec) from SNAD match: "+SNAD_distance[i-1]
    period_mpa_td.string = "Period from MPA: "+period_mpa[i-1]
    period_zg_td.string = "Period from ZTF-zg: "+period_zg[i-1]
    period_zi_td.string = "Period from ZTF-zi: "+period_zi[i-1]
    period_zr_td.string = "Period from ZTF-zr: "+period_zr[i-1]
    
    comment_td.string = "Comment: "+comments[i-1]

    data_tr1.append(coord_td)
    data_tr1.append(mag_td)
    data_tr1.append(colour_td)
    data_tr2.append(ID_td)
    data_tr2.append(field_td)
    data_tr2.append(distance_td)
    data_tr3.append(period_mpa_td)
    data_tr3.append(period_zg_td)
    data_tr3.append(period_zi_td)
    data_tr3.append(period_zr_td)
    
    comments_tr.append(comment_td)

    # Create the second tr in the 2 x 1 table
    sub_tr2 = html.new_tag('tr')
    sub_table.append(sub_tr2)
    
    # Second td contains a 1 x 2 table
    sub_td2 = html.new_tag('td')
    sub_tr2.append(sub_td2)
    
    # Create a 1 x 2 table
    sub_sub_table = html.new_tag('table')
    sub_td2.append(sub_sub_table)
    
    # Create the only tr in the 1 x 2 table
    sub_sub_tr = html.new_tag('tr')
    sub_sub_table.append(sub_sub_tr)
    
    # First td contains a 4 x 1 table of images
    sub_sub_td1 = html.new_tag('td')
    sub_sub_tr.append(sub_sub_td1)

    sub_sub_sub_table1 = html.new_tag('table')
    sub_sub_td1.append(sub_sub_sub_table1)
    
    # Create a 4 x 1 table of images
    for ii in range(4):
        image_path = results_path + str(i) + "/" + plot_preffixes[ii] + plot_suffixes[0]
        if os.path.exists(image_path):
            sub_sub_sub_tr = html.new_tag('tr')
            sub_sub_sub_table1.append(sub_sub_sub_tr)
            sub_sub_sub_td = html.new_tag('td')
            img = html.new_tag('img', src=image_path, width='350')
            sub_sub_sub_td.append(img)
            caption = html.new_tag('figcaption', style="text-align:center")
            caption.string = source_names[ii]+captions[0]
            sub_sub_sub_td.append(caption)
            sub_sub_sub_tr.append(sub_sub_sub_td)
    
    # Second td contains a 4 x 4 table of images
    sub_sub_td2 = html.new_tag('td')
    sub_sub_tr.append(sub_sub_td2)
    
    sub_sub_sub_table2 = html.new_tag('table')
    sub_sub_td2.append(sub_sub_sub_table2)

    # Create a 4 x 4 table of images
    for ii in range(4):
        sub_sub_sub_tr = html.new_tag('tr')  # Create a new row for images and captions
        sub_sub_sub_table2.append(sub_sub_sub_tr)
        
        for iii in range(4):
            image_path = results_path + str(i) + "/" + plot_preffixes[ii] + plot_suffixes[iii+1]
            if os.path.exists(image_path):
                img = html.new_tag('img', src=image_path, width='350')
                sub_sub_sub_td = html.new_tag('td')
                sub_sub_sub_td.append(img)
                caption = html.new_tag('figcaption', style="text-align:center")
                caption.string = source_names[ii]+captions[iii+1]
                sub_sub_sub_td.append(caption)
                sub_sub_sub_tr.append(sub_sub_sub_td)

# Save the HTML to a file
with open('output.html', 'w') as file:
    file.write(str(html))

