import numpy as np
import pandas as pd
from datetime import datetime
import re

def escape_german_umlauts(text):
    replacements = {
        'ä': '&auml;',
        'ö': '&ouml;',
        'ü': '&uuml;',
        'Ä': '&Auml;',
        'Ö': '&Ouml;',
        'Ü': '&Uuml;',
        'ß': '&szlig;'
    }
    for char, html_entity in replacements.items():
        text = text.replace(char, html_entity)
    return text



logo_files = {
    'Athletenpräsentation'      : '',
    'Avetana'                   : 'avetana_brighter.png',
    'Badisch Brauhaus'          : 'badisch-brauhaus_white.png',
    'Beinert & Partner'         : 'Beinert und Partner_brightened.png',
    'Brenner Gebäudereinigung'  : 'brenner_kleiner.png',
    'Die Stadtmitte Nachtclub'  : 'Logo Stadtmitte weiss.png',
    'Ford Wolf'                 : 'Wolf_logo15.png',
    'Freizeitlauf'              : '',
    'Hoepfner'                  : '2000px-Privatbrauerei_Hoepfner.png',
    'Indoor Meeting'            : 'indoor_meeting.png',
    'Joggling'                  : '',
    'M&M Sports'                : 'm_und_m_sports_white.png',
    'Nussbaumer'                : 'logo-nuss_white.png',
    'Osteopathie Besse'         : '',
    'Peterstaler'               : 'peterstaler.jpg',
    'PUMA NITRO'                : 'Puma_Nitro.png',
    'REWE'                      : 'REWE_4c_negativ.jpg',
    'San Lucar'                 : 'sanlucar-logo.png',
    'Scholarbook'               : 'scholarbook.png',
    'Siegerehrung'              : '',
    'Sparkasse Karlsruhe'       : 'Sparkasse Karlsruhe Logo 2021 Negativ Rot.jpg',
    'Stadt Karlsruhe'           : 'stadt_KA_white.png',
    'Top4Running'               : 'Top4Running Logo white.png',
    'Trimedic'                  : 'trimedic_white.png',
    'Weingut Anselmann'         : 'Anselmann Logo_white.png',
    ''                          :'',
    'Siegerehrung1500M'         : 'SE_1500_M.png',
    'Siegerehrung1500W'         : 'SE_1500_W.png',
    'Siegerehrung800M'          : 'SE_800_M.png',
    'Siegerehrung800W'          : 'SE_800_W.png',
    'Siegerehrung5000M'         : 'SE_5000_M.png',
    'Siegerehrung5000W'         : 'SE_5000_W.png',
    'Siegerehrung3000HiM'       : 'SE_3000Hi_M.png',
    'Siegerehrung3000HiW'       : 'SE_3000Hi_W.png',
    'HPP Vermögensverwaltung'   : 'pohlig.svg',
    'wus-media'                 : 'wus_media.png',
    'REHA med Herxheim'         : 'reha_med.png',
    'Auth Kälte- & Klimatechnik': 'logo_auth.jpg',
    'Sasse'                     : 'sasse.png',
    }


table = pd.read_csv('tabelle.csv', skiprows=0, na_filter=False, header = 0)
# only keep the columns we want
columns_to_keep = ['Lauf', 'm/w', 'Nummer', 'Buchstabe', 'Zeit', 'Pace', 'Partner']
table = table.loc[:, columns_to_keep]
# throw away rows in which column "Lauf" contains "NaN":
# table = table[table['Lauf'] != '']
# convert values in column "Nummer" to integer
table['Nummer'] = pd.to_numeric(table['Nummer'], errors='coerce').astype('Int64')
# replace all 'NaN' entries with ''
# table = table.replace('NaN', '', regex=True)
# table = table.replace('<NA>', '', regex=True)
# print(table)

