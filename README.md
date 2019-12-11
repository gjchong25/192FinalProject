# 192FinalProject
Final project for CIS 192

## Running the script

In order to run the script, run the command python spotifyProj.py [insert spotify username here]. Make sure no other spotify users are logged in at this time. Also, in order to find your spotify username, you can go to your spotify profile, click on your profile picture, the 3 horizontal dots for the settings menu, go to 'Share', then click on the 'Copy Spotify URI ' button. You may see something like this: "spotify:user:22727lpkw7t7zy7p2gicvwvgy", and everything after the 'user:' should be your username or unique id. Users who log into spotify through facebook may have numbers and random strings in their usernames. You may be redirected to another link, and the terminal will prompt you to copy and paste the URL that you were redirected into the terminal. After entering the redirect URL into the terminal, the script should run and print out the necessary information.

This command should display a user's top 5 tracks, or songs, for short term, medium term, and long term durations. It will also display the musical qualities of these top songs, looking at aspects such as valence, energy, danceability, tempo, and more of the user's top songs.

## Flask app
Once you've run the script, in order to see the flask app you can run the command 'python server.py' and then navigate to localhost:8080/. Make sure no other users are logged in at this time, otherwise Spotify will automatically log the currently logged in user in. Once you go to localhost:8080/, you will be prompted with a spotify sign in, which you must fill out with your spotify username/email and password. Once you login to the site, you should have choices to view your current top tracks, the musical features of your short term top songs, medium and long term songs. If you would like to learn more about the different musical aspects about your favorite songs, click on some of these buttons.  

## Additional notes

Caches are created every time a user authenticates and allows the use of their data, so that the user only has to allow for use of their data once and not repeatedly. However, some of the tokens used to authenticate may have to be refreshed occasionally. In this case simply delete the old cache, run the spotifyProj.py script again, and then run server.py. 

## Design Consideration
We used a website called Bootswatch that had free themes for Bootstrap to design most of the layout of the website. The link to this website can be found below: https://bootswatch.com/lux/
