post_path = '/home/pi/post.txt'

open(post_path, 'w').close()
postfile = open(post_path, 'a')
postfile.write("Run Burgundy - Decentralized Fitness Group - Activity Log: .\n") ### This line is the title of the post
postfile.write("fitnation running cycling hiking fitness\n") ### This line holds the tags
postfile.write("![Run_Burgandy.png](https://steemitimages.com/DQmewBzW8MzewBP3qcUJzNL79hmfzM1qUquedRdSaLX83K4/Run_Burgandy.png)\n") ### This line should be the header image