html_start = '''<!DOCTYPE html>
                <html lang="en">

                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>LLN Videowand</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
                    <link rel="icon" type="image/x-icon" href="Logos/cropped-cropped-cropped-Lange_Laufnacht_rund-1.webp">
                    <link rel="stylesheet" type="text/css" href="style.css">
                    
                </head>

                <body>
                        
                        <!-- MEETING RECORD -->
                        <div class="align-items-center overlay" id="meetingRecord">
                            <div class="row align-items-center">
                              <div class="col-md-5" style="text-align: right;">
                                <img src="Logos/LLN_medium.png" loading="lazy" class="img-fluid">
                              </div>
                              <div class="col-md-7" style="text-align: left;">
                                <p class="hRecord"> Meeting Record!</p>
                              </div>
                            </div>
                            <canvas class="confetti" id="mrCanvas"></canvas>
                        </div>
                        
                        
                        <!-- OLYMPIC STANDARD -->
                         <div class="align-items-center overlay" id="worldRecord">
                            <div class="row align-items-center">
                              <div class="col-md-5" style="text-align: right;">
                                <img src="Logos/LLN_medium.png" loading="lazy" class="img-fluid">
                              </div>
                              <div class="col-md-7" style="text-align: left;">
                                <p class="hRecord"> Olympic Standard!</p>
                              </div>
                            </div>
                            <canvas class="confetti" id="wrCanvas"></canvas>
                        </div>
                        
                        
                        <!-- ALL SPONSORS -->
                         <div class="align-items-center overlay" id="allSponsors">
                             <img src="Einblendungen/alle_sponsoren.png" class="img-fluid">
                        </div>
                        
                        
                        <!-- LGR -->
                         <div class="align-items-center overlay" id="lgr">
                             <img src="Einblendungen/LGR.png" class="img-fluid">
                        </div>
                        
                        
                        <!-- PACERS IN ALL RACES -->
                         <div class="align-items-center overlay" id="pacersInAllRaces">
                             <img src="Einblendungen/pacers_in_all_races.png" class="img-fluid">
                        </div>
                        
                
                        <!-- HEADER -->
                        <div class="sticky-header">
                            <div class="header-box">
                                <div class="col">
                                    <h1>Lange Laufnacht</h1>
                                </div>
                                <div class="col">
                                    <img class="logo" src="Logos/WAC.png" loading="lazy">
                                    </div>
                                <div class="col">
                                    <img class="logo" src="Logos/LLN.png" loading="lazy">
                                </div>           
                            
                            </div>
                            <!-- YELLOW LINE>
                            <div style="background-color: yellow; height: 1vh; width: vw;">
                            </div -->
                        </div>
                        
                        
                        
                        <!-- ACCORDION -->
                        <div class="m-4" style="padding: 0; margin:0;">
                            <div class="accordion" id="myAccordion">

            '''

html_ending = '''
                        </div>
                    </div>
                    <div style="background-color: black; height: 100vh"></div>
                </div>
                
                <script type='text/javascript' src="confettiEffect.js"></script>
                <script type='text/javascript' src="toggleAnimations.js"></script>
                <script src="https://scripts.sirv.com/sirvjs/v3/sirv.js"></script>
                    
            </body>
            </html>
            '''

accordion_item_template = '''  <div class="accordion-item">
                                    <button type="button" class="accordion-button collapsed" data-bs-toggle="collapse"
                                        data-bs-target="#collapse{index}">
                                        <div class="row">
                                            <div class="col-1">
                                                {time}
                                            </div>
                                            <div class="col-2" style="text-align: right;">
                                                {distance}
                                            </div>
                                            <div class="col-1">
                                                {gender}
                                            </div>
                                            <div class="col-6" style="padding-left: 5vw; font-size:{font_size}">
                                                {sponsor}
                                            </div>
                                            <div class="col-2" style="text-align: right;">
                                                {pace}
                                            </div>
                                        </div>
                                    </button>
                                <div id="collapse{index}" class="accordion-collapse collapse" data-bs-parent="#myAccordion">
                                    <div class="card-body d-flex justify-content-center align-items-center">
                                        <img class="sponsoren-logo Sirv" data-src="{image_path}">
                                    </div>
                                </div>
                            </div>
                        '''
              
html_content = html_start
                        
for index, element in table.iterrows():
    event_time = element['Zeit']
    
    event_distance = element['Lauf']
    
    # remove all numbers '\d+' and paranthesis '(' and ')' from string
    event_sponsor = re.sub(r'\(\d+\)', '', element['Partner'])
    # remove last character if it is whitespace
    if event_sponsor.endswith(" "):
        event_sponsor = event_sponsor[:-1]
    # get path of logo:
    image_path = logo_files[event_sponsor]
    if event_sponsor == 'Siegerehrung':
        image_path = 'SE' + event_distance + '.png'
    if image_path == '': image_path='placeholder.png'
    image_path = 'Sponsoren/' + image_path
    # print(image_path)
    
    # replace ä with '&auml'
    # event_sponsor = re.sub(r'ä', '&auml', event_sponsor)
    event_sponsor = escape_german_umlauts(event_sponsor)

    
    if 'Hi' not in event_distance and event_distance != '': 
        event_distance = event_distance + 'm'
        
    
    
    if 'MU16' in event_distance:
        event_gender = 'MU16'
        event_distance = re.sub(r'[MU16]', '', event_distance)
        event_sponsor = "\t"+ event_sponsor
    elif 'WU16' in event_distance :
        event_gender = 'WU16'
        event_distance = re.sub(r'[WU16]', '', event_distance)
    elif 'ATHL' in element['m/w']:
        event_gender = ''
    else:
        event_gender = element['m/w']
        
        
    
    event_pace = element['Pace']
    font_size = '3.5rem'
    
    if 'Brenner' in event_sponsor:
        font_size = '3.4rem'
    div_element = accordion_item_template.format(index=index, 
                                                 time=event_time, 
                                                 distance=event_distance,
                                                 gender=event_gender,
                                                 sponsor=event_sponsor,
                                                 pace=event_pace,
                                                 font_size=font_size,
                                                 image_path=image_path)
    html_content += div_element
    
    

    
    
html_content += html_ending
file_name = "index.html"

# Write the HTML content to the file
with open(file_name, "w") as file:
    file.write(html_content)

print(f"HTML file '{file_name}' has been created.")
    
    