letter = readtable("folder\file.txt");              %add the corresponding path
letter.Time = (letter.Time - letter.Time(1))/1000;
plot(letter.X,letter.Y)
axis equal

dur = letter.Time(end)
aratio = range(letter.Y)/range(letter.X)
